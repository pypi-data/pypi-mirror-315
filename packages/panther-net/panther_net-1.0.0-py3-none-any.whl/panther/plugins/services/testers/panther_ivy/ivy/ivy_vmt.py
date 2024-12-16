#
# Copyright (c) Microsoft Corporation. All Rights Reserved.
#

from . import ivy_module as im
from . import ivy_actions as ia
from . import ivy_logic as il
from . import ivy_transrel as tr
from . import ivy_logic_utils as ilu
from . import ivy_utils as iu
from . import ivy_art as art
from . import ivy_interp as itp
from . import ivy_theory as thy
from . import ivy_ast
from . import ivy_proof
from . import ivy_trace
from . import ivy_solver as slvr

import tempfile
import subprocess
from collections import defaultdict
import itertools
import sys
import os

logfile = None
verbose = False

def checked(thing):
    return ia.checked_assert.value in ["",thing.lineno]

def action_to_tr(mod,action,method):
    bgt = mod.background_theory()
    if method=="fsmc":  # if finite-state, unroll the loops
        with ia.UnrollContext(im.module.sort_card):
            upd = action.update(im.module,None)
    else:
        upd = action.update(im.module,None)
    stvars,trans,error = tr.add_post_axioms(upd,bgt)
    trans = ilu.and_clauses(trans,ilu.Clauses(defs=bgt.defs))
    defsyms = set(x.defines() for x in bgt.defs)
    rn = dict((tr.new(sym),tr.new(sym).prefix('__')) for sym in defsyms)
    trans = ilu.rename_clauses(trans,rn)
    error = ilu.rename_clauses(error,rn)
    stvars = [x for x in stvars if x not in defsyms]  # Remove symbols with state-dependent definitions
    return (stvars,trans,error)

def add_err_flag(action,erf,errconds):
    if isinstance(action,ia.AssertAction):
        if checked(action):
            if verbose:
                print("{}Model checking guarantee".format(action.lineno))
            errcond = ilu.dual_formula(il.drop_universals(action.formula))
            res = ia.AssignAction(erf,il.Or(erf,errcond))
            errconds.append(errcond)
            res.lineno = iu.nowhere()
            return res
        if isinstance(action,ia.SubgoalAction):
#            print "skipping subgoal at line {}".format(action.lineno)
            return ia.Sequence()
    if isinstance(action,ia.AssumeAction) or isinstance(action,ia.AssertAction):
        if isinstance(action,ia.AssertAction):
            if verbose:
                print("assuming assertion at line {}".format(action.lineno))
        res = ia.AssumeAction(il.Or(erf,action.formula)) 
        res.lineno = iu.nowhere()
        return res
    if isinstance(action,(ia.Sequence,ia.ChoiceAction,ia.EnvAction,ia.BindOldsAction)):
        return action.clone([add_err_flag(a,erf,errconds) for a in action.args])
    if isinstance(action,ia.IfAction):
        return action.clone([action.args[0]] + [add_err_flag(a,erf,errconds) for a in action.args[1:]])
    if isinstance(action,ia.LocalAction):
        return action.clone(action.args[:-1] + [add_err_flag(action.args[-1],erf,errconds)])
    return action

def add_err_flag_mod(mod,erf,errconds):
    for actname in list(mod.actions):
        action = mod.actions[actname]
        new_action = add_err_flag(action,erf,errconds)
        new_action.formal_params = action.formal_params
        new_action.formal_returns = action.formal_returns
        mod.actions[actname] = new_action


# Take a function sort and return a corresponding array sort.
def create_array_sort(sort):
    def aname(i):
        if i == len(sort.dom):
            return (sort.rng.name,[sort.rng])
        sname,ssorts = aname(i+1)
        name = 'arr[' + sort.dom[i].name + '][' + sname + ']'
        if name not in il.sig.sorts:
            asort = il.UninterpretedSort(name)
            il.add_sort(asort)
            il.sig.interp[name] = name
        return (name,[il.sig.sorts[name]]+ssorts)
    return aname(0)

# Should I convert this symbol to an array?

def encode_as_array(sym):
    return not il.is_interpreted_symbol(sym) and sym.name not in im.module.destructor_sorts

# Convert all uninterpreted functions in a formula to
# arrays.

def uf_to_arr_ast(ast):
    args = [uf_to_arr_ast(arg) for arg in ast.args]
    if il.is_app(ast) and not il.is_named_binder(ast) and ast.args:
        sym = ast.rep
        if encode_as_array(sym):
            sname,ssorts = create_array_sort(sym.sort)
            asym = il.Symbol(sym.name,ssorts[0])
            for i,arg in enumerate(args):
                sel = il.Symbol('arrsel',il.FunctionSort(asym.sort,arg.sort,ssorts[i+1]))
                asym = sel(asym,arg)
            return asym
    return ast.clone(args)
            
def encode_assign(asgn,lhs,rhs):
    sym = lhs.rep
    if sym.name in im.module.destructor_sorts:
        (nlhs,nrhs) = encode_assign(asgn,lhs.args[0],rhs)
        return (lhs.clone([nlhs]+[lhs.args[1:]]),rhs)
    else:
        lvs = set(ilu.variables_ast(lhs));
        rvs = set(ilu.variables_ast(rhs));
        if any(v in rvs for v in lvs):
            raise iu.IvyError(asgn,'cannot convert paramaterized assignment to VMT')
        sym = lhs.rep
        sname, ssorts = create_array_sort(sym.sort)
        asort = ssorts[0]
        asym = il.Symbol(sym.name,asort)
        arhs = uf_to_arr_ast(rhs)
        def recur(i,val):
            if i == len(lhs.args):
                return arhs
            idx = lhs.args[i]
            if il.is_variable(idx):
                sval = recur(i+1,None)
                return il.Symbol('arrcst',il.FunctionSort(ssorts[i+1],ssorts[i]))(sval)
            if val is None:
                raise iu.IvyError(asgn,'cannot convert paramaterized assignment to VMT')
            aidx = uf_to_arr_ast(idx)
            sel = il.Symbol('arrsel',il.FunctionSort(ssorts[i],aidx.sort,ssorts[i+1]))
            sval = recur(i+1,sel(val,aidx))
            upd = il.Symbol('arrupd',il.FunctionSort(ssorts[i],aidx.sort,ssorts[i+1],ssorts[i]))
            return upd(val,aidx,sval)
        return(asym,recur(0,asym))
        
def uf_to_array_action(action):
    if isinstance(action,ia.Action):
        args = [uf_to_array_action(act) for act in action.args]
        if isinstance(action,ia.AssignAction):
            if action.args[0].args and not il.is_interpreted_symbol(action.args[0].rep):
                args = encode_assign(action,action.args[0],action.args[1])
        return action.clone(args)
    else:
        return uf_to_arr_ast(action)

def has_assert(action):
    for x in action.iter_subactions():
        if isinstance(x,ia.AssertAction):
            return True
    return False

def check_isolate(method="mc"):
    mod = im.module
    
    # Use the error flag construction to turn assertion checks into
    # an invariant check.

    erf = il.Symbol('err_flag',il.find_sort('bool'))
    errconds = []
    has_erf = any(has_assert(mod.actions[x]) for x in mod.actions)
    if has_erf:
        add_err_flag_mod(mod,erf,errconds)
    
    # Combine all actions nto a single action

    actions = [(x,mod.actions[x].add_label(x)) for x in sorted(mod.public_actions)]
#    action = ia.EnvAction(*ext_acts)
    if has_erf:
        actions = [(x,ia.Sequence(ia.AssignAction(erf,il.Or()).set_lineno(iu.nowhere()),act))
                   for x,act in actions]

    # We can't currently handle assertions in the initializers

    for (name,init) in mod.initializers:
        if has_assert(init):
            raise iu.IvyError(x,'VMT cannot handle assertions in initializers')
    

    # Build a single initializer action
    init_action = ia.Sequence(*[act for (nm,act) in mod.initializers])

    
    # get the invariant to be proved, replacing free variables with
    # skolems. First, we apply any proof tactics.

    pc = ivy_proof.ProofChecker(mod.labeled_axioms,mod.definitions,mod.schemata)
    pmap = dict((lf.id,p) for lf,p in mod.proofs)
    conjs = []
    for lf in mod.labeled_conjs:
        if not checked(lf):
#            print 'skipping {}'.format(lf)
            continue
        if verbose:
            print("{}Model checking invariant".format(lf.lineno))
        if lf.id in pmap:
            proof = pmap[lf.id]
            subgoals = pc.admit_proposition(lf,proof)
            conjs.extend(subgoals)
        else:
            conjs.append(lf)

    # Convert uf's to arrays, if possible

    actions = [(x,uf_to_array_action(action)) for x,action in actions] 
    # for x,a in actions:
    #     print (a)

    init_action = uf_to_array_action(init_action)
    # print (init_action)
    conjs = [conj.clone([conj.label,uf_to_arr_ast(conj.formula)]) for conj in conjs]

    # Convert the global action and initializer to logic. Notice we
    # use 'action_to_state' to turn the initializer TR into a state
    # predicate (i.e., it's strongest post).
    
    actupds = [action_to_tr(mod,action,method) for x,action in actions]
    transs = [ilu.clauses_to_formula(a[1]) for a in actupds]
    trans = il.Or(*[fmla for fmla in transs]) if len(actupds) != 1 else transs[0]
    stvars = list(iu.unique(sym for a in actupds for sym in a[0]))
    istvars,init,ierror = tr.action_to_state(action_to_tr(mod,init_action,method))
    stvars = list(iu.unique(stvars+istvars))

    # funs = set()
    # for df in trans.defs:
    #     funs.update(ilu.used_symbols_ast(df.args[1]))
    # for fmla in trans.fmlas:
    #     funs.update(ilu.used_symbols_ast(fmla))
    # funs.update(ilu.used_symbols_ast(invariant))
    # funs = set(sym for sym in funs if  il.is_function_sort(sym.sort))

    # trans = ilu.clauses_to_formula(trans)
    init = ilu.clauses_to_formula(init)

    # print ('init: {}'.format(init))
    # print ('trans: {}'.format(trans))
    # for conj in conjs:
    #     print ('conj: {}'.format(conj))

    f = open("ivy.vmt", "w")
    for sym in ilu.used_symbols_asts([init,trans]+[lf.formula for lf in conjs]):
        if slvr.solver_name(sym) is not None:
            decl = slvr.symbol_to_z3(sym)
            if il.is_constant(sym):
                if not il.is_interpreted_symbol(sym):
                    f.write ('(declare-const {} {})'.format(decl.sexpr(),decl.sort().sexpr()) + '\n')
            else:
                f.write (decl.sexpr() + '\n')
    ctr = 0
    for sym in ilu.used_symbols_asts([init,trans]):
        if tr.is_new(sym):
            decl = slvr.symbol_to_z3(sym)
            declc = slvr.symbol_to_z3(tr.new_of(sym))
            f.write ('(declare-fun $sv.{} () {} (! {} :next {}))\n'
                   .format(ctr,decl.sort().sexpr(),declc.sexpr(),decl.sexpr()))
            ctr += 1
    f.write ('(define-fun $init () Bool (!\n{} :init true))\n'
           .format(slvr.formula_to_z3(init).sexpr()))
    f.write ('(define-fun $trans () Bool (!\n{} :trans true))\n'
           .format(slvr.formula_to_z3(trans).sexpr()))
    ctr = 1
    for lf in conjs:
        f.write ('(define-fun {} () Bool (!\n{} :invar-property {}))\n'
               .format(lf.label,slvr.formula_to_z3(lf.formula).sexpr(),ctr))
        ctr += 1
    
    f.close()    

    print('output written to ivy.vmt')
    exit(0)
            
    return None


                          
