#define _HAS_ITERATOR_DEBUGGING 0
struct ivy_gen {virtual int choose(int rng,const char *name) = 0;};
#include "z3++.h"

/*++
  Copyright (c) Microsoft Corporation

  This hash template is borrowed from Microsoft Z3
  (https://github.com/Z3Prover/z3).

  Simple implementation of bucket-list hash tables conforming roughly
  to SGI hash_map and hash_set interfaces, though not all members are
  implemented.

  These hash tables have the property that insert preserves iterators
  and references to elements.

  This package lives in namespace hash_space. Specializations of
  class "hash" should be made in this namespace.

  --*/

#pragma once

#ifndef HASH_H
#define HASH_H

#ifdef _WINDOWS
#pragma warning(disable:4267)
#endif

#include <string>
#include <vector>
#include <map>
#include <iterator>
#include <fstream>

namespace hash_space {

    unsigned string_hash(const char * str, unsigned length, unsigned init_value);

    template <typename T> class hash {
    public:
        size_t operator()(const T &s) const {
            return s.__hash();
        }
    };

    template <>
        class hash<int> {
    public:
        size_t operator()(const int &s) const {
            return s;
        }
    };

    template <>
        class hash<long long> {
    public:
        size_t operator()(const long long &s) const {
            return s;
        }
    };

    template <>
        class hash<unsigned> {
    public:
        size_t operator()(const unsigned &s) const {
            return s;
        }
    };

    template <>
        class hash<unsigned long long> {
    public:
        size_t operator()(const unsigned long long &s) const {
            return s;
        }
    };

    template <>
        class hash<bool> {
    public:
        size_t operator()(const bool &s) const {
            return s;
        }
    };

    template <>
        class hash<std::string> {
    public:
        size_t operator()(const std::string &s) const {
            return string_hash(s.c_str(), (unsigned)s.size(), 0);
        }
    };

    template <>
        class hash<std::pair<int,int> > {
    public:
        size_t operator()(const std::pair<int,int> &p) const {
            return p.first + p.second;
        }
    };

    template <typename T>
        class hash<std::vector<T> > {
    public:
        size_t operator()(const std::vector<T> &p) const {
            hash<T> h;
            size_t res = 0;
            for (unsigned i = 0; i < p.size(); i++)
                res += h(p[i]);
            return res;
        }
    };

    template <typename K, typename V>
        class hash<std::map<K,V> > {
    public:
        size_t operator()(const std::map<K,V> &p) const {
            hash<K> hk;
            hash<V> hv;
            size_t res = 0;
            for (typename std::map<K,V>::const_iterator it = p.begin(), en = p.end(); it != en; ++it)
                res += hk(it->first) + hv(it->second);
            return res;
        }
    };

    template <class T>
        class hash<std::pair<T *, T *> > {
    public:
        size_t operator()(const std::pair<T *,T *> &p) const {
            return (size_t)p.first + (size_t)p.second;
        }
    };

    template <class T>
        class hash<T *> {
    public:
        size_t operator()(T * const &p) const {
            return (size_t)p;
        }
    };

    enum { num_primes = 29 };

    static const unsigned long primes[num_primes] =
        {
            7ul,
            53ul,
            97ul,
            193ul,
            389ul,
            769ul,
            1543ul,
            3079ul,
            6151ul,
            12289ul,
            24593ul,
            49157ul,
            98317ul,
            196613ul,
            393241ul,
            786433ul,
            1572869ul,
            3145739ul,
            6291469ul,
            12582917ul,
            25165843ul,
            50331653ul,
            100663319ul,
            201326611ul,
            402653189ul,
            805306457ul,
            1610612741ul,
            3221225473ul,
            4294967291ul
        };

    inline unsigned long next_prime(unsigned long n) {
        const unsigned long* to = primes + (int)num_primes;
        for(const unsigned long* p = primes; p < to; p++)
            if(*p >= n) return *p;
        return primes[num_primes-1];
    }

    template<class Value, class Key, class HashFun, class GetKey, class KeyEqFun>
        class hashtable
    {
    public:

        typedef Value &reference;
        typedef const Value &const_reference;
    
        struct Entry
        {
            Entry* next;
            Value val;
      
        Entry(const Value &_val) : val(_val) {next = 0;}
        };
    

        struct iterator
        {      
            Entry* ent;
            hashtable* tab;

            typedef std::forward_iterator_tag iterator_category;
            typedef Value value_type;
            typedef std::ptrdiff_t difference_type;
            typedef size_t size_type;
            typedef Value& reference;
            typedef Value* pointer;

        iterator(Entry* _ent, hashtable* _tab) : ent(_ent), tab(_tab) { }

            iterator() { }

            Value &operator*() const { return ent->val; }

            Value *operator->() const { return &(operator*()); }

            iterator &operator++() {
                Entry *old = ent;
                ent = ent->next;
                if (!ent) {
                    size_t bucket = tab->get_bucket(old->val);
                    while (!ent && ++bucket < tab->buckets.size())
                        ent = tab->buckets[bucket];
                }
                return *this;
            }

            iterator operator++(int) {
                iterator tmp = *this;
                operator++();
                return tmp;
            }


            bool operator==(const iterator& it) const { 
                return ent == it.ent;
            }

            bool operator!=(const iterator& it) const {
                return ent != it.ent;
            }
        };

        struct const_iterator
        {      
            const Entry* ent;
            const hashtable* tab;

            typedef std::forward_iterator_tag iterator_category;
            typedef Value value_type;
            typedef std::ptrdiff_t difference_type;
            typedef size_t size_type;
            typedef const Value& reference;
            typedef const Value* pointer;

        const_iterator(const Entry* _ent, const hashtable* _tab) : ent(_ent), tab(_tab) { }

            const_iterator() { }

            const Value &operator*() const { return ent->val; }

            const Value *operator->() const { return &(operator*()); }

            const_iterator &operator++() {
                const Entry *old = ent;
                ent = ent->next;
                if (!ent) {
                    size_t bucket = tab->get_bucket(old->val);
                    while (!ent && ++bucket < tab->buckets.size())
                        ent = tab->buckets[bucket];
                }
                return *this;
            }

            const_iterator operator++(int) {
                const_iterator tmp = *this;
                operator++();
                return tmp;
            }


            bool operator==(const const_iterator& it) const { 
                return ent == it.ent;
            }

            bool operator!=(const const_iterator& it) const {
                return ent != it.ent;
            }
        };

    private:

        typedef std::vector<Entry*> Table;

        Table buckets;
        size_t entries;
        HashFun hash_fun ;
        GetKey get_key;
        KeyEqFun key_eq_fun;
    
    public:

    hashtable(size_t init_size) : buckets(init_size,(Entry *)0) {
            entries = 0;
        }
    
        hashtable(const hashtable& other) {
            dup(other);
        }

        hashtable& operator= (const hashtable& other) {
            if (&other != this)
                dup(other);
            return *this;
        }

        ~hashtable() {
            clear();
        }

        size_t size() const { 
            return entries;
        }

        bool empty() const { 
            return size() == 0;
        }

        void swap(hashtable& other) {
            buckets.swap(other.buckets);
            std::swap(entries, other.entries);
        }
    
        iterator begin() {
            for (size_t i = 0; i < buckets.size(); ++i)
                if (buckets[i])
                    return iterator(buckets[i], this);
            return end();
        }
    
        iterator end() { 
            return iterator(0, this);
        }

        const_iterator begin() const {
            for (size_t i = 0; i < buckets.size(); ++i)
                if (buckets[i])
                    return const_iterator(buckets[i], this);
            return end();
        }
    
        const_iterator end() const { 
            return const_iterator(0, this);
        }
    
        size_t get_bucket(const Value& val, size_t n) const {
            return hash_fun(get_key(val)) % n;
        }
    
        size_t get_key_bucket(const Key& key) const {
            return hash_fun(key) % buckets.size();
        }

        size_t get_bucket(const Value& val) const {
            return get_bucket(val,buckets.size());
        }

        Entry *lookup(const Value& val, bool ins = false)
        {
            resize(entries + 1);

            size_t n = get_bucket(val);
            Entry* from = buckets[n];
      
            for (Entry* ent = from; ent; ent = ent->next)
                if (key_eq_fun(get_key(ent->val), get_key(val)))
                    return ent;
      
            if(!ins) return 0;

            Entry* tmp = new Entry(val);
            tmp->next = from;
            buckets[n] = tmp;
            ++entries;
            return tmp;
        }

        Entry *lookup_key(const Key& key) const
        {
            size_t n = get_key_bucket(key);
            Entry* from = buckets[n];
      
            for (Entry* ent = from; ent; ent = ent->next)
                if (key_eq_fun(get_key(ent->val), key))
                    return ent;
      
            return 0;
        }

        const_iterator find(const Key& key) const {
            return const_iterator(lookup_key(key),this);
        }

        iterator find(const Key& key) {
            return iterator(lookup_key(key),this);
        }

        std::pair<iterator,bool> insert(const Value& val){
            size_t old_entries = entries;
            Entry *ent = lookup(val,true);
            return std::pair<iterator,bool>(iterator(ent,this),entries > old_entries);
        }
    
        iterator insert(const iterator &it, const Value& val){
            Entry *ent = lookup(val,true);
            return iterator(ent,this);
        }

        size_t erase(const Key& key)
        {
            Entry** p = &(buckets[get_key_bucket(key)]);
            size_t count = 0;
            while(*p){
                Entry *q = *p;
                if (key_eq_fun(get_key(q->val), key)) {
                    ++count;
                    *p = q->next;
                    delete q;
                }
                else
                    p = &(q->next);
            }
            entries -= count;
            return count;
        }

        void resize(size_t new_size) {
            const size_t old_n = buckets.size();
            if (new_size <= old_n) return;
            const size_t n = next_prime(new_size);
            if (n <= old_n) return;
            Table tmp(n, (Entry*)(0));
            for (size_t i = 0; i < old_n; ++i) {
                Entry* ent = buckets[i];
                while (ent) {
                    size_t new_bucket = get_bucket(ent->val, n);
                    buckets[i] = ent->next;
                    ent->next = tmp[new_bucket];
                    tmp[new_bucket] = ent;
                    ent = buckets[i];
                }
            }
            buckets.swap(tmp);
        }
    
        void clear()
        {
            for (size_t i = 0; i < buckets.size(); ++i) {
                for (Entry* ent = buckets[i]; ent != 0;) {
                    Entry* next = ent->next;
                    delete ent;
                    ent = next;
                }
                buckets[i] = 0;
            }
            entries = 0;
        }

        void dup(const hashtable& other)
        {
            clear();
            buckets.resize(other.buckets.size());
            for (size_t i = 0; i < other.buckets.size(); ++i) {
                Entry** to = &buckets[i];
                for (Entry* from = other.buckets[i]; from; from = from->next)
                    to = &((*to = new Entry(from->val))->next);
            }
            entries = other.entries;
        }
    };

    template <typename T> 
        class equal {
    public:
        bool operator()(const T& x, const T &y) const {
            return x == y;
        }
    };

    template <typename T>
        class identity {
    public:
        const T &operator()(const T &x) const {
            return x;
        }
    };

    template <typename T, typename U>
        class proj1 {
    public:
        const T &operator()(const std::pair<T,U> &x) const {
            return x.first;
        }
    };

    template <typename Element, class HashFun = hash<Element>, 
        class EqFun = equal<Element> >
        class hash_set
        : public hashtable<Element,Element,HashFun,identity<Element>,EqFun> {

    public:

    typedef Element value_type;

    hash_set()
    : hashtable<Element,Element,HashFun,identity<Element>,EqFun>(7) {}
    };

    template <typename Key, typename Value, class HashFun = hash<Key>, 
        class EqFun = equal<Key> >
        class hash_map
        : public hashtable<std::pair<Key,Value>,Key,HashFun,proj1<Key,Value>,EqFun> {

    public:

    hash_map()
    : hashtable<std::pair<Key,Value>,Key,HashFun,proj1<Key,Value>,EqFun>(7) {}

    Value &operator[](const Key& key) {
	std::pair<Key,Value> kvp(key,Value());
	return 
	hashtable<std::pair<Key,Value>,Key,HashFun,proj1<Key,Value>,EqFun>::
        lookup(kvp,true)->val.second;
    }
    };

    template <typename D,typename R>
        class hash<hash_map<D,R> > {
    public:
        size_t operator()(const hash_map<D,R> &p) const {
            hash<D > h1;
            hash<R > h2;
            size_t res = 0;
            
            for (typename hash_map<D,R>::const_iterator it=p.begin(), en=p.end(); it!=en; ++it)
                res += (h1(it->first)+h2(it->second));
            return res;
        }
    };

    template <typename D,typename R>
    inline bool operator ==(const hash_map<D,R> &s, const hash_map<D,R> &t){
        for (typename hash_map<D,R>::const_iterator it=s.begin(), en=s.end(); it!=en; ++it) {
            typename hash_map<D,R>::const_iterator it2 = t.find(it->first);
            if (it2 == t.end() || !(it->second == it2->second)) return false;
        }
        for (typename hash_map<D,R>::const_iterator it=t.begin(), en=t.end(); it!=en; ++it) {
            typename hash_map<D,R>::const_iterator it2 = s.find(it->first);
            if (it2 == t.end() || !(it->second == it2->second)) return false;
        }
        return true;
    }
}
#endif
typedef std::string __strlit;
extern std::ofstream __ivy_out;
void __ivy_exit(int);
#include <inttypes.h>
#include <math.h>
typedef __int128_t int128_t;
typedef __uint128_t uint128_t;
#include <signal.h>
#include <chrono> 
int call_generating = 1;

template <typename D, typename R>
struct thunk {
    virtual R operator()(const D &) = 0;
    int ___ivy_choose(int rng,const char *name,int id) {
        return 0;
    }
};
template <typename D, typename R, class HashFun = hash_space::hash<D> >
struct hash_thunk {
    thunk<D,R> *fun;
    hash_space::hash_map<D,R,HashFun> memo;
    hash_thunk() : fun(0) {}
    hash_thunk(thunk<D,R> *fun) : fun(fun) {}
    ~hash_thunk() {
//        if (fun)
//            delete fun;
    }
    R &operator[](const D& arg){
        std::pair<typename hash_space::hash_map<D,R>::iterator,bool> foo = memo.insert(std::pair<D,R>(arg,R()));
        R &res = foo.first->second;
        if (foo.second && fun)
            res = (*fun)(arg);
        return res;
    }
};

    //class ivy_binary_ser;
    //class ivy_binary_deser;
    class ivy_binary_ser_128;
    class ivy_binary_deser_128;



        class ivy_binary_ser;
        class ivy_binary_deser;

    
    extern "C" {
    #ifdef _WIN32
    #include "picotls/wincompat.h"
    #endif
    #include "picotls.h"
    //#include "picotls.c"
    #include "picotls/openssl.h"
    #include "picotls/minicrypto.h"
    //#include <fmt/core.h>
    }

    #include <openssl/pem.h>

    // TODO: put any forward class definitions here

    class tls_callbacks;
    class picotls_connection;



    #include <list>
    #ifndef _WIN32
    #include <netinet/udp.h>
    #include <semaphore.h>
	#include <arpa/inet.h>
	#include <sys/ioctl.h>
	#include <net/if.h>
	#include <linux/if_packet.h>
	#include <linux/if_ether.h>
	#include <netinet/ip.h>
	#include <netinet/tcp.h>
	#include <iomanip>
#include <iostream>

    #endif

    class udp_listener;   // class of threads that listen for connections
    class udp_callbacks;  // class holding callbacks to ivy

    // A udp_config maps endpoint ids to IP addresses and ports.





	#include "time.h"
	#include <sys/time.h>
	#include <unordered_map>

	class CTimeMeasuring;

	
	#include <chrono>
	#include <unordered_map>
	using namespace std::chrono;

	class ChronoTimeMeasuring;

	

    class reader;
    class timer;


        struct LongClass {
            LongClass() : val(0) {}
            LongClass(int128_t val) : val(val) {}
            int128_t val;
            int128_t __hash() const {return val;}
        };
        
	std::ostream& operator<<(std::ostream&s, const LongClass &v) {
		std::ostream::sentry ss( s ); 
		if ( ss ) { 
		   __int128_t value = v.val; 
		   //https://stackoverflow.com/questions/25114597/how-to-print-int128-in-g 
		   __uint128_t tmp = value < 0 ? -value : value; 
		   char buffer[ 128 ]; 
		   char* d = std::end( buffer ); 
		   do 
		   { 
		     -- d; 
		     *d = "0123456789"[ tmp % 10 ]; 
		     tmp /= 10; 
		   } while ( tmp != 0 ); 
		   if ( value < 0 ) { 
		      -- d; 
		      *d = '-'; 
		   } 
		   int len = std::end( buffer ) - d; 
		   if ( s.rdbuf()->sputn( d, len ) != len ) { 
		      s.setstate( std::ios_base::badbit ); 
		    } 
	    } 
	    return s; 
	}
    std::istream& operator>>(std::istream& is, LongClass& x) {
        x.val = 0;
        std::string s;
        is >> s;
        int n = int(s.size());
        int it = 0;
        if (s[0] == '-') it++;
        for (; it < n; it++) x.val = (x.val * 10 + s[it] - '0');
        if (s[0] == '-') x.val = -x.val;
        return is;
    }
	bool operator==(const LongClass &x, const LongClass &y) {return x.val == y.val;}
class quic_server_test_stream {
  public:
    typedef quic_server_test_stream ivy_class;

    std::vector<std::string> __argv;
#ifdef _WIN32
    void *mutex;  // forward reference to HANDLE
#else
    pthread_mutex_t mutex;
#endif
    void __lock();
    void __unlock();

#ifdef _WIN32
    std::vector<HANDLE> thread_ids;

#else
    std::vector<pthread_t> thread_ids;

#endif
    void install_reader(reader *);
    void install_thread(reader *);
    void install_timer(timer *);
    virtual ~quic_server_test_stream();
    std::vector<int> ___ivy_stack;
    ivy_gen *___ivy_gen;
    int ___ivy_choose(int rng,const char *name,int id);
    virtual void ivy_assert(bool,const char *){}
    virtual void ivy_assume(bool,const char *){}
    virtual void ivy_check_progress(int,int){}
class cid : public LongClass {
public:
    
    cid(){}
    cid(const LongClass &s) : LongClass(s) {}
    cid(int128_t v) : LongClass(v) {}
    size_t __hash() const { return hash_space::hash<LongClass>()(*this); }
    #ifdef Z3PP_H_
    static z3::sort z3_sort(z3::context &ctx) {return ctx.bv_sort(20);}
    static hash_space::hash_map<LongClass,int> x_to_bv_hash;
    static hash_space::hash_map<int,LongClass> bv_to_x_hash;
    static int next_bv;
    static std::vector<LongClass> nonces;
    static LongClass random_x();
    static int x_to_bv(const LongClass &s){
        if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
            for (; next_bv < (1<<20); next_bv++) {
                if(bv_to_x_hash.find(next_bv) == bv_to_x_hash.end()) {
                    x_to_bv_hash[s] = next_bv;
                    bv_to_x_hash[next_bv] = s;
    		//std::cerr << "bv_to_x_hash[next_bv]" << s << std::endl;
                    return next_bv++;
                } 
            }
            std::cerr << "Ran out of values for type cid" << std::endl;
            __ivy_out << "out_of_values(cid,\"" << s << "\")" << std::endl;
            for (int i = 0; i < (1<<20); i++)
                __ivy_out << "value(\"" << bv_to_x_hash[i] << "\")" << std::endl;
            __ivy_exit(1);
        }
        return x_to_bv_hash[s];
    }
    static LongClass bv_to_x(int bv){
        if(bv_to_x_hash.find(bv) == bv_to_x_hash.end()){
            int num = 0;
            while (true) {
                // std::ostringstream str;
                // str << num;
                // LongClass s = str.str();
                LongClass s = random_x();
                if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
                   x_to_bv_hash[s] = bv;
                   bv_to_x_hash[bv] = s;
    	       //sstd::cerr << "bv_to_x_hash: " << s << std::endl;
                   return s;
                }
                num++;
            }
        }
        //std::cerr << "bv_to_x_hash: " << bv_to_x_hash[bv] << std::endl;
        return bv_to_x_hash[bv];
    }
    static void prepare() {}
    static void cleanup() {
        x_to_bv_hash.clear();
        bv_to_x_hash.clear();
        next_bv = 0;
    }
    #endif
};class itoken : public LongClass {
public:
    
    itoken(){}
    itoken(const LongClass &s) : LongClass(s) {}
    itoken(int128_t v) : LongClass(v) {}
    size_t __hash() const { return hash_space::hash<LongClass>()(*this); }
    #ifdef Z3PP_H_
    static z3::sort z3_sort(z3::context &ctx) {return ctx.bv_sort(16);}
    static hash_space::hash_map<LongClass,int> x_to_bv_hash;
    static hash_space::hash_map<int,LongClass> bv_to_x_hash;
    static int next_bv;
    static std::vector<LongClass> nonces;
    static LongClass random_x();
    static int x_to_bv(const LongClass &s){
        if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
            for (; next_bv < (1<<16); next_bv++) {
                if(bv_to_x_hash.find(next_bv) == bv_to_x_hash.end()) {
                    x_to_bv_hash[s] = next_bv;
                    bv_to_x_hash[next_bv] = s;
    		//std::cerr << "bv_to_x_hash[next_bv]" << s << std::endl;
                    return next_bv++;
                } 
            }
            std::cerr << "Ran out of values for type itoken" << std::endl;
            __ivy_out << "out_of_values(itoken,\"" << s << "\")" << std::endl;
            for (int i = 0; i < (1<<16); i++)
                __ivy_out << "value(\"" << bv_to_x_hash[i] << "\")" << std::endl;
            __ivy_exit(1);
        }
        return x_to_bv_hash[s];
    }
    static LongClass bv_to_x(int bv){
        if(bv_to_x_hash.find(bv) == bv_to_x_hash.end()){
            int num = 0;
            while (true) {
                // std::ostringstream str;
                // str << num;
                // LongClass s = str.str();
                LongClass s = random_x();
                if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
                   x_to_bv_hash[s] = bv;
                   bv_to_x_hash[bv] = s;
    	       //sstd::cerr << "bv_to_x_hash: " << s << std::endl;
                   return s;
                }
                num++;
            }
        }
        //std::cerr << "bv_to_x_hash: " << bv_to_x_hash[bv] << std::endl;
        return bv_to_x_hash[bv];
    }
    static void prepare() {}
    static void cleanup() {
        x_to_bv_hash.clear();
        bv_to_x_hash.clear();
        next_bv = 0;
    }
    #endif
};    enum stream_kind{unidir,bidir};
    enum role{role__client,role__server};
    enum quic_packet_type{quic_packet_type__initial,quic_packet_type__zero_rtt,quic_packet_type__handshake,quic_packet_type__one_rtt,quic_packet_type__version_negociation,quic_packet_type__retry};
    class bytes : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class stream_data : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
class tls__handshake{
public:
    struct wrap {
    
        virtual wrap *dup() = 0;
        virtual bool deref() = 0;
        virtual ~wrap() {}
    };
    
    template <typename T> struct twrap : public wrap {
    
        unsigned refs;
    
        T item;
    
        twrap(const T &item) : refs(1), item(item) {}
    
        virtual wrap *dup() {refs++; return this;}
    
        virtual bool deref() {return (--refs) != 0;}
    
    };
    
    int tag;
    
    wrap *ptr;
    
    tls__handshake(){
    tag=-1;
    ptr=0;
    }
    
    tls__handshake(int tag,wrap *ptr) : tag(tag),ptr(ptr) {}
    
    tls__handshake(const tls__handshake&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
    };
    
    tls__handshake& operator=(const tls__handshake&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
        return *this;
    };
    
    ~tls__handshake(){if(ptr){if (!ptr->deref()) delete ptr;}}
    
    static int temp_counter;
    
    static void prepare() {temp_counter = 0;}
    
    static void cleanup() {}
    
    size_t __hash() const {
    
        switch(tag) {
    
            case 0: return 0 + hash_space::hash<quic_server_test_stream::tls__client_hello>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__client_hello >((*this)));
    
            case 1: return 1 + hash_space::hash<quic_server_test_stream::tls__server_hello>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__server_hello >((*this)));
    
            case 2: return 2 + hash_space::hash<quic_server_test_stream::tls__new_session_ticket>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__new_session_ticket >((*this)));
    
            case 3: return 3 + hash_space::hash<quic_server_test_stream::tls__encrypted_extensions>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__encrypted_extensions >((*this)));
    
            case 4: return 4 + hash_space::hash<quic_server_test_stream::tls__unknown_message>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__unknown_message >((*this)));
    
            case 5: return 5 + hash_space::hash<quic_server_test_stream::tls__finished>()(quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__finished >((*this)));
    
        }
    
        return 0;
    
    }
    
    template <typename T> static const T &unwrap(const tls__handshake &x) {
    
        return ((static_cast<const twrap<T> *>(x.ptr))->item);
    
    }
    
    template <typename T> static T &unwrap(tls__handshake &x) {
    
         twrap<T> *p = static_cast<twrap<T> *>(x.ptr);
    
         if (p->refs > 1) {
    
             p = new twrap<T> (p->item);
    
         }
    
         return ((static_cast<twrap<T> *>(p))->item);
    
    }
    
};class tls__extension{
public:
    struct wrap {
    
        virtual wrap *dup() = 0;
        virtual bool deref() = 0;
        virtual ~wrap() {}
    };
    
    template <typename T> struct twrap : public wrap {
    
        unsigned refs;
    
        T item;
    
        twrap(const T &item) : refs(1), item(item) {}
    
        virtual wrap *dup() {refs++; return this;}
    
        virtual bool deref() {return (--refs) != 0;}
    
    };
    
    int tag;
    
    wrap *ptr;
    
    tls__extension(){
    tag=-1;
    ptr=0;
    }
    
    tls__extension(int tag,wrap *ptr) : tag(tag),ptr(ptr) {}
    
    tls__extension(const tls__extension&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
    };
    
    tls__extension& operator=(const tls__extension&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
        return *this;
    };
    
    ~tls__extension(){if(ptr){if (!ptr->deref()) delete ptr;}}
    
    static int temp_counter;
    
    static void prepare() {temp_counter = 0;}
    
    static void cleanup() {}
    
    size_t __hash() const {
    
        switch(tag) {
    
            case 0: return 0 + hash_space::hash<quic_server_test_stream::tls__unknown_extension>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__unknown_extension >((*this)));
    
            case 1: return 1 + hash_space::hash<quic_server_test_stream::tls__early_data>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__early_data >((*this)));
    
            case 2: return 2 + hash_space::hash<quic_server_test_stream::tls__end_of_early_data>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__end_of_early_data >((*this)));
    
            case 3: return 3 + hash_space::hash<quic_server_test_stream::tls__psk_key_exchange_modes>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__psk_key_exchange_modes >((*this)));
    
            case 4: return 4 + hash_space::hash<quic_server_test_stream::tls__pre_shared_key_client>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_client >((*this)));
    
            case 5: return 5 + hash_space::hash<quic_server_test_stream::tls__pre_shared_key_server>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_server >((*this)));
    
            case 6: return 6 + hash_space::hash<quic_server_test_stream::quic_transport_parameters>()(quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::quic_transport_parameters >((*this)));
    
        }
    
        return 0;
    
    }
    
    template <typename T> static const T &unwrap(const tls__extension &x) {
    
        return ((static_cast<const twrap<T> *>(x.ptr))->item);
    
    }
    
    template <typename T> static T &unwrap(tls__extension &x) {
    
         twrap<T> *p = static_cast<twrap<T> *>(x.ptr);
    
         if (p->refs > 1) {
    
             p = new twrap<T> (p->item);
    
         }
    
         return ((static_cast<twrap<T> *>(p))->item);
    
    }
    
};    struct tls__unknown_extension {
    unsigned etype;
    stream_data content;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(etype);
hv += hash_space::hash<stream_data>()(content);
return hv;
}
    };
    struct tls__early_data {
    unsigned long long max_early_data_size;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(max_early_data_size);
return hv;
}
    };
    struct tls__end_of_early_data {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct tls__psk_key_exchange_modes {
    stream_data content;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<stream_data>()(content);
return hv;
}
    };
    struct tls__psk_identity {
    stream_data identity;
    unsigned long long obfuscated_ticket_age;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<stream_data>()(identity);
hv += hash_space::hash<unsigned long long>()(obfuscated_ticket_age);
return hv;
}
    };
    class vector__tls__psk_identity__ : public std::vector<tls__psk_identity>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__psk_identity> >()(*this);};
    };
    struct tls__pre_shared_key_client {
    vector__tls__psk_identity__ psk_identities;
    stream_data psk_binder;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<vector__tls__psk_identity__>()(psk_identities);
hv += hash_space::hash<stream_data>()(psk_binder);
return hv;
}
    };
    struct tls__pre_shared_key_server {
    unsigned long long selected_identity;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(selected_identity);
return hv;
}
    };
    struct tls__random {
    unsigned gmt_unix_time;
    stream_data random_bytes;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(gmt_unix_time);
hv += hash_space::hash<stream_data>()(random_bytes);
return hv;
}
    };
    class vector__tls__cipher_suite__ : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class vector__tls__compression_method__ : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class vector__tls__extension__ : public std::vector<tls__extension>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__extension> >()(*this);};
    };
    struct tls__client_hello {
    unsigned client_version;
    tls__random rand_info;
    stream_data session_id;
    vector__tls__cipher_suite__ cipher_suites;
    vector__tls__compression_method__ compression_methods;
    vector__tls__extension__ extensions;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(client_version);
hv += hash_space::hash<tls__random>()(rand_info);
hv += hash_space::hash<stream_data>()(session_id);
hv += hash_space::hash<vector__tls__cipher_suite__>()(cipher_suites);
hv += hash_space::hash<vector__tls__compression_method__>()(compression_methods);
hv += hash_space::hash<vector__tls__extension__>()(extensions);
return hv;
}
    };
    struct tls__server_hello {
    unsigned server_version;
    tls__random rand_info;
    stream_data session_id;
    unsigned the_cipher_suite;
    unsigned the_compression_method;
    vector__tls__extension__ extensions;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(server_version);
hv += hash_space::hash<tls__random>()(rand_info);
hv += hash_space::hash<stream_data>()(session_id);
hv += hash_space::hash<unsigned>()(the_cipher_suite);
hv += hash_space::hash<unsigned>()(the_compression_method);
hv += hash_space::hash<vector__tls__extension__>()(extensions);
return hv;
}
    };
    struct tls__new_session_ticket {
    unsigned long long ticket_lifetime;
    unsigned long long ticket_age_add;
    stream_data ticket_nonce;
    stream_data ticket;
    vector__tls__extension__ extensions;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(ticket_lifetime);
hv += hash_space::hash<unsigned long long>()(ticket_age_add);
hv += hash_space::hash<stream_data>()(ticket_nonce);
hv += hash_space::hash<stream_data>()(ticket);
hv += hash_space::hash<vector__tls__extension__>()(extensions);
return hv;
}
    };
    struct tls__encrypted_extensions {
    vector__tls__extension__ extensions;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<vector__tls__extension__>()(extensions);
return hv;
}
    };
    struct tls__unknown_message {
    unsigned mtype;
    stream_data unknown_message_bytes;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(mtype);
hv += hash_space::hash<stream_data>()(unknown_message_bytes);
return hv;
}
    };
    struct tls__finished {
    unsigned mtype;
    stream_data unknown_message_bytes;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(mtype);
hv += hash_space::hash<stream_data>()(unknown_message_bytes);
return hv;
}
    };
    class vector__tls__handshake__ : public std::vector<tls__handshake>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__handshake> >()(*this);};
    };
    enum ip__protocol{ip__udp,ip__tcp};
    enum ip__interface{ip__lo,ip__ivy,ip__ivy_client,ip__ivy_server,ip__veth_ivy};
    struct ip__endpoint {
    ip__protocol protocol;
    unsigned addr;
    unsigned port;
    ip__interface interface;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(protocol);
hv += hash_space::hash<unsigned>()(addr);
hv += hash_space::hash<unsigned>()(port);
hv += hash_space::hash<int>()(interface);
return hv;
}
    };
    class tls__handshakes : public std::vector<tls__handshake>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__handshake> >()(*this);};
    };
    struct tls__handshake_parser__result {
    unsigned long long pos;
    tls__handshakes value;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(pos);
hv += hash_space::hash<tls__handshakes>()(value);
return hv;
}
    };
class frame{
public:
    struct wrap {
    
        virtual wrap *dup() = 0;
        virtual bool deref() = 0;
        virtual ~wrap() {}
    };
    
    template <typename T> struct twrap : public wrap {
    
        unsigned refs;
    
        T item;
    
        twrap(const T &item) : refs(1), item(item) {}
    
        virtual wrap *dup() {refs++; return this;}
    
        virtual bool deref() {return (--refs) != 0;}
    
    };
    
    int tag;
    
    wrap *ptr;
    
    frame(){
    tag=-1;
    ptr=0;
    }
    
    frame(int tag,wrap *ptr) : tag(tag),ptr(ptr) {}
    
    frame(const frame&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
    };
    
    frame& operator=(const frame&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
        return *this;
    };
    
    ~frame(){if(ptr){if (!ptr->deref()) delete ptr;}}
    
    static int temp_counter;
    
    static void prepare() {temp_counter = 0;}
    
    static void cleanup() {}
    
    size_t __hash() const {
    
        switch(tag) {
    
            case 0: return 0 + hash_space::hash<quic_server_test_stream::frame__ping>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ping >((*this)));
    
            case 1: return 1 + hash_space::hash<quic_server_test_stream::frame__ack>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack >((*this)));
    
            case 2: return 2 + hash_space::hash<quic_server_test_stream::frame__ack_ecn>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_ecn >((*this)));
    
            case 3: return 3 + hash_space::hash<quic_server_test_stream::frame__rst_stream>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__rst_stream >((*this)));
    
            case 4: return 4 + hash_space::hash<quic_server_test_stream::frame__stop_sending>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stop_sending >((*this)));
    
            case 5: return 5 + hash_space::hash<quic_server_test_stream::frame__crypto>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__crypto >((*this)));
    
            case 6: return 6 + hash_space::hash<quic_server_test_stream::frame__new_token>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_token >((*this)));
    
            case 7: return 7 + hash_space::hash<quic_server_test_stream::frame__stream>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream >((*this)));
    
            case 8: return 8 + hash_space::hash<quic_server_test_stream::frame__max_data>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_data >((*this)));
    
            case 9: return 9 + hash_space::hash<quic_server_test_stream::frame__max_stream_data>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_stream_data >((*this)));
    
            case 10: return 10 + hash_space::hash<quic_server_test_stream::frame__max_streams>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams >((*this)));
    
            case 11: return 11 + hash_space::hash<quic_server_test_stream::frame__max_streams_bidi>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams_bidi >((*this)));
    
            case 12: return 12 + hash_space::hash<quic_server_test_stream::frame__data_blocked>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__data_blocked >((*this)));
    
            case 13: return 13 + hash_space::hash<quic_server_test_stream::frame__stream_data_blocked>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream_data_blocked >((*this)));
    
            case 14: return 14 + hash_space::hash<quic_server_test_stream::frame__streams_blocked>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked >((*this)));
    
            case 15: return 15 + hash_space::hash<quic_server_test_stream::frame__streams_blocked_bidi>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked_bidi >((*this)));
    
            case 16: return 16 + hash_space::hash<quic_server_test_stream::frame__new_connection_id>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_connection_id >((*this)));
    
            case 17: return 17 + hash_space::hash<quic_server_test_stream::frame__retire_connection_id>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__retire_connection_id >((*this)));
    
            case 18: return 18 + hash_space::hash<quic_server_test_stream::frame__path_challenge>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_challenge >((*this)));
    
            case 19: return 19 + hash_space::hash<quic_server_test_stream::frame__path_response>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_response >((*this)));
    
            case 20: return 20 + hash_space::hash<quic_server_test_stream::frame__connection_close>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__connection_close >((*this)));
    
            case 21: return 21 + hash_space::hash<quic_server_test_stream::frame__application_close>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__application_close >((*this)));
    
            case 22: return 22 + hash_space::hash<quic_server_test_stream::frame__handshake_done>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__handshake_done >((*this)));
    
            case 23: return 23 + hash_space::hash<quic_server_test_stream::frame__ack_frequency>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_frequency >((*this)));
    
            case 24: return 24 + hash_space::hash<quic_server_test_stream::frame__immediate_ack>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__immediate_ack >((*this)));
    
            case 25: return 25 + hash_space::hash<quic_server_test_stream::frame__unknown_frame>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__unknown_frame >((*this)));
    
            case 26: return 26 + hash_space::hash<quic_server_test_stream::frame__malicious_frame>()(quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__malicious_frame >((*this)));
    
        }
    
        return 0;
    
    }
    
    template <typename T> static const T &unwrap(const frame &x) {
    
        return ((static_cast<const twrap<T> *>(x.ptr))->item);
    
    }
    
    template <typename T> static T &unwrap(frame &x) {
    
         twrap<T> *p = static_cast<twrap<T> *>(x.ptr);
    
         if (p->refs > 1) {
    
             p = new twrap<T> (p->item);
    
         }
    
         return ((static_cast<twrap<T> *>(p))->item);
    
    }
    
};    struct frame__ping {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct frame__ack__range {
    unsigned gap;
    unsigned ranges;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(gap);
hv += hash_space::hash<unsigned>()(ranges);
return hv;
}
    };
    class frame__ack__range__arr : public std::vector<frame__ack__range>{
        public: size_t __hash() const { return hash_space::hash<std::vector<frame__ack__range> >()(*this);};
    };
    struct frame__ack {
    unsigned largest_acked;
    int ack_delay;
    frame__ack__range__arr ack_ranges;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(largest_acked);
hv += hash_space::hash<int>()(ack_delay);
hv += hash_space::hash<frame__ack__range__arr>()(ack_ranges);
return hv;
}
    };
    struct frame__ack_ecn__range {
    unsigned gap;
    unsigned ranges;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(gap);
hv += hash_space::hash<unsigned>()(ranges);
return hv;
}
    };
    class frame__ack_ecn__range__arr : public std::vector<frame__ack_ecn__range>{
        public: size_t __hash() const { return hash_space::hash<std::vector<frame__ack_ecn__range> >()(*this);};
    };
    struct frame__ack_ecn {
    unsigned largest_acked;
    int ack_delay;
    frame__ack_ecn__range__arr ack_ranges;
    bool ecnp;
    unsigned ect0;
    unsigned ect1;
    unsigned ecn_ce;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(largest_acked);
hv += hash_space::hash<int>()(ack_delay);
hv += hash_space::hash<frame__ack_ecn__range__arr>()(ack_ranges);
hv += hash_space::hash<bool>()(ecnp);
hv += hash_space::hash<unsigned>()(ect0);
hv += hash_space::hash<unsigned>()(ect1);
hv += hash_space::hash<unsigned>()(ecn_ce);
return hv;
}
    };
    struct frame__rst_stream {
    unsigned id;
    unsigned err_code;
    unsigned long long final_offset;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
hv += hash_space::hash<unsigned>()(err_code);
hv += hash_space::hash<unsigned long long>()(final_offset);
return hv;
}
    };
    struct frame__stop_sending {
    unsigned id;
    unsigned err_code;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
hv += hash_space::hash<unsigned>()(err_code);
return hv;
}
    };
    struct frame__crypto {
    unsigned long long offset;
    unsigned long long length;
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(offset);
hv += hash_space::hash<unsigned long long>()(length);
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    struct frame__new_token {
    unsigned long long length;
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(length);
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    struct frame__stream {
    bool off;
    bool len;
    bool fin;
    unsigned id;
    unsigned long long offset;
    unsigned long long length;
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<bool>()(off);
hv += hash_space::hash<bool>()(len);
hv += hash_space::hash<bool>()(fin);
hv += hash_space::hash<unsigned>()(id);
hv += hash_space::hash<unsigned long long>()(offset);
hv += hash_space::hash<unsigned long long>()(length);
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    struct frame__max_data {
    unsigned long long pos;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(pos);
return hv;
}
    };
    struct frame__max_stream_data {
    unsigned id;
    unsigned long long pos;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
hv += hash_space::hash<unsigned long long>()(pos);
return hv;
}
    };
    struct frame__max_streams {
    unsigned id;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
return hv;
}
    };
    struct frame__max_streams_bidi {
    unsigned id;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
return hv;
}
    };
    struct frame__data_blocked {
    unsigned long long pos;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(pos);
return hv;
}
    };
    struct frame__stream_data_blocked {
    unsigned id;
    unsigned long long pos;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(id);
hv += hash_space::hash<unsigned long long>()(pos);
return hv;
}
    };
    struct frame__streams_blocked {
    cid id;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(id);
return hv;
}
    };
    struct frame__streams_blocked_bidi {
    cid id;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(id);
return hv;
}
    };
    struct frame__new_connection_id {
    unsigned seq_num;
    unsigned retire_prior_to;
    unsigned length;
    cid scid;
    unsigned token;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<unsigned>()(retire_prior_to);
hv += hash_space::hash<unsigned>()(length);
hv += hash_space::hash<cid>()(scid);
hv += hash_space::hash<unsigned>()(token);
return hv;
}
    };
    struct frame__retire_connection_id {
    unsigned seq_num;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(seq_num);
return hv;
}
    };
    struct frame__path_challenge {
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    struct frame__path_response {
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    struct frame__connection_close {
    unsigned err_code;
    unsigned frame_type;
    unsigned long long reason_phrase_length;
    stream_data reason_phrase;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(err_code);
hv += hash_space::hash<unsigned>()(frame_type);
hv += hash_space::hash<unsigned long long>()(reason_phrase_length);
hv += hash_space::hash<stream_data>()(reason_phrase);
return hv;
}
    };
    struct frame__application_close {
    unsigned err_code;
    unsigned long long reason_phrase_length;
    stream_data reason_phrase;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(err_code);
hv += hash_space::hash<unsigned long long>()(reason_phrase_length);
hv += hash_space::hash<stream_data>()(reason_phrase);
return hv;
}
    };
    struct frame__handshake_done {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct frame__ack_frequency {
    unsigned seq_num;
    unsigned long long ack_eliciting_threshold;
    int request_max_ack_delay;
    unsigned long long reordering_threshold;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<unsigned long long>()(ack_eliciting_threshold);
hv += hash_space::hash<int>()(request_max_ack_delay);
hv += hash_space::hash<unsigned long long>()(reordering_threshold);
return hv;
}
    };
    struct frame__immediate_ack {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct frame__unknown_frame {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct frame__malicious_frame {
    stream_data data;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<stream_data>()(data);
return hv;
}
    };
    class frame__arr : public std::vector<frame>{
        public: size_t __hash() const { return hash_space::hash<std::vector<frame> >()(*this);};
    };
    class versions : public std::vector<stream_data>{
        public: size_t __hash() const { return hash_space::hash<std::vector<stream_data> >()(*this);};
    };
    class versions_bv : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct quic_packet_vn {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    versions_bv supported_version;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<versions_bv>()(supported_version);
return hv;
}
    };
    class quic_packet_vn__arr : public std::vector<quic_packet_vn>{
        public: size_t __hash() const { return hash_space::hash<std::vector<quic_packet_vn> >()(*this);};
    };
class ipv6__addr : public LongClass {
public:
    
    ipv6__addr(){}
    ipv6__addr(const LongClass &s) : LongClass(s) {}
    ipv6__addr(int128_t v) : LongClass(v) {}
    size_t __hash() const { return hash_space::hash<LongClass>()(*this); }
    #ifdef Z3PP_H_
    static z3::sort z3_sort(z3::context &ctx) {return ctx.bv_sort(3);}
    static hash_space::hash_map<LongClass,int> x_to_bv_hash;
    static hash_space::hash_map<int,LongClass> bv_to_x_hash;
    static int next_bv;
    static std::vector<LongClass> nonces;
    static LongClass random_x();
    static int x_to_bv(const LongClass &s){
        if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
            for (; next_bv < (1<<3); next_bv++) {
                if(bv_to_x_hash.find(next_bv) == bv_to_x_hash.end()) {
                    x_to_bv_hash[s] = next_bv;
                    bv_to_x_hash[next_bv] = s;
    		//std::cerr << "bv_to_x_hash[next_bv]" << s << std::endl;
                    return next_bv++;
                } 
            }
            std::cerr << "Ran out of values for type ipv6__addr" << std::endl;
            __ivy_out << "out_of_values(ipv6__addr,\"" << s << "\")" << std::endl;
            for (int i = 0; i < (1<<3); i++)
                __ivy_out << "value(\"" << bv_to_x_hash[i] << "\")" << std::endl;
            __ivy_exit(1);
        }
        return x_to_bv_hash[s];
    }
    static LongClass bv_to_x(int bv){
        if(bv_to_x_hash.find(bv) == bv_to_x_hash.end()){
            int num = 0;
            while (true) {
                // std::ostringstream str;
                // str << num;
                // LongClass s = str.str();
                LongClass s = random_x();
                if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
                   x_to_bv_hash[s] = bv;
                   bv_to_x_hash[bv] = s;
    	       //sstd::cerr << "bv_to_x_hash: " << s << std::endl;
                   return s;
                }
                num++;
            }
        }
        //std::cerr << "bv_to_x_hash: " << bv_to_x_hash[bv] << std::endl;
        return bv_to_x_hash[bv];
    }
    static void prepare() {}
    static void cleanup() {
        x_to_bv_hash.clear();
        bv_to_x_hash.clear();
        next_bv = 0;
    }
    #endif
};class transport_parameter{
public:
    struct wrap {
    
        virtual wrap *dup() = 0;
        virtual bool deref() = 0;
        virtual ~wrap() {}
    };
    
    template <typename T> struct twrap : public wrap {
    
        unsigned refs;
    
        T item;
    
        twrap(const T &item) : refs(1), item(item) {}
    
        virtual wrap *dup() {refs++; return this;}
    
        virtual bool deref() {return (--refs) != 0;}
    
    };
    
    int tag;
    
    wrap *ptr;
    
    transport_parameter(){
    tag=-1;
    ptr=0;
    }
    
    transport_parameter(int tag,wrap *ptr) : tag(tag),ptr(ptr) {}
    
    transport_parameter(const transport_parameter&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
    };
    
    transport_parameter& operator=(const transport_parameter&other){
        tag=other.tag;
        ptr = other.ptr ? other.ptr->dup() : 0;
        return *this;
    };
    
    ~transport_parameter(){if(ptr){if (!ptr->deref()) delete ptr;}}
    
    static int temp_counter;
    
    static void prepare() {temp_counter = 0;}
    
    static void cleanup() {}
    
    size_t __hash() const {
    
        switch(tag) {
    
            case 0: return 0 + hash_space::hash<quic_server_test_stream::original_destination_connection_id>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::original_destination_connection_id >((*this)));
    
            case 1: return 1 + hash_space::hash<quic_server_test_stream::initial_max_stream_data_bidi_local>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_local >((*this)));
    
            case 2: return 2 + hash_space::hash<quic_server_test_stream::initial_max_data>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_data >((*this)));
    
            case 3: return 3 + hash_space::hash<quic_server_test_stream::initial_max_stream_id_bidi>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_bidi >((*this)));
    
            case 4: return 4 + hash_space::hash<quic_server_test_stream::max_idle_timeout>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_idle_timeout >((*this)));
    
            case 5: return 5 + hash_space::hash<quic_server_test_stream::preferred_address>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::preferred_address >((*this)));
    
            case 6: return 6 + hash_space::hash<quic_server_test_stream::max_packet_size>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_packet_size >((*this)));
    
            case 7: return 7 + hash_space::hash<quic_server_test_stream::stateless_reset_token>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::stateless_reset_token >((*this)));
    
            case 8: return 8 + hash_space::hash<quic_server_test_stream::ack_delay_exponent>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::ack_delay_exponent >((*this)));
    
            case 9: return 9 + hash_space::hash<quic_server_test_stream::initial_max_stream_id_uni>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_uni >((*this)));
    
            case 10: return 10 + hash_space::hash<quic_server_test_stream::disable_active_migration>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::disable_active_migration >((*this)));
    
            case 11: return 11 + hash_space::hash<quic_server_test_stream::initial_max_stream_data_bidi_remote>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_remote >((*this)));
    
            case 12: return 12 + hash_space::hash<quic_server_test_stream::initial_max_stream_data_uni>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_uni >((*this)));
    
            case 13: return 13 + hash_space::hash<quic_server_test_stream::max_ack_delay>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_ack_delay >((*this)));
    
            case 14: return 14 + hash_space::hash<quic_server_test_stream::active_connection_id_limit>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::active_connection_id_limit >((*this)));
    
            case 15: return 15 + hash_space::hash<quic_server_test_stream::initial_source_connection_id>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_source_connection_id >((*this)));
    
            case 16: return 16 + hash_space::hash<quic_server_test_stream::retry_source_connection_id>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::retry_source_connection_id >((*this)));
    
            case 17: return 17 + hash_space::hash<quic_server_test_stream::loss_bits>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::loss_bits >((*this)));
    
            case 18: return 18 + hash_space::hash<quic_server_test_stream::grease_quic_bit>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::grease_quic_bit >((*this)));
    
            case 19: return 19 + hash_space::hash<quic_server_test_stream::enable_time_stamp>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::enable_time_stamp >((*this)));
    
            case 20: return 20 + hash_space::hash<quic_server_test_stream::min_ack_delay>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::min_ack_delay >((*this)));
    
            case 21: return 21 + hash_space::hash<quic_server_test_stream::version_information>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::version_information >((*this)));
    
            case 22: return 22 + hash_space::hash<quic_server_test_stream::unknown_ignore>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_ignore >((*this)));
    
            case 23: return 23 + hash_space::hash<quic_server_test_stream::unknown_transport_parameter>()(quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_transport_parameter >((*this)));
    
        }
    
        return 0;
    
    }
    
    template <typename T> static const T &unwrap(const transport_parameter &x) {
    
        return ((static_cast<const twrap<T> *>(x.ptr))->item);
    
    }
    
    template <typename T> static T &unwrap(transport_parameter &x) {
    
         twrap<T> *p = static_cast<twrap<T> *>(x.ptr);
    
         if (p->refs > 1) {
    
             p = new twrap<T> (p->item);
    
         }
    
         return ((static_cast<twrap<T> *>(p))->item);
    
    }
    
};    struct original_destination_connection_id {
    cid dcid;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(dcid);
return hv;
}
    };
    struct initial_max_stream_data_bidi_local {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct initial_max_data {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct initial_max_stream_id_bidi {
    unsigned stream_id_16;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(stream_id_16);
return hv;
}
    };
    struct max_idle_timeout {
    int seconds_16;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(seconds_16);
return hv;
}
    };
    struct preferred_address {
    unsigned ip_addr;
    unsigned ip_port;
    ipv6__addr ip6_addr;
    unsigned ip6_port;
    unsigned long long pcid_len;
    cid pcid;
    ipv6__addr pref_token;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(ip_addr);
hv += hash_space::hash<unsigned>()(ip_port);
hv += hash_space::hash<ipv6__addr>()(ip6_addr);
hv += hash_space::hash<unsigned>()(ip6_port);
hv += hash_space::hash<unsigned long long>()(pcid_len);
hv += hash_space::hash<cid>()(pcid);
hv += hash_space::hash<ipv6__addr>()(pref_token);
return hv;
}
    };
    struct max_packet_size {
    unsigned long long stream_pos_16;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_16);
return hv;
}
    };
    struct stateless_reset_token {
    ipv6__addr data_8;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<ipv6__addr>()(data_8);
return hv;
}
    };
    struct ack_delay_exponent {
    int exponent_8;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(exponent_8);
return hv;
}
    };
    struct initial_max_stream_id_uni {
    unsigned stream_id_16;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(stream_id_16);
return hv;
}
    };
    struct disable_active_migration {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct initial_max_stream_data_bidi_remote {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct initial_max_stream_data_uni {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct max_ack_delay {
    int exponent_8;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(exponent_8);
return hv;
}
    };
    struct active_connection_id_limit {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct initial_source_connection_id {
    cid scid;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(scid);
return hv;
}
    };
    struct retry_source_connection_id {
    cid rcid;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(rcid);
return hv;
}
    };
    struct loss_bits {
    unsigned long long unknown;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(unknown);
return hv;
}
    };
    struct grease_quic_bit {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct enable_time_stamp {
    unsigned long long stream_pos_32;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(stream_pos_32);
return hv;
}
    };
    struct min_ack_delay {
    int exponent_8;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(exponent_8);
return hv;
}
    };
    struct version_information {
    unsigned chosen_version;
    versions_bv other_version;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(chosen_version);
hv += hash_space::hash<versions_bv>()(other_version);
return hv;
}
    };
    struct unknown_ignore {
        size_t __hash() const { size_t hv = 0;
return hv;
}
    };
    struct unknown_transport_parameter {
    unsigned long long unknown;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned long long>()(unknown);
return hv;
}
    };
    struct trans_params_struct {
    bool original_destination_connection_id__is_set;
    original_destination_connection_id original_destination_connection_id__value;
    bool initial_max_stream_data_bidi_local__is_set;
    initial_max_stream_data_bidi_local initial_max_stream_data_bidi_local__value;
    bool initial_max_data__is_set;
    initial_max_data initial_max_data__value;
    bool initial_max_stream_id_bidi__is_set;
    initial_max_stream_id_bidi initial_max_stream_id_bidi__value;
    bool max_idle_timeout__is_set;
    max_idle_timeout max_idle_timeout__value;
    bool preferred_address__is_set;
    preferred_address preferred_address__value;
    bool max_packet_size__is_set;
    max_packet_size max_packet_size__value;
    bool stateless_reset_token__is_set;
    stateless_reset_token stateless_reset_token__value;
    bool ack_delay_exponent__is_set;
    ack_delay_exponent ack_delay_exponent__value;
    bool initial_max_stream_id_uni__is_set;
    initial_max_stream_id_uni initial_max_stream_id_uni__value;
    bool disable_active_migration__is_set;
    disable_active_migration disable_active_migration__value;
    bool initial_max_stream_data_bidi_remote__is_set;
    initial_max_stream_data_bidi_remote initial_max_stream_data_bidi_remote__value;
    bool initial_max_stream_data_uni__is_set;
    initial_max_stream_data_uni initial_max_stream_data_uni__value;
    bool max_ack_delay__is_set;
    max_ack_delay max_ack_delay__value;
    bool active_connection_id_limit__is_set;
    active_connection_id_limit active_connection_id_limit__value;
    bool initial_source_connection_id__is_set;
    initial_source_connection_id initial_source_connection_id__value;
    bool retry_source_connection_id__is_set;
    retry_source_connection_id retry_source_connection_id__value;
    bool loss_bits__is_set;
    loss_bits loss_bits__value;
    bool grease_quic_bit__is_set;
    grease_quic_bit grease_quic_bit__value;
    bool enable_time_stamp__is_set;
    enable_time_stamp enable_time_stamp__value;
    bool min_ack_delay__is_set;
    min_ack_delay min_ack_delay__value;
    bool version_information__is_set;
    version_information version_information__value;
    bool unknown_ignore__is_set;
    unknown_ignore unknown_ignore__value;
    bool unknown_transport_parameter__is_set;
    unknown_transport_parameter unknown_transport_parameter__value;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<bool>()(original_destination_connection_id__is_set);
hv += hash_space::hash<original_destination_connection_id>()(original_destination_connection_id__value);
hv += hash_space::hash<bool>()(initial_max_stream_data_bidi_local__is_set);
hv += hash_space::hash<initial_max_stream_data_bidi_local>()(initial_max_stream_data_bidi_local__value);
hv += hash_space::hash<bool>()(initial_max_data__is_set);
hv += hash_space::hash<initial_max_data>()(initial_max_data__value);
hv += hash_space::hash<bool>()(initial_max_stream_id_bidi__is_set);
hv += hash_space::hash<initial_max_stream_id_bidi>()(initial_max_stream_id_bidi__value);
hv += hash_space::hash<bool>()(max_idle_timeout__is_set);
hv += hash_space::hash<max_idle_timeout>()(max_idle_timeout__value);
hv += hash_space::hash<bool>()(preferred_address__is_set);
hv += hash_space::hash<preferred_address>()(preferred_address__value);
hv += hash_space::hash<bool>()(max_packet_size__is_set);
hv += hash_space::hash<max_packet_size>()(max_packet_size__value);
hv += hash_space::hash<bool>()(stateless_reset_token__is_set);
hv += hash_space::hash<stateless_reset_token>()(stateless_reset_token__value);
hv += hash_space::hash<bool>()(ack_delay_exponent__is_set);
hv += hash_space::hash<ack_delay_exponent>()(ack_delay_exponent__value);
hv += hash_space::hash<bool>()(initial_max_stream_id_uni__is_set);
hv += hash_space::hash<initial_max_stream_id_uni>()(initial_max_stream_id_uni__value);
hv += hash_space::hash<bool>()(disable_active_migration__is_set);
hv += hash_space::hash<disable_active_migration>()(disable_active_migration__value);
hv += hash_space::hash<bool>()(initial_max_stream_data_bidi_remote__is_set);
hv += hash_space::hash<initial_max_stream_data_bidi_remote>()(initial_max_stream_data_bidi_remote__value);
hv += hash_space::hash<bool>()(initial_max_stream_data_uni__is_set);
hv += hash_space::hash<initial_max_stream_data_uni>()(initial_max_stream_data_uni__value);
hv += hash_space::hash<bool>()(max_ack_delay__is_set);
hv += hash_space::hash<max_ack_delay>()(max_ack_delay__value);
hv += hash_space::hash<bool>()(active_connection_id_limit__is_set);
hv += hash_space::hash<active_connection_id_limit>()(active_connection_id_limit__value);
hv += hash_space::hash<bool>()(initial_source_connection_id__is_set);
hv += hash_space::hash<initial_source_connection_id>()(initial_source_connection_id__value);
hv += hash_space::hash<bool>()(retry_source_connection_id__is_set);
hv += hash_space::hash<retry_source_connection_id>()(retry_source_connection_id__value);
hv += hash_space::hash<bool>()(loss_bits__is_set);
hv += hash_space::hash<loss_bits>()(loss_bits__value);
hv += hash_space::hash<bool>()(grease_quic_bit__is_set);
hv += hash_space::hash<grease_quic_bit>()(grease_quic_bit__value);
hv += hash_space::hash<bool>()(enable_time_stamp__is_set);
hv += hash_space::hash<enable_time_stamp>()(enable_time_stamp__value);
hv += hash_space::hash<bool>()(min_ack_delay__is_set);
hv += hash_space::hash<min_ack_delay>()(min_ack_delay__value);
hv += hash_space::hash<bool>()(version_information__is_set);
hv += hash_space::hash<version_information>()(version_information__value);
hv += hash_space::hash<bool>()(unknown_ignore__is_set);
hv += hash_space::hash<unknown_ignore>()(unknown_ignore__value);
hv += hash_space::hash<bool>()(unknown_transport_parameter__is_set);
hv += hash_space::hash<unknown_transport_parameter>()(unknown_transport_parameter__value);
return hv;
}
    };
    class vector__transport_parameter__ : public std::vector<transport_parameter>{
        public: size_t __hash() const { return hash_space::hash<std::vector<transport_parameter> >()(*this);};
    };
    struct quic_transport_parameters {
    vector__transport_parameter__ transport_parameters;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<vector__transport_parameter__>()(transport_parameters);
return hv;
}
    };
    class arr_streamid_s : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class arr_pkt_num_s : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class arr_streamid_r : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class arr_pkt_num_r : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct quic_packet {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    stream_data token;
    unsigned seq_num;
    frame__arr payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<stream_data>()(token);
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<frame__arr>()(payload);
return hv;
}
    };
    class quic_packet__arr : public std::vector<quic_packet>{
        public: size_t __hash() const { return hash_space::hash<std::vector<quic_packet> >()(*this);};
    };
    struct quic_packet_retry {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    stream_data token;
    itoken integrity_token;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<stream_data>()(token);
hv += hash_space::hash<itoken>()(integrity_token);
return hv;
}
    };
    class quic_packet_retry__arr : public std::vector<quic_packet_retry>{
        public: size_t __hash() const { return hash_space::hash<std::vector<quic_packet_retry> >()(*this);};
    };
    class quic_packet_retry__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct quic_packet_0rtt {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    unsigned seq_num;
    frame__arr payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<frame__arr>()(payload);
return hv;
}
    };
    class quic_packet_0rtt__arr : public std::vector<quic_packet_0rtt>{
        public: size_t __hash() const { return hash_space::hash<std::vector<quic_packet_0rtt> >()(*this);};
    };
    class quic_packet_0rtt__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct quic_packet_coal_0rtt {
    quic_packet_type ptype_i;
    unsigned pversion_i;
    cid dst_cid_i;
    cid src_cid_i;
    stream_data token_i;
    unsigned seq_num_i;
    frame__arr payload_i;
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    unsigned seq_num;
    frame__arr payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype_i);
hv += hash_space::hash<unsigned>()(pversion_i);
hv += hash_space::hash<cid>()(dst_cid_i);
hv += hash_space::hash<cid>()(src_cid_i);
hv += hash_space::hash<stream_data>()(token_i);
hv += hash_space::hash<unsigned>()(seq_num_i);
hv += hash_space::hash<frame__arr>()(payload_i);
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<frame__arr>()(payload);
return hv;
}
    };
    class quic_packet_coal_0rtt__arr : public std::vector<quic_packet_coal_0rtt>{
        public: size_t __hash() const { return hash_space::hash<std::vector<quic_packet_coal_0rtt> >()(*this);};
    };
    class quic_packet_coal_0rtt__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class forged_pkts : public std::vector<stream_data>{
        public: size_t __hash() const { return hash_space::hash<std::vector<stream_data> >()(*this);};
    };
    struct forged_protected_quic_packet {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    stream_data token;
    stream_data protected_payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<stream_data>()(token);
hv += hash_space::hash<stream_data>()(protected_payload);
return hv;
}
    };
    class forged_protected_quic_packet__arr : public std::vector<forged_protected_quic_packet>{
        public: size_t __hash() const { return hash_space::hash<std::vector<forged_protected_quic_packet> >()(*this);};
    };
    class forged_protected_quic_packet__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct forged_quic_packet {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    stream_data token;
    unsigned seq_num;
    frame__arr payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<stream_data>()(token);
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<frame__arr>()(payload);
return hv;
}
    };
    class forged_quic_packet__arr : public std::vector<forged_quic_packet>{
        public: size_t __hash() const { return hash_space::hash<std::vector<forged_quic_packet> >()(*this);};
    };
    class forged_quic_packet__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct forged_quic_packet_retry {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    stream_data token;
    itoken integrity_token;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<stream_data>()(token);
hv += hash_space::hash<itoken>()(integrity_token);
return hv;
}
    };
    class forged_quic_packet_retry__arr : public std::vector<forged_quic_packet_retry>{
        public: size_t __hash() const { return hash_space::hash<std::vector<forged_quic_packet_retry> >()(*this);};
    };
    class forged_quic_packet_retry__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    struct forged_quic_packet_vn {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    versions_bv supported_version;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<versions_bv>()(supported_version);
return hv;
}
    };
    class forged_quic_packet_vn__arr : public std::vector<forged_quic_packet_vn>{
        public: size_t __hash() const { return hash_space::hash<std::vector<forged_quic_packet_vn> >()(*this);};
    };
    struct replayed_quic_packet_0rtt {
    quic_packet_type ptype;
    unsigned pversion;
    cid dst_cid;
    cid src_cid;
    unsigned seq_num;
    frame__arr payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(ptype);
hv += hash_space::hash<unsigned>()(pversion);
hv += hash_space::hash<cid>()(dst_cid);
hv += hash_space::hash<cid>()(src_cid);
hv += hash_space::hash<unsigned>()(seq_num);
hv += hash_space::hash<frame__arr>()(payload);
return hv;
}
    };
    class replayed_quic_packet_0rtt__arr : public std::vector<replayed_quic_packet_0rtt>{
        public: size_t __hash() const { return hash_space::hash<std::vector<replayed_quic_packet_0rtt> >()(*this);};
    };
    class replayed_quic_packet_0rtt__retired_cids : public std::vector<unsigned>{
        public: size_t __hash() const { return hash_space::hash<std::vector<unsigned> >()(*this);};
    };
    class prot__arr : public std::vector<stream_data>{
        public: size_t __hash() const { return hash_space::hash<std::vector<stream_data> >()(*this);};
    };
    struct prot__header_info {
    bool hdr_long;
    unsigned hdr_type;
    cid dcid;
    cid scid;
    unsigned long long payload_length;
    unsigned long long token_length;
    unsigned long long payload_length_pos;
    unsigned long long pkt_num_pos;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<bool>()(hdr_long);
hv += hash_space::hash<unsigned>()(hdr_type);
hv += hash_space::hash<cid>()(dcid);
hv += hash_space::hash<cid>()(scid);
hv += hash_space::hash<unsigned long long>()(payload_length);
hv += hash_space::hash<unsigned long long>()(token_length);
hv += hash_space::hash<unsigned long long>()(payload_length_pos);
hv += hash_space::hash<unsigned long long>()(pkt_num_pos);
return hv;
}
    };
class tls_api__id : public LongClass {
public:
    
    tls_api__id(){}
    tls_api__id(const LongClass &s) : LongClass(s) {}
    tls_api__id(int128_t v) : LongClass(v) {}
    size_t __hash() const { return hash_space::hash<LongClass>()(*this); }
    #ifdef Z3PP_H_
    static z3::sort z3_sort(z3::context &ctx) {return ctx.bv_sort(16);}
    static hash_space::hash_map<LongClass,int> x_to_bv_hash;
    static hash_space::hash_map<int,LongClass> bv_to_x_hash;
    static int next_bv;
    static std::vector<LongClass> nonces;
    static LongClass random_x();
    static int x_to_bv(const LongClass &s){
        if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
            for (; next_bv < (1<<16); next_bv++) {
                if(bv_to_x_hash.find(next_bv) == bv_to_x_hash.end()) {
                    x_to_bv_hash[s] = next_bv;
                    bv_to_x_hash[next_bv] = s;
    		//std::cerr << "bv_to_x_hash[next_bv]" << s << std::endl;
                    return next_bv++;
                } 
            }
            std::cerr << "Ran out of values for type tls_api__id" << std::endl;
            __ivy_out << "out_of_values(tls_api__id,\"" << s << "\")" << std::endl;
            for (int i = 0; i < (1<<16); i++)
                __ivy_out << "value(\"" << bv_to_x_hash[i] << "\")" << std::endl;
            __ivy_exit(1);
        }
        return x_to_bv_hash[s];
    }
    static LongClass bv_to_x(int bv){
        if(bv_to_x_hash.find(bv) == bv_to_x_hash.end()){
            int num = 0;
            while (true) {
                // std::ostringstream str;
                // str << num;
                // LongClass s = str.str();
                LongClass s = random_x();
                if(x_to_bv_hash.find(s) == x_to_bv_hash.end()){
                   x_to_bv_hash[s] = bv;
                   bv_to_x_hash[bv] = s;
    	       //sstd::cerr << "bv_to_x_hash: " << s << std::endl;
                   return s;
                }
                num++;
            }
        }
        //std::cerr << "bv_to_x_hash: " << bv_to_x_hash[bv] << std::endl;
        return bv_to_x_hash[bv];
    }
    static void prepare() {}
    static void cleanup() {
        x_to_bv_hash.clear();
        bv_to_x_hash.clear();
        next_bv = 0;
    }
    #endif
};    struct tls_api__upper__decrypt_result {
    bool ok;
    stream_data data;
    stream_data payload;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<bool>()(ok);
hv += hash_space::hash<stream_data>()(data);
hv += hash_space::hash<stream_data>()(payload);
return hv;
}
    };
    enum endpoint_id{endpoint_id__client,endpoint_id__client_alt,endpoint_id__client_vn,endpoint_id__server,endpoint_id__server_alt,endpoint_id__mim,endpoint_id__victim,endpoint_id__client_server,endpoint_id__attacker};
    class cids : public std::vector<cid>{
        public: size_t __hash() const { return hash_space::hash<std::vector<cid> >()(*this);};
    };
    struct clients__client {
    ip__endpoint ep;
    tls_api__id tls_id;
    quic_packet_type enc_level;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<ip__endpoint>()(ep);
hv += hash_space::hash<tls_api__id>()(tls_id);
hv += hash_space::hash<int>()(enc_level);
return hv;
}
    };
    class clients__client__arr : public std::vector<clients__client>{
        public: size_t __hash() const { return hash_space::hash<std::vector<clients__client> >()(*this);};
    };
    struct servers__server {
    ip__endpoint ep;
    tls_api__id tls_id;
    quic_packet_type enc_level;
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<ip__endpoint>()(ep);
hv += hash_space::hash<tls_api__id>()(tls_id);
hv += hash_space::hash<int>()(enc_level);
return hv;
}
    };
    class servers__server__arr : public std::vector<servers__server>{
        public: size_t __hash() const { return hash_space::hash<std::vector<servers__server> >()(*this);};
    };
    class ip_endpoints : public std::vector<ip__endpoint>{
        public: size_t __hash() const { return hash_space::hash<std::vector<ip__endpoint> >()(*this);};
    };
    class tls_extensions : public std::vector<tls__extension>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__extension> >()(*this);};
    };
    class tls_hand_extensions : public std::vector<tls__handshake>{
        public: size_t __hash() const { return hash_space::hash<std::vector<tls__handshake> >()(*this);};
    };
struct __tup__cid__unsigned {
    cid arg0;
    unsigned arg1;
__tup__cid__unsigned(){}__tup__cid__unsigned(const cid &arg0,const unsigned &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<unsigned>()(arg1);
return hv;
}
};
struct __tup__cid__quic_packet_type {
    cid arg0;
    quic_packet_type arg1;
__tup__cid__quic_packet_type(){}__tup__cid__quic_packet_type(const cid &arg0,const quic_packet_type &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<int>()(arg1);
return hv;
}
};
struct __tup__cid__quic_packet_type__unsigned_long_long {
    cid arg0;
    quic_packet_type arg1;
    unsigned long long arg2;
__tup__cid__quic_packet_type__unsigned_long_long(){}__tup__cid__quic_packet_type__unsigned_long_long(const cid &arg0,const quic_packet_type &arg1,const unsigned long long &arg2) : arg0(arg0),arg1(arg1),arg2(arg2){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<int>()(arg1);
hv += hash_space::hash<unsigned long long>()(arg2);
return hv;
}
};
struct __tup__cid__stream_kind {
    cid arg0;
    stream_kind arg1;
__tup__cid__stream_kind(){}__tup__cid__stream_kind(const cid &arg0,const stream_kind &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<int>()(arg1);
return hv;
}
};
struct __tup__cid__stream_data {
    cid arg0;
    stream_data arg1;
__tup__cid__stream_data(){}__tup__cid__stream_data(const cid &arg0,const stream_data &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<stream_data>()(arg1);
return hv;
}
};
struct __tup__unsigned__unsigned__unsigned__cid__unsigned {
    unsigned arg0;
    unsigned arg1;
    unsigned arg2;
    cid arg3;
    unsigned arg4;
__tup__unsigned__unsigned__unsigned__cid__unsigned(){}__tup__unsigned__unsigned__unsigned__cid__unsigned(const unsigned &arg0,const unsigned &arg1,const unsigned &arg2,const cid &arg3,const unsigned &arg4) : arg0(arg0),arg1(arg1),arg2(arg2),arg3(arg3),arg4(arg4){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<unsigned>()(arg0);
hv += hash_space::hash<unsigned>()(arg1);
hv += hash_space::hash<unsigned>()(arg2);
hv += hash_space::hash<cid>()(arg3);
hv += hash_space::hash<unsigned>()(arg4);
return hv;
}
};
struct __tup__cid__quic_packet_type__unsigned {
    cid arg0;
    quic_packet_type arg1;
    unsigned arg2;
__tup__cid__quic_packet_type__unsigned(){}__tup__cid__quic_packet_type__unsigned(const cid &arg0,const quic_packet_type &arg1,const unsigned &arg2) : arg0(arg0),arg1(arg1),arg2(arg2){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<int>()(arg1);
hv += hash_space::hash<unsigned>()(arg2);
return hv;
}
};
struct __tup__ip__endpoint__ip__endpoint__cid {
    ip__endpoint arg0;
    ip__endpoint arg1;
    cid arg2;
__tup__ip__endpoint__ip__endpoint__cid(){}__tup__ip__endpoint__ip__endpoint__cid(const ip__endpoint &arg0,const ip__endpoint &arg1,const cid &arg2) : arg0(arg0),arg1(arg1),arg2(arg2){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<ip__endpoint>()(arg0);
hv += hash_space::hash<ip__endpoint>()(arg1);
hv += hash_space::hash<cid>()(arg2);
return hv;
}
};
struct __tup__cid__ip__endpoint {
    cid arg0;
    ip__endpoint arg1;
__tup__cid__ip__endpoint(){}__tup__cid__ip__endpoint(const cid &arg0,const ip__endpoint &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<cid>()(arg0);
hv += hash_space::hash<ip__endpoint>()(arg1);
return hv;
}
};
struct __tup__quic_packet_type__unsigned_long_long {
    quic_packet_type arg0;
    unsigned long long arg1;
__tup__quic_packet_type__unsigned_long_long(){}__tup__quic_packet_type__unsigned_long_long(const quic_packet_type &arg0,const unsigned long long &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(arg0);
hv += hash_space::hash<unsigned long long>()(arg1);
return hv;
}
};
struct __tup__quic_packet_type__unsigned {
    quic_packet_type arg0;
    unsigned arg1;
__tup__quic_packet_type__unsigned(){}__tup__quic_packet_type__unsigned(const quic_packet_type &arg0,const unsigned &arg1) : arg0(arg0),arg1(arg1){}
        size_t __hash() const { size_t hv = 0;
hv += hash_space::hash<int>()(arg0);
hv += hash_space::hash<unsigned>()(arg1);
return hv;
}
};

class hash____tup__cid__unsigned {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__unsigned &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<unsigned>()(__s.arg1);
        }
    };

class hash____tup__cid__quic_packet_type {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__quic_packet_type &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<int>()(__s.arg1);
        }
    };

class hash____tup__cid__quic_packet_type__unsigned_long_long {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__quic_packet_type__unsigned_long_long &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<int>()(__s.arg1)+hash_space::hash<unsigned long long>()(__s.arg2);
        }
    };

class hash____tup__cid__stream_kind {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__stream_kind &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<int>()(__s.arg1);
        }
    };

class hash____tup__cid__stream_data {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__stream_data &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<stream_data>()(__s.arg1);
        }
    };

class hash____tup__unsigned__unsigned__unsigned__cid__unsigned {
    public:
        size_t operator()(const quic_server_test_stream::__tup__unsigned__unsigned__unsigned__cid__unsigned &__s) const {
            return hash_space::hash<unsigned>()(__s.arg0)+hash_space::hash<unsigned>()(__s.arg1)+hash_space::hash<unsigned>()(__s.arg2)+hash_space::hash<cid>()(__s.arg3)+hash_space::hash<unsigned>()(__s.arg4);
        }
    };

class hash____tup__cid__quic_packet_type__unsigned {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__quic_packet_type__unsigned &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<int>()(__s.arg1)+hash_space::hash<unsigned>()(__s.arg2);
        }
    };

class hash____tup__ip__endpoint__ip__endpoint__cid {
    public:
        size_t operator()(const quic_server_test_stream::__tup__ip__endpoint__ip__endpoint__cid &__s) const {
            return hash_space::hash<ip__endpoint>()(__s.arg0)+hash_space::hash<ip__endpoint>()(__s.arg1)+hash_space::hash<cid>()(__s.arg2);
        }
    };

class hash____tup__cid__ip__endpoint {
    public:
        size_t operator()(const quic_server_test_stream::__tup__cid__ip__endpoint &__s) const {
            return hash_space::hash<cid>()(__s.arg0)+hash_space::hash<ip__endpoint>()(__s.arg1);
        }
    };

class hash____tup__quic_packet_type__unsigned_long_long {
    public:
        size_t operator()(const quic_server_test_stream::__tup__quic_packet_type__unsigned_long_long &__s) const {
            return hash_space::hash<int>()(__s.arg0)+hash_space::hash<unsigned long long>()(__s.arg1);
        }
    };

class hash____tup__quic_packet_type__unsigned {
    public:
        size_t operator()(const quic_server_test_stream::__tup__quic_packet_type__unsigned &__s) const {
            return hash_space::hash<int>()(__s.arg0)+hash_space::hash<unsigned>()(__s.arg1);
        }
    };
    bool _generating;
    bool is_no_error;
    hash_thunk<__tup__cid__unsigned,stream_data> stream_app_data;
    hash_thunk<__tup__cid__unsigned,unsigned long long> stream_app_data_end;
    hash_thunk<__tup__cid__unsigned,bool> stream_app_data_finished;
    hash_thunk<cid,bool> used_cid;
    hash_thunk<__tup__cid__quic_packet_type,stream_data> crypto_data;
    hash_thunk<__tup__cid__quic_packet_type__unsigned_long_long,bool> crypto_data_present;
    hash_thunk<__tup__cid__quic_packet_type,unsigned long long> crypto_data_end;
    hash_thunk<__tup__cid__quic_packet_type,unsigned long long> crypto_length;
    hash_thunk<__tup__cid__quic_packet_type,unsigned long long> crypto_pos;
    hash_thunk<__tup__cid__quic_packet_type,unsigned long long> crypto_handler_pos;
    hash_thunk<cid,bool> established_1rtt_keys;
    hash_thunk<cid,bool> established_handshake_keys;
    hash_thunk<cid,bool> crypto_reset;
    hash_thunk<__tup__cid__unsigned,bool> stream_seen;
    hash_thunk<__tup__cid__unsigned,unsigned long long> max_stream_data_val;
    hash_thunk<__tup__cid__unsigned,bool> max_stream_data_set;
    hash_thunk<cid,unsigned long long> max_data_val;
    hash_thunk<cid,bool> max_data_set;
    hash_thunk<__tup__cid__unsigned,unsigned long long> stream_length;
    hash_thunk<__tup__cid__unsigned,bool> stream_finished;
    hash_thunk<__tup__cid__unsigned,bool> stream_reset;
    hash_thunk<__tup__cid__stream_kind,bool> max_stream_set;
    hash_thunk<__tup__cid__stream_kind,unsigned> max_stream;
    hash_thunk<cid,frame__arr> queued_frames;
    hash_thunk<cid,frame__arr> queued_frames_rtt;
    hash_thunk<cid,quic_packet_type> queued_level;
    hash_thunk<cid,bool> queued_non_probing;
    hash_thunk<cid,bool> queued_non_ack;
    hash_thunk<cid,bool> queued_close;
    hash_thunk<cid,unsigned long long> num_queued_frames;
    hash_thunk<cid,unsigned long long> num_queued_frames_rtt;
    hash_thunk<__tup__cid__stream_data,bool> path_challenge_pending;
    hash_thunk<cid,bool> path_challenge_sent;
    hash_thunk<cid,unsigned long long> conn_total_data;
    hash_thunk<cid,bool> queued_ack_eliciting;
    hash_thunk<unsigned long long,bool> queued_ack_eliciting_pkt;
    unsigned long long num_ack_eliciting_pkt;
    unsigned long long num_ack_pkt;
    hash_thunk<cid,bool> send_retire_cid;
    hash_thunk<cid,unsigned> max_rtp_num;
    bool first_ack_freq_received;
    hash_thunk<cid,unsigned> last_ack_freq_seq;
    hash_thunk<__tup__unsigned__unsigned__unsigned__cid__unsigned,unsigned long long> count_newcid_frame;
    hash_thunk<unsigned,unsigned long long> count_rcid_frame;
    bool handshake_done_send;
    bool handshake_done_recv;
    hash_thunk<cid,unsigned long long> ack_eliciting_threshold_val;
    hash_thunk<cid,unsigned long long> ack_eliciting_threshold_current_val;
    hash_thunk<cid,unsigned long long> ack_out_of_order_val;
    bool ack_frequency_pending;
    unsigned long long initial_max_stream_data_uni_server_0rtt;
    unsigned long long initial_max_stream_data_bidi_remote_server_0rtt;
    unsigned long long initial_max_data_server_0rtt;
    unsigned long long initial_max_stream_data_bidi_local_server_0rtt;
    unsigned initial_max_stream_id_bidi_server_0rtt;
    unsigned long long active_connection_id_limit_server_0rtt;
    hash_thunk<cid,bool> conn_seen;
    hash_thunk<cid,bool> conn_closed;
    hash_thunk<cid,bool> conn_draining;
    hash_thunk<cid,bool> draining_pkt_sent;
    hash_thunk<__tup__cid__quic_packet_type,unsigned> last_pkt_num;
    hash_thunk<__tup__cid__quic_packet_type__unsigned,bool> sent_pkt;
    hash_thunk<__tup__cid__quic_packet_type__unsigned,bool> acked_pkt;
    hash_thunk<__tup__cid__quic_packet_type,unsigned> max_acked;
    hash_thunk<cid,unsigned> ack_credit;
    hash_thunk<cid,trans_params_struct> trans_params;
    hash_thunk<cid,bool> connected;
    hash_thunk<cid,cid> cid_to_aid;
    hash_thunk<cid,bool> cid_mapped;
    hash_thunk<__tup__cid__unsigned,cid> seqnum_to_cid;
    hash_thunk<cid,unsigned> max_seq_num;
    hash_thunk<cid,cid> connected_to;
    hash_thunk<cid,cid> nonce_cid;
    hash_thunk<cid,bool> is_client;
    hash_thunk<__tup__ip__endpoint__ip__endpoint__cid,bool> conn_requested;
    bool issued_zero_length_cid;
    hash_thunk<cid,unsigned> hi_non_probing;
    hash_thunk<__tup__cid__ip__endpoint,bool> hi_non_probing_endpoint;
    hash_thunk<__tup__cid__quic_packet_type__unsigned,bool> pkt_has_close;
    hash_thunk<cid,unsigned long long> num_conn;
    bool tls_handshake_finished;
    bool migration_done;
    bool first_initial_send;
    cid initial_scid;
    cid initial_dcid;
    hash_thunk<frame__arr,unsigned> is_retransmitted;
    ip__endpoint dst_endpoint;
    bool address_validated;
    hash_thunk<cid,bool> retry_sent;
    hash_thunk<cid,bool> retry_recv;
    bool token_saved;
    bool zero_length_token;
    hash_thunk<cid,bool> retry_response;
    bool retry_client_test;
    hash_thunk<cid,stream_data> retry_token;
    unsigned long long header_retry;
    stream_data last_zrtt_pkt;
    bool zrtt_pkt_set;
    bool zrtt_pkt_process;
    unsigned drop_n;
    unsigned drop_every_n;
    int temporary_delay;
    int permanent_delay;
    int start_delay;
    int drop_delay;
    unsigned current_recv_pkt;
    int loss_detection_timer;
    int first_rtt_sample;
    hash_thunk<cid,int> latest_rtt;
    hash_thunk<cid,int> smoothed_rtt;
    hash_thunk<cid,int> rttvar;
    hash_thunk<cid,int> min_rtt;
    int time_of_last_ack_eliciting_packet[6];
    unsigned largest_acked_packet[6];
    int loss_time[6];
    hash_thunk<__tup__quic_packet_type__unsigned_long_long,quic_packet> newly_acked_packets;
    unsigned long long newly_acked_packets_end[6];
    hash_thunk<__tup__quic_packet_type__unsigned_long_long,quic_packet> lost_packets;
    unsigned long long lost_packets_end[6];
    unsigned long long pc_lost_end[6];
    hash_thunk<__tup__quic_packet_type__unsigned_long_long,quic_packet> sent_packets;
    unsigned long long sent_packets_end[6];
    hash_thunk<__tup__quic_packet_type__unsigned,unsigned> sent_packets_packet_number;
    hash_thunk<__tup__quic_packet_type__unsigned,int> sent_packets_time_sent;
    hash_thunk<__tup__quic_packet_type__unsigned,bool> sent_packets_ack_eliciting;
    hash_thunk<__tup__quic_packet_type__unsigned,bool> sent_packets_in_flight;
    hash_thunk<__tup__quic_packet_type__unsigned,unsigned long long> sent_packets_sent_bytes;
    unsigned long long received_packets_end[6];
    hash_thunk<__tup__quic_packet_type__unsigned,unsigned> received_packets_packet_number;
    hash_thunk<__tup__quic_packet_type__unsigned,int> received_packets_time_sent;
    hash_thunk<__tup__quic_packet_type__unsigned,bool> received_packets_ack_eliciting;
    hash_thunk<__tup__quic_packet_type__unsigned,unsigned long long> received_packets_sent_bytes;
    hash_thunk<__tup__quic_packet_type__unsigned_long_long,frame__arr> packets_to_retransmit;
    unsigned long long packets_to_retransmit_end[6];
    bool ack_eliciting_packet_in_flight;
    hash_thunk<unsigned,int> sent_time_of_largest_acked;
    unsigned long long kPacketThreshold;
    bool anti_amplification_limit_reached;
    int kTimeThreshold;
    int kGranularity;
    int pto_count;
    int pto_timeout;
    int max_idle_timeout_server;
    int max_idle_timeout_client;
    int max_idle_timeout_used;
    hash_thunk<cid,int> idle_timeout;
    bool connection_timeout;
    int max_ack_delay_tp;
    int local_max_ack_delay_tp;
    int ack_delay_exponent_tp;
    bool need_sent_ack_eliciting_initial_packet;
    bool need_sent_ack_eliciting_handshake_packet;
    bool need_sent_ack_eliciting_application_packet;
    bool pn_space_discarded;
    unsigned long long kInitialWindow;
    unsigned long long kMinimumWindow;
    unsigned long long kLossReductionFactor;
    unsigned long long kPersistentCongestionThreshold;
    unsigned long long max_datagram_size;
    unsigned long long bytes_in_flight;
    unsigned long long congestion_window;
    int congestion_recovery_start_time;
    unsigned long long ssthresh;
    unsigned server_addr;
    unsigned server_port;
    unsigned server_port_alt;
    cid server_cid;
    ip__endpoint server__ep;
    ip__endpoint second_server__ep;
    cid the_cid;
    unsigned client_addr;
    unsigned client_port;
    unsigned client_port_alt;
    unsigned client_port_vn;
    unsigned long long n_clients;
    unsigned long long max_stream_data;
    unsigned initial_max_streams_bidi;
    ip__endpoint client__ep;
    tls_api__id client__tls_id;
    ip__endpoint client_alt;
    ip__endpoint client_vn;
    ip__endpoint second_client__ep;
    tls_api__id second_client__tls_id;
    int sock;
    int sock_alt;
    int sock_vn;
    unsigned victim_addr;
    unsigned victim_port;
    bool is_victim;
    forged_pkts victim_agent__ppkt_recvd;
    unsigned mim_addr;
    unsigned mim_port_in;
    unsigned mim_port_out;
    bool is_mim;
    bool is_mim_standalone;
    bool forward_packets;
    bool keep_coalesed;
    bool forward_packets_victim;
    bool modify_packets;
    bool replay_packets;
    bool save_packet;
    ip__endpoint mim_agent__ep_out;
    stream_data mim_agent__ppkt_to_be_forge;
    ip__endpoint mim_server_target__ep;
    ip__endpoint mim_client_target__ep;
    ip__endpoint fake_client__ep;
    hash_thunk<cid,bool> initial_keys_set;
    bool tp_client_set;
    cid client_initial_rcid;
    cid client_initial_scid;
    unsigned long long client_initial_scil;
    cid client_initial_dcid;
    unsigned client_initial_version;
    bool client_non_zero_scil;
    bool zero_rtt_allowed;
    bool zero_rtt_sent;
    bool zero_rtt_client_test;
    bool zero_rtt_server_test;
    unsigned long long nclients;
    cids the_cids;
    clients__client__arr clients__clients;
    servers__server__arr servers__servers;
    bool allowed_multiple_migration;
    bool first_datagram_received;
    unsigned long long last_datagram_received_size;
    bool version_negociated;
    unsigned initial_version;
    hash_thunk<ip__endpoint,bool> negocation_of_version;
    hash_thunk<ip__endpoint,bool> negocation_of_version_initiated;
    hash_thunk<cid,quic_packet_type> last_packet_type;
    unsigned long long total_data_received;
    unsigned long long total_data_sent;
    unsigned long long iversion;
    unsigned long long vnversion;
    hash_thunk<ip__endpoint,bool> version_not_found;
    versions supported_versions;
    unsigned final_version;
    versions_bv supported_versions_bv;
    stream_data http_request;
    unsigned current_stream;
    long long __CARD__bit;
    long long __CARD__type_bits;
    long long __CARD__cid_length;
    long long __CARD__cid_seq;
    long long __CARD__reset_token;
    long long __CARD__port;
    long long __CARD__ipv4;
    long long __CARD__ipv6;
    long long __CARD__idx;
    long long __CARD__byte;
    long long __CARD__stream_pos;
    long long __CARD__tls__protocol_version;
    long long __CARD__tls__extension_type;
    long long __CARD__vector__tls__psk_identity____domain;
    long long __CARD__tls__gmt;
    long long __CARD__tls__cipher_suite;
    long long __CARD__tls__compression_method;
    long long __CARD__vector__tls__cipher_suite____domain;
    long long __CARD__vector__tls__compression_method____domain;
    long long __CARD__vector__tls__extension____domain;
    long long __CARD__tls__message_type;
    long long __CARD__vector__tls__handshake____domain;
    long long __CARD__ip__addr;
    long long __CARD__ip__port;
    long long __CARD__tls__handshakes__domain;
    long long __CARD__frame__ack__range__idx;
    long long __CARD__frame__ack_ecn__range__idx;
    long long __CARD__frame__idx;
    long long __CARD__index;
    long long __CARD__version;
    long long __CARD__quic_packet_vn__idx;
    long long __CARD__ipv6__addr;
    long long __CARD__ipv6__port;
    long long __CARD__vector__transport_parameter____domain;
    long long __CARD__idx_s;
    long long __CARD__jdx_s;
    long long __CARD__idx_r;
    long long __CARD__jdx_r;
    long long __CARD__quic_packet__idx;
    long long __CARD__itoken;
    long long __CARD__quic_packet_retry__idx;
    long long __CARD__quic_packet_0rtt__idx;
    long long __CARD__quic_packet_coal_0rtt__idx;
    long long __CARD__forged_protected_quic_packet__idx;
    long long __CARD__forged_quic_packet__idx;
    long long __CARD__forged_quic_packet_retry__idx;
    long long __CARD__forged_quic_packet_vn__idx;
    long long __CARD__replayed_quic_packet_0rtt__idx;
    long long __CARD__prot__idx;
    long long __CARD__tls_api__id;
    long long __CARD__clients__client__idx;
    long long __CARD__servers__server__idx;
    long long __CARD__tls_extensions__domain;
    long long __CARD__tls_hand_extensions__domain;
    long long __CARD__cid;
    long long __CARD__pkt_num;
    long long __CARD__error_code;
    long long __CARD__stream_id;
    long long __CARD__microseconds;
    long long __CARD__seconds;
    long long __CARD__milliseconds;
    long long __CARD__tls_api__lower__level;
    long long __CARD__tls_api__upper__level;
    long long __CARD__net__socket;
    virtual unsigned bit__one();
    virtual unsigned long long stream_data__begin(const stream_data& A);
    virtual stream_kind get_stream_kind(unsigned S);
    virtual role get_stream_role(unsigned S);
    virtual unsigned long long vector__tls__extension____begin(const vector__tls__extension__& A);
    virtual unsigned long long tls__handshakes__begin(const tls__handshakes& A);
    virtual unsigned long long frame__arr__begin(const frame__arr& A);
    virtual unsigned long long vector__transport_parameter____begin(const vector__transport_parameter__& A);
    virtual unsigned long long prot__arr__begin(const prot__arr& A);
    virtual unsigned long long cids__begin(const cids& A);
    virtual unsigned long long clients__client__arr__begin(const clients__client__arr& A);
    virtual unsigned bytes__value(const bytes& a, unsigned long long i);
    virtual unsigned long long bytes__end(const bytes& a);
    virtual unsigned stream_data__value(const stream_data& a, unsigned long long i);
    virtual unsigned long long stream_data__end(const stream_data& a);
    virtual stream_data stream_data__segment(const stream_data& a, unsigned long long lo, unsigned long long hi);
    virtual tls__psk_identity vector__tls__psk_identity____value(const vector__tls__psk_identity__& a, unsigned long long i);
    virtual unsigned long long vector__tls__psk_identity____end(const vector__tls__psk_identity__& a);
    virtual unsigned vector__tls__cipher_suite____value(const vector__tls__cipher_suite__& a, unsigned long long i);
    virtual unsigned long long vector__tls__cipher_suite____end(const vector__tls__cipher_suite__& a);
    virtual unsigned vector__tls__compression_method____value(const vector__tls__compression_method__& a, unsigned long long i);
    virtual unsigned long long vector__tls__compression_method____end(const vector__tls__compression_method__& a);
    virtual quic_server_test_stream::tls__extension vector__tls__extension____value(const vector__tls__extension__& a, unsigned long long i);
    virtual unsigned long long vector__tls__extension____end(const vector__tls__extension__& a);
    virtual quic_server_test_stream::tls__handshake vector__tls__handshake____value(const vector__tls__handshake__& a, unsigned long long i);
    virtual unsigned long long vector__tls__handshake____end(const vector__tls__handshake__& a);
    virtual quic_server_test_stream::tls__handshake tls__handshakes__value(const tls__handshakes& a, unsigned long long i);
    virtual unsigned long long tls__handshakes__end(const tls__handshakes& a);
    virtual frame__ack__range frame__ack__range__arr__value(const frame__ack__range__arr& a, unsigned long long i);
    virtual unsigned long long frame__ack__range__arr__end(const frame__ack__range__arr& a);
    virtual frame__ack_ecn__range frame__ack_ecn__range__arr__value(const frame__ack_ecn__range__arr& a, unsigned long long i);
    virtual unsigned long long frame__ack_ecn__range__arr__end(const frame__ack_ecn__range__arr& a);
    virtual quic_server_test_stream::frame frame__arr__value(const frame__arr& a, unsigned long long i);
    virtual unsigned long long frame__arr__end(const frame__arr& a);
    virtual stream_data versions__value(const versions& a, unsigned long long i);
    virtual unsigned long long versions__end(const versions& a);
    virtual unsigned versions_bv__value(const versions_bv& a, unsigned long long i);
    virtual unsigned long long versions_bv__end(const versions_bv& a);
    virtual quic_packet_vn quic_packet_vn__arr__value(const quic_packet_vn__arr& a, unsigned long long i);
    virtual unsigned long long quic_packet_vn__arr__end(const quic_packet_vn__arr& a);
    virtual quic_server_test_stream::transport_parameter vector__transport_parameter____value(const vector__transport_parameter__& a, unsigned long long i);
    virtual unsigned long long vector__transport_parameter____end(const vector__transport_parameter__& a);
    virtual unsigned arr_streamid_s__value(const arr_streamid_s& a, unsigned long long i);
    virtual unsigned long long arr_streamid_s__end(const arr_streamid_s& a);
    virtual unsigned arr_pkt_num_s__value(const arr_pkt_num_s& a, unsigned long long i);
    virtual unsigned long long arr_pkt_num_s__end(const arr_pkt_num_s& a);
    virtual unsigned arr_streamid_r__value(const arr_streamid_r& a, unsigned long long i);
    virtual unsigned long long arr_streamid_r__end(const arr_streamid_r& a);
    virtual unsigned arr_pkt_num_r__value(const arr_pkt_num_r& a, unsigned long long i);
    virtual unsigned long long arr_pkt_num_r__end(const arr_pkt_num_r& a);
    virtual quic_packet quic_packet__arr__value(const quic_packet__arr& a, unsigned long long i);
    virtual unsigned long long quic_packet__arr__end(const quic_packet__arr& a);
    virtual quic_packet_retry quic_packet_retry__arr__value(const quic_packet_retry__arr& a, unsigned long long i);
    virtual unsigned long long quic_packet_retry__arr__end(const quic_packet_retry__arr& a);
    virtual unsigned quic_packet_retry__retired_cids__value(const quic_packet_retry__retired_cids& a, unsigned long long i);
    virtual unsigned long long quic_packet_retry__retired_cids__end(const quic_packet_retry__retired_cids& a);
    virtual quic_packet_0rtt quic_packet_0rtt__arr__value(const quic_packet_0rtt__arr& a, unsigned long long i);
    virtual unsigned long long quic_packet_0rtt__arr__end(const quic_packet_0rtt__arr& a);
    virtual unsigned quic_packet_0rtt__retired_cids__value(const quic_packet_0rtt__retired_cids& a, unsigned long long i);
    virtual unsigned long long quic_packet_0rtt__retired_cids__end(const quic_packet_0rtt__retired_cids& a);
    virtual quic_packet_coal_0rtt quic_packet_coal_0rtt__arr__value(const quic_packet_coal_0rtt__arr& a, unsigned long long i);
    virtual unsigned long long quic_packet_coal_0rtt__arr__end(const quic_packet_coal_0rtt__arr& a);
    virtual unsigned quic_packet_coal_0rtt__retired_cids__value(const quic_packet_coal_0rtt__retired_cids& a, unsigned long long i);
    virtual unsigned long long quic_packet_coal_0rtt__retired_cids__end(const quic_packet_coal_0rtt__retired_cids& a);
    virtual stream_data forged_pkts__value(const forged_pkts& a, unsigned long long i);
    virtual unsigned long long forged_pkts__end(const forged_pkts& a);
    virtual forged_protected_quic_packet forged_protected_quic_packet__arr__value(const forged_protected_quic_packet__arr& a, unsigned long long i);
    virtual unsigned long long forged_protected_quic_packet__arr__end(const forged_protected_quic_packet__arr& a);
    virtual unsigned forged_protected_quic_packet__retired_cids__value(const forged_protected_quic_packet__retired_cids& a, unsigned long long i);
    virtual unsigned long long forged_protected_quic_packet__retired_cids__end(const forged_protected_quic_packet__retired_cids& a);
    virtual forged_quic_packet forged_quic_packet__arr__value(const forged_quic_packet__arr& a, unsigned long long i);
    virtual unsigned long long forged_quic_packet__arr__end(const forged_quic_packet__arr& a);
    virtual unsigned forged_quic_packet__retired_cids__value(const forged_quic_packet__retired_cids& a, unsigned long long i);
    virtual unsigned long long forged_quic_packet__retired_cids__end(const forged_quic_packet__retired_cids& a);
    virtual forged_quic_packet_retry forged_quic_packet_retry__arr__value(const forged_quic_packet_retry__arr& a, unsigned long long i);
    virtual unsigned long long forged_quic_packet_retry__arr__end(const forged_quic_packet_retry__arr& a);
    virtual unsigned forged_quic_packet_retry__retired_cids__value(const forged_quic_packet_retry__retired_cids& a, unsigned long long i);
    virtual unsigned long long forged_quic_packet_retry__retired_cids__end(const forged_quic_packet_retry__retired_cids& a);
    virtual forged_quic_packet_vn forged_quic_packet_vn__arr__value(const forged_quic_packet_vn__arr& a, unsigned long long i);
    virtual unsigned long long forged_quic_packet_vn__arr__end(const forged_quic_packet_vn__arr& a);
    virtual replayed_quic_packet_0rtt replayed_quic_packet_0rtt__arr__value(const replayed_quic_packet_0rtt__arr& a, unsigned long long i);
    virtual unsigned long long replayed_quic_packet_0rtt__arr__end(const replayed_quic_packet_0rtt__arr& a);
    virtual unsigned replayed_quic_packet_0rtt__retired_cids__value(const replayed_quic_packet_0rtt__retired_cids& a, unsigned long long i);
    virtual unsigned long long replayed_quic_packet_0rtt__retired_cids__end(const replayed_quic_packet_0rtt__retired_cids& a);
    virtual stream_data prot__arr__value(const prot__arr& a, unsigned long long i);
    virtual unsigned long long prot__arr__end(const prot__arr& a);
    virtual quic_server_test_stream::cid cids__value(const cids& a, unsigned long long i);
    virtual unsigned long long cids__end(const cids& a);
    virtual clients__client clients__client__arr__value(const clients__client__arr& a, unsigned long long i);
    virtual unsigned long long clients__client__arr__end(const clients__client__arr& a);
    virtual servers__server servers__server__arr__value(const servers__server__arr& a, unsigned long long i);
    virtual unsigned long long servers__server__arr__end(const servers__server__arr& a);
    virtual ip__endpoint ip_endpoints__value(const ip_endpoints& a, unsigned long long i);
    virtual unsigned long long ip_endpoints__end(const ip_endpoints& a);
    virtual quic_server_test_stream::tls__extension tls_extensions__value(const tls_extensions& a, unsigned long long i);
    virtual unsigned long long tls_extensions__end(const tls_extensions& a);
    virtual quic_server_test_stream::tls__handshake tls_hand_extensions__value(const tls_hand_extensions& a, unsigned long long i);
    virtual unsigned long long tls_hand_extensions__end(const tls_hand_extensions& a);
    class tls_deser;
    class tls_ser;
    class tls_ser_server;

    //typedef ivy_binary_ser std_serializer;
    //typedef ivy_binary_deser std_deserializer;
    typedef ivy_binary_ser_128 std_serializer;
    typedef ivy_binary_deser_128 std_deserializer;


        typedef ivy_binary_ser std_serdes__serializer;
        typedef ivy_binary_deser std_serdes__deserializer;

    
    class quic_deser;


    class quic_ser;


    class quic_deser_vn;


    class quic_ser_vn;


    class quic_deser_retry;


    class quic_ser_retry;


    class quic_deser_zerortt;


    class quic_ser_zerortt;


    class quic_deser_forged;


    class quic_ser_forged;


    class quic_prot_ser;


    class quic_prot_deser;


    hash_space::hash_map<quic_server_test_stream::tls_api__id,picotls_connection *> tls_api__upper__foo__cid_map; // maps cid's to connections
    tls_callbacks *tls_api__upper__foo__cb;             // the callbacks to ivy


	udp_callbacks *net__impl__cb[9];             // the callbacks to ivy
	bool is_vnet = false;

                int http_request_file__fildes;
        		
	struct timeval start;
	std::unordered_map<std::string, struct timeval> breakpoints;
	CTimeMeasuring * time_api__c_timer__impl__measures;

	
	std::chrono::high_resolution_clock::time_point chrono_start;
	std::unordered_map<std::string, std::chrono::high_resolution_clock::time_point> chrono_breakpoints;
	ChronoTimeMeasuring * time_api__chrono_timer__impl__measures;

	    quic_server_test_stream(unsigned drop_n, unsigned drop_every_n, int temporary_delay, int permanent_delay, int start_delay, int drop_delay, unsigned server_addr, unsigned server_port, unsigned server_port_alt, quic_server_test_stream::cid server_cid, quic_server_test_stream::cid the_cid, unsigned client_addr, unsigned client_port, unsigned client_port_alt, unsigned client_port_vn, unsigned long long n_clients, unsigned long long max_stream_data, unsigned initial_max_streams_bidi, unsigned victim_addr, unsigned victim_port, bool is_victim, unsigned mim_addr, unsigned mim_port_in, unsigned mim_port_out, bool is_mim, bool is_mim_standalone, bool forward_packets, bool keep_coalesed, bool forward_packets_victim, bool modify_packets, bool replay_packets, bool save_packet, unsigned long long iversion, unsigned long long vnversion);
void __init();
    virtual void ext__infer_tls_events(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet& pkt);
    virtual void infer_tls_events_vn(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_vn& pkt);
    virtual void infer_tls_events_retry(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_retry& pkt);
    virtual void infer_tls_events_0rtt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_0rtt& pkt);
    virtual void ext__app_server_open_event_1rtt(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void ext__app_server_open_event_0rtt(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void ext__app_server_open_event_retry(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void ext__app_server_open_event_vn(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void ext__infer_frame(quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_server_test_stream::frame f);
    virtual void handle_transport_error(unsigned ec);
    virtual unsigned long long stream_pos__next(unsigned long long x);
    virtual unsigned long long ext__stream_pos__next(unsigned long long x);
    virtual stream_data stream_data__empty();
    virtual stream_data ext__stream_data__empty();
    virtual void stream_data__set(stream_data& a, unsigned long long x, unsigned y);
    virtual void ext__stream_data__set(stream_data& a, unsigned long long x, unsigned y);
    virtual unsigned long long stream_data__size(const stream_data& a);
    virtual unsigned long long ext__stream_data__size(const stream_data& a);
    virtual void stream_data__resize(stream_data& a, unsigned long long s, unsigned v);
    virtual void ext__stream_data__resize(stream_data& a, unsigned long long s, unsigned v);
    virtual void stream_data__append(stream_data& a, unsigned v);
    virtual void ext__stream_data__append(stream_data& a, unsigned v);
    virtual void ext__stream_data__extend(stream_data& a, const stream_data& b);
    virtual void ext__app_server_open_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void app_send_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid dcid, unsigned s, const stream_data& data, unsigned long long pos, bool close);
    virtual void ext__app_send_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid dcid, unsigned s, const stream_data& data, unsigned long long pos, bool close);
    virtual void map_cids(quic_server_test_stream::cid dcid, quic_server_test_stream::cid scid);
    virtual unsigned long long ext__vector__tls__extension____domain__next(unsigned long long x);
    virtual unsigned long long tls__handshakes__domain__next(unsigned long long x);
    virtual tls__handshake_parser__result tls__handshake_parser__deserialize(const stream_data& x, unsigned long long pos);
    virtual void tls__handshake_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::tls__handshake h);
    virtual void tls__handshake_data_event(const ip__endpoint& src, const ip__endpoint& dst, const stream_data& data);
    virtual void ext__tls_send_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, const stream_data& data, unsigned long long pos, quic_packet_type e, quic_server_test_stream::tls_api__id tls_id);
    virtual void ext__tls_recv_event(ip__endpoint src, ip__endpoint dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned long long lo, unsigned long long hi);
    virtual void ext__tls_keys_established_event(quic_server_test_stream::cid scid, quic_packet_type e);
    virtual void tls_client_initial_request(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid nonce, unsigned pversion, quic_server_test_stream::tls_api__id id);
    virtual void ext__tls_client_initial_response(const ip__endpoint& src, const ip__endpoint& dst, const stream_data& ppkt);
    virtual void ext__tls_client_version_response(const ip__endpoint& src, const ip__endpoint& dst, const stream_data& ppkt);
    virtual void ext__tls_client_retry_response(const ip__endpoint& src, const ip__endpoint& dst, const stream_data& ppkt);
    virtual void ext__tls_client_0rtt_response(const ip__endpoint& src, const ip__endpoint& dst, const stream_data& ppkt);
    virtual void show_test();
    virtual void show_tls_keys_established_event(quic_server_test_stream::cid scid, quic_packet_type e);
    virtual void ext__set_encryption_level(const ip__endpoint& src, quic_server_test_stream::cid scid, quic_packet_type e);
    virtual void handle_h3_error(unsigned ec);
    virtual unsigned long long frame__ack__range__idx__next(unsigned long long x);
    virtual unsigned long long frame__ack_ecn__range__idx__next(unsigned long long x);
    virtual unsigned long long ext__frame__idx__next(unsigned long long x);
    virtual frame__arr frame__arr__empty();
    virtual void ext__frame__arr__append(frame__arr& a, quic_server_test_stream::frame v);
    virtual void ext__frame__handle(quic_server_test_stream::frame f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void show_num_ack_eliciting_pkt(unsigned long long s);
    virtual void show_num_ack_pkt(unsigned long long s);
    virtual void is_generating(bool b);
    virtual void is_ack_frequency_respected(bool b);
    virtual void ext__frame__ack__handle(frame__ack f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void show_ack_generated();
    virtual void show_ack_eliciting_threshold_current_val(unsigned long long val);
    virtual void show_ack_eliciting_threshold_val(unsigned long long val);
    virtual void ext__frame__ack_ecn__handle(const frame__ack_ecn& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__stream__handle(frame__stream f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__crypto__handle(frame__crypto f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__rst_stream__handle(const frame__rst_stream& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__stop_sending__handle(const frame__stop_sending& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__max_streams__handle(const frame__max_streams& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__max_streams_bidi__handle(const frame__max_streams_bidi& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__connection_close__handle(const frame__connection_close& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__application_close__handle(const frame__application_close& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__max_stream_data__handle(const frame__max_stream_data& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__stream_data_blocked__handle(const frame__stream_data_blocked& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__data_blocked__handle(const frame__data_blocked& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__streams_blocked__handle(const frame__streams_blocked& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__streams_blocked_bidi__handle(const frame__streams_blocked_bidi& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__max_data__handle(const frame__max_data& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__ping__handle(frame__ping f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__unknown_frame__handle(const frame__unknown_frame& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__handshake_done__handle(const frame__handshake_done& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__new_connection_id__handle(const frame__new_connection_id& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__retire_connection_id__handle(const frame__retire_connection_id& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__path_challenge__handle(const frame__path_challenge& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__path_response__handle(frame__path_response f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__new_token__handle(const frame__new_token& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ack_freq_generated();
    virtual void ext__frame__ack_frequency__handle(const frame__ack_frequency& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__immediate_ack__handle(const frame__immediate_ack& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void ext__frame__malicious_frame__handle(const frame__malicious_frame& f, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_packet_type e, unsigned seq_num);
    virtual void enqueue_frame(quic_server_test_stream::cid scid, quic_server_test_stream::frame f, quic_packet_type e, bool probing, unsigned seq);
    virtual void enqueue_frame_rtt(quic_server_test_stream::cid scid, quic_server_test_stream::frame f, quic_packet_type e, bool probing);
    virtual bool stream_id_allowed(quic_server_test_stream::cid dcid, unsigned id, quic_packet_type e);
    virtual bool acti_coid_check(quic_server_test_stream::cid scid, unsigned long long count);
    virtual void show_pkt_num(unsigned p);
    virtual void ext__show_seqnum_to_streampos(unsigned long long p);
    virtual void ext__show_seqnum(unsigned p);
    virtual unsigned long long index__next(unsigned long long x);
    virtual unsigned long long ext__index__next(unsigned long long x);
    virtual versions versions__empty();
    virtual versions ext__versions__empty();
    virtual void versions__append(versions& a, const stream_data& v);
    virtual void ext__versions__append(versions& a, const stream_data& v);
    virtual versions_bv ext__versions_bv__empty();
    virtual void ext__versions_bv__append(versions_bv& a, unsigned v);
    virtual void packet_event_vn(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_vn& pkt);
    virtual quic_server_test_stream::cid inc_cid(quic_server_test_stream::cid c, unsigned long long inc);
    virtual void ext__transport_parameter__set(quic_server_test_stream::transport_parameter p, trans_params_struct& s);
    virtual void ext__original_destination_connection_id__set(const original_destination_connection_id& p, trans_params_struct& s);
    virtual void ext__initial_max_stream_data_bidi_local__set(const initial_max_stream_data_bidi_local& p, trans_params_struct& s);
    virtual void ext__initial_max_data__set(const initial_max_data& p, trans_params_struct& s);
    virtual void ext__initial_max_stream_id_bidi__set(const initial_max_stream_id_bidi& p, trans_params_struct& s);
    virtual void ext__max_idle_timeout__set(const max_idle_timeout& p, trans_params_struct& s);
    virtual void ext__preferred_address__set(const preferred_address& p, trans_params_struct& s);
    virtual void ext__max_packet_size__set(const max_packet_size& p, trans_params_struct& s);
    virtual void ext__stateless_reset_token__set(const stateless_reset_token& p, trans_params_struct& s);
    virtual void ext__ack_delay_exponent__set(const ack_delay_exponent& p, trans_params_struct& s);
    virtual void ext__initial_max_stream_id_uni__set(const initial_max_stream_id_uni& p, trans_params_struct& s);
    virtual void ext__disable_active_migration__set(const disable_active_migration& p, trans_params_struct& s);
    virtual void ext__initial_max_stream_data_bidi_remote__set(const initial_max_stream_data_bidi_remote& p, trans_params_struct& s);
    virtual void ext__initial_max_stream_data_uni__set(const initial_max_stream_data_uni& p, trans_params_struct& s);
    virtual void ext__max_ack_delay__set(const max_ack_delay& p, trans_params_struct& s);
    virtual void ext__active_connection_id_limit__set(const active_connection_id_limit& p, trans_params_struct& s);
    virtual void ext__initial_source_connection_id__set(const initial_source_connection_id& p, trans_params_struct& s);
    virtual void ext__retry_source_connection_id__set(const retry_source_connection_id& p, trans_params_struct& s);
    virtual void ext__loss_bits__set(const loss_bits& p, trans_params_struct& s);
    virtual void ext__grease_quic_bit__set(const grease_quic_bit& p, trans_params_struct& s);
    virtual void ext__enable_time_stamp__set(const enable_time_stamp& p, trans_params_struct& s);
    virtual void ext__min_ack_delay__set(const min_ack_delay& p, trans_params_struct& s);
    virtual void ext__version_information__set(const version_information& p, trans_params_struct& s);
    virtual void ext__unknown_ignore__set(const unknown_ignore& p, trans_params_struct& s);
    virtual void ext__unknown_transport_parameter__set(const unknown_transport_parameter& p, trans_params_struct& s);
    virtual unsigned long long ext__vector__transport_parameter____domain__next(unsigned long long x);
    virtual void ext__vector__transport_parameter____append(vector__transport_parameter__& a, quic_server_test_stream::transport_parameter v);
    virtual bool quic_packet__long(const quic_packet& pkt);
    virtual bool ext__quic_packet__long(const quic_packet& pkt);
    virtual void ext__packet_event(ip__endpoint src, ip__endpoint dst, quic_packet pkt);
    virtual void ext__send_ack_eliciting_handshake_packet(ip__endpoint src, ip__endpoint dst, quic_packet pkt);
    virtual void ext__send_ack_eliciting_initial_packet(ip__endpoint src, ip__endpoint dst, quic_packet pkt);
    virtual void show_queued_frames(quic_server_test_stream::cid scid, const frame__arr& queued_frames);
    virtual void show_current_time(int t);
    virtual void show_retransmit_lost_packet(const frame__arr& paylo);
    virtual void show_connection_timeout(int idle_timeout, int max_idle_timeout_used, int pto_timeout);
    virtual void show_initial_request_initial();
    virtual void show_is_retransmitted(unsigned long long p, unsigned c_time);
    virtual void respect_idle_timeout_none();
    virtual void handle_tls_handshake(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_server_test_stream::tls__handshake hs);
    virtual void ext__handle_tls_extensions(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, const vector__tls__extension__& exts, bool is_client_hello);
    virtual void ext__handle_client_transport_parameters(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, const quic_transport_parameters& tps, bool is_client_hello);
    virtual void ext__max_idle_timeout_update(int e);
    virtual void show_current_idle_timeout(int e);
    virtual void show_probe_idle_timeout(int e);
    virtual void ext__show_max_ack_delay(int e);
    virtual void ext__show_ack_delay_exponent(int e);
    virtual void show_ack_credit(quic_server_test_stream::cid c, unsigned p, bool eli, bool non_ack, unsigned pp);
    virtual void packet_event_retry(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_retry& pkt);
    virtual bool quic_packet_0rtt__long(const quic_packet_0rtt& pkt);
    virtual void packet_event_0rtt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_0rtt& pkt);
    virtual forged_pkts ext__forged_pkts__empty();
    virtual unsigned long long ext__random_stream_pos(unsigned long long min, unsigned long long max);
    virtual unsigned ext__random_stream_id(unsigned min, unsigned max);
    virtual void ext__modulo(unsigned n, unsigned& m);
    virtual bool ext__is_lost_recv();
    virtual unsigned long long ext__prot__idx__next(unsigned long long x);
    virtual prot__arr prot__arr__empty();
    virtual void prot__arr__append(prot__arr& a, const stream_data& v);
    virtual void prot__encrypt(quic_server_test_stream::tls_api__id c, unsigned seq, stream_data& pkt);
    virtual void prot__encrypt_rtt(quic_server_test_stream::tls_api__id c, unsigned seq, stream_data& pkt);
    virtual tls_api__upper__decrypt_result ext__prot__decrypt(quic_server_test_stream::tls_api__id c, unsigned seq, const stream_data& pkt);
    virtual stream_data prot__retry_integrity_tag(unsigned long long odcil, quic_server_test_stream::cid odcid, unsigned pversion, unsigned long long dcil, quic_server_test_stream::cid dcid, unsigned long long scil, quic_server_test_stream::cid scid, const stream_data& token, unsigned seq, unsigned long long h, bool b);
    virtual quic_server_test_stream::tls_api__id ext__prot__cid_to_tls_id(quic_server_test_stream::cid c);
    virtual int ext__prot__get_level(const stream_data& pkt);
    virtual prot__header_info ext__prot__get_header_info(const stream_data& pkt, bool decrypt);
    virtual void ext__prot__correct_pnum(unsigned last, unsigned& pnum, unsigned long long pnum_len);
    virtual unsigned long long ext__prot__get_pnum_len_b(const stream_data& pkt);
    virtual unsigned long long ext__prot__get_pnum_len(const stream_data& pkt);
    virtual unsigned ext__prot__get_pnum(const stream_data& pkt, unsigned long long pnum_pos, unsigned long long pnum_len);
    virtual unsigned long long ext__prot__get_var_int_len(const stream_data& pkt, unsigned long long pos);
    virtual unsigned long long ext__prot__get_var_int(const stream_data& pkt, unsigned long long pos, unsigned long long len);
    virtual stream_data ext__prot__to_var_int_16(unsigned long long val);
    virtual quic_server_test_stream::cid prot__bytes_to_cid(const stream_data& bytes);
    virtual quic_server_test_stream::cid ext__prot__bytes_to_cid(const stream_data& bytes);
    virtual unsigned ext__prot__byte_xor(unsigned x, unsigned y);
    virtual void ext__prot__stream_data_xor(stream_data& x, const stream_data& y);
    virtual void ext__prot__show_token_len(unsigned long long ver);
    virtual void ext__prot__show_header(const prot__header_info& h);
    virtual void tls_api__lower__send(quic_server_test_stream::tls_api__id c, const stream_data& data, int lev);
    virtual void tls_api__lower__recv(quic_server_test_stream::tls_api__id c, const stream_data& data, int lev);
    virtual void tls_api__upper__recv(quic_server_test_stream::tls_api__id c, const stream_data& data);
    virtual void tls_api__upper__alert(quic_server_test_stream::tls_api__id c, const stream_data& data);
    virtual void tls_api__upper__keys_established(quic_server_test_stream::tls_api__id c, int lev);
    virtual void tls_api__upper__create(quic_server_test_stream::tls_api__id c, bool is_server, const tls_extensions& e);
    virtual void ext__tls_api__upper__create(quic_server_test_stream::tls_api__id c, bool is_server, const tls_extensions& e);
    virtual void tls_api__upper__create_0rtt_client(quic_server_test_stream::tls_api__id c, bool is_server, const tls_extensions& e);
    virtual void tls_api__upper__save_token(const stream_data& token);
    virtual void ext__tls_api__upper__save_initial_max_stream_data_uni(unsigned long long i);
    virtual void ext__tls_api__upper__save_initial_max_stream_data_bidi_remote(unsigned long long i);
    virtual void ext__tls_api__upper__save_initial_max_data(unsigned long long i);
    virtual void ext__tls_api__upper__save_initial_max_stream_data_bidi_local(unsigned long long i);
    virtual void ext__tls_api__upper__save_initial_max_stream_id_bidi(unsigned i);
    virtual void ext__tls_api__upper__save_active_connection_id_limit(unsigned long long i);
    virtual stream_data tls_api__upper__get_old_new_token();
    virtual void tls_api__upper__destroy(quic_server_test_stream::tls_api__id c);
    virtual void tls_api__upper__set_initial_keys(quic_server_test_stream::tls_api__id c, const stream_data& salt, const stream_data& ikm);
    virtual unsigned long long ext__tls_api__upper__iv_size(quic_server_test_stream::tls_api__id c, int l);
    virtual stream_data ext__tls_api__upper__encrypt_cipher(quic_server_test_stream::tls_api__id c, int l, const stream_data& clear, const stream_data& iv, bool recv);
    virtual stream_data ext__tls_api__upper__compute_retry_integrity_tag(unsigned long long odcil, quic_server_test_stream::tls_api__id odcid, unsigned pversion, unsigned long long dcil, quic_server_test_stream::tls_api__id dcid, unsigned long long scil, quic_server_test_stream::tls_api__id scid, const stream_data& token, unsigned seq, unsigned long long h, bool is_recv);
    virtual stream_data ext__tls_api__upper__encrypt_aead(quic_server_test_stream::tls_api__id c, int l, const stream_data& clear, unsigned seq, const stream_data& ad);
    virtual tls_api__upper__decrypt_result ext__tls_api__upper__decrypt_aead(quic_server_test_stream::tls_api__id c, int l, const stream_data& cipher, unsigned seq, const stream_data& ad);
    virtual void net__impl__handle_recv(endpoint_id prm__V0, int s, const ip__endpoint& src, const prot__arr& x);
    virtual int ext__net__impl__open(endpoint_id prm__V0, const ip__endpoint& addr);
    virtual int ext__net__open(endpoint_id me, const ip__endpoint& addr);
    virtual void net__send(endpoint_id me, int s, const ip__endpoint& dst, const prot__arr& x);
    virtual void ext__net__recv(endpoint_id me, int s, const ip__endpoint& src, const prot__arr& x);
    virtual ip__endpoint ext__endpoint_id_addr(endpoint_id ep_id);
    virtual quic_server_test_stream::cid ext__double_cid(quic_server_test_stream::cid c);
    virtual void ext__show_latest_rtt(int t, quic_server_test_stream::cid c);
    virtual int ext__pow(int x, int y);
    virtual int ext__abs(int x);
    virtual int ext__get_pto_time_and_space(const ip__endpoint& dst, quic_server_test_stream::cid dcid, quic_packet_type& pto_space);
    virtual int ext__get_loss_time_space(quic_packet_type& space);
    virtual bool ext__peer_completed_address_validation(const ip__endpoint& dst, quic_server_test_stream::cid dcid);
    virtual void ext__set_loss_detection_timer(const ip__endpoint& dst, quic_server_test_stream::cid dcid);
    virtual void ext__on_loss_detection_timeout(const ip__endpoint& dst, quic_server_test_stream::cid dcid);
    virtual void ext__show_need_sent_ack_eliciting_initial_packet();
    virtual void ext__show_need_sent_ack_eliciting_handshake_packet();
    virtual void ext__show_need_sent_ack_eliciting_application_packet();
    virtual void ext__detect_and_remove_lost_packets(quic_packet_type pn_space, quic_server_test_stream::cid dcid);
    virtual void ext__show_loss_time_update(int t, quic_packet_type pn_space);
    virtual void ext__on_datagram_received(const ip__endpoint& dst, quic_server_test_stream::cid dcid, const stream_data& datagram);
    virtual void ext__show_loss_detection_timeout();
    virtual void ext__detect_and_remove_acked_packets(unsigned largest_acked, quic_packet_type pn_space);
    virtual void on_ack_received(const ip__endpoint& dst, unsigned largest_acked, int ack_delay, quic_packet_type pn_space);
    virtual void ext__show_detect_and_remove_lost_packets_size(quic_packet_type pn_space, unsigned long long lost_packets_end);
    virtual void ext__show_on_ack_received(unsigned largest_acked, int ack_delay, quic_packet_type pn_space);
    virtual bool ext__includes_ack_eliciting(quic_packet_type pn_space);
    virtual void ext__update_rtt(int ack_delay, quic_server_test_stream::cid dcid);
    virtual void ext__show_update_rtt(int latest_rtt, int min_rtt, int smoothed_rtt, int rttvar, quic_server_test_stream::cid dcid);
    virtual void on_pn_space_discarded(const ip__endpoint& dst, quic_server_test_stream::cid dcid, quic_packet_type pn_space);
    virtual void ext__show_on_pn_space_discarded(quic_packet_type pn_space);
    virtual void on_packet_sent(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet& pkt, unsigned long long sent_bytes);
    virtual void ext__on_packet_received(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet& pkt, unsigned long long sent_bytes);
    virtual void ext__show_get_loss_time_space(int t, quic_packet_type s);
    virtual void ext__show_detect_and_remove_lost_packets(int lost_sent_time, int loss_delay, unsigned long long sent_packets_size);
    virtual void ext__show_detect_and_remove_acked_packets(unsigned largest_acked, unsigned long long sent_packets_size, unsigned long long newly_acked_packets_end, unsigned long long sent_packets_end);
    virtual void ext__show_on_packet_sent(unsigned long long sent_packets_end, unsigned sent_packets_packet_number, int sent_packets_time_sent, bool sent_packets_ack_eliciting, bool sent_packets_in_flight, unsigned long long sent_packets_sent_bytes, bool ack_eliciting_packet_in_flight);
    virtual void ext__show_on_packet_received(unsigned long long sent_packets_end, unsigned sent_packets_packet_number, int sent_packets_time_sent, bool sent_packets_ack_eliciting, bool sent_packets_in_flight, unsigned long long sent_packets_sent_bytes);
    virtual void ext__show_include_ack_eliciting(bool res, quic_packet_type pn_space);
    virtual void ext__show_largest_acked_packet(unsigned largest_acked, unsigned largest_acked2d, quic_packet_type pn_space);
    virtual void ext__show_loss_detection_timer(int loss_detection_timer);
    virtual void ext__show_get_pto_time_and_space(int pto_timeout_res, quic_packet_type pto_space);
    virtual void ext__show_time_of_last_ack_eliciting_packet(int time_of_last_ack_eliciting_packet, quic_packet_type ptype);
    virtual void ext__on_congestion_event(int sent_time_of_last_loss);
    virtual void ext__on_packets_acked(quic_packet_type pn_space);
    virtual void ext__on_packet_acked(const quic_packet& acked_packet);
    virtual void ext__on_packets_lost(quic_packet_type pn_space);
    virtual void ext__remove_from_bytes_in_flight(quic_packet_type pn_space);
    virtual void ext__server__set_tls_id(quic_server_test_stream::tls_api__id e);
    virtual void ext__server__behavior(endpoint_id host, int s, const ip__endpoint& src, const prot__arr& pkts);
    virtual void ext__server__show_data_received(unsigned long long s);
    virtual void ext__server__show_data_sent(unsigned long long s);
    virtual void ext__server__show_rnum(unsigned s);
    virtual void client__set_ep(const ip__endpoint& e);
    virtual void ext__client__set_tls_id(quic_server_test_stream::tls_api__id e);
    virtual void ext__client__behavior(endpoint_id host, int s, const ip__endpoint& src, const prot__arr& pkts);
    virtual void ext__client__show_rnum(unsigned s);
    virtual void ext__second_client__set_tls_id(quic_server_test_stream::tls_api__id e);
    virtual void ext__cids__append(cids& a, quic_server_test_stream::cid v);
    virtual unsigned long long clients__client__idx__next(unsigned long long x);
    virtual unsigned long long ext__clients__client__idx__next(unsigned long long x);
    virtual void ext__clients__client__arr__append(clients__client__arr& a, const clients__client& v);
    virtual unsigned long long ext__servers__server__idx__next(unsigned long long x);
    virtual void ext__servers__server__arr__append(servers__server__arr& a, const servers__server& v);
    virtual void ext__recv_packet(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const quic_packet& pkt);
    virtual void ext__padding_packet_event(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const stream_data& pkt);
    virtual void ext__undecryptable_packet_event(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const stream_data& pkt);
    virtual void ext__on_purpose_lost_packet_event(endpoint_id host, const ip__endpoint& src, const prot__arr& pkt);
    virtual void ext__undefined_host_error(endpoint_id host, int s, const ip__endpoint& src);
    virtual void ext__show_last_datagram_size(unsigned long long size);
    virtual void ext__show_socket_debug_event(int n);
    virtual void ext__show_biatch_debug_event(const ip__endpoint& src);
    virtual void show_set_initial_keys(const stream_data& ik, quic_server_test_stream::tls_api__id id);
    virtual void recv_vn_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_vn& spkt);
    virtual void recv_retry_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_retry& spkt);
    virtual void recv_0rtt_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_0rtt& spkt);
    virtual void version_not_found_event();
    virtual quic_packet_type ext__packet_encryption_level(const prot__header_info& h);
    virtual quic_packet_type ext__packet_encryption_level_up(const prot__header_info& h);
    virtual quic_server_test_stream::cid ext__packet_scid(const prot__header_info& h);
    virtual unsigned reference_pkt_num(const stream_data& spkt, bool decrypt);
    virtual unsigned ext__reference_pkt_num(const stream_data& spkt, bool decrypt);
    virtual bool ext__is_padding_packet(const stream_data& spkt);
    virtual stream_data pkt_serdes__to_bytes(const quic_packet& x);
    virtual quic_packet ext__pkt_serdes__from_bytes(const stream_data& y);
    virtual stream_data pkt_serdes_vn__to_bytes(const quic_packet_vn& x);
    virtual quic_packet_vn pkt_serdes_vn__from_bytes(const stream_data& y);
    virtual stream_data pkt_serdes_retry__to_bytes(const quic_packet_retry& x);
    virtual quic_packet_retry pkt_serdes_retry__from_bytes(const stream_data& y);
    virtual stream_data pkt_serdes_0rtt__to_bytes(const quic_packet_0rtt& x);
    virtual quic_packet_0rtt pkt_serdes_0rtt__from_bytes(const stream_data& y);
    virtual stream_data cid_to_bytes(quic_server_test_stream::cid c, unsigned len);
    virtual stream_data ext__cid_to_bytes(quic_server_test_stream::cid c, unsigned len);
    virtual unsigned long long seqnum_to_streampos(unsigned c);
    virtual unsigned long long ext__seqnum_to_streampos(unsigned c);
    virtual unsigned ext__streampos_to_seqnum(unsigned long long c);
    virtual unsigned dcid_size_cl(bool cond);
    virtual unsigned long long scid_size_pos(bool cond);
    virtual unsigned long long dcid_size_pos(bool cond);
    virtual quic_server_test_stream::cid bytes_to_cid(const stream_data& bytes);
    virtual quic_server_test_stream::cid ext__bytes_to_cid(const stream_data& bytes);
    virtual unsigned bytes_to_version(const stream_data& bytes);
    virtual unsigned ext__bytes_to_version(const stream_data& bytes);
    virtual quic_server_test_stream::itoken bytes_to_itoken(const stream_data& bytes);
    virtual void export_length_cid_extension(unsigned long long dcil, unsigned long long scil);
    virtual void export_length_cid(unsigned long long dcil, unsigned long long scil);
    virtual tls_extensions tls_extensions__empty();
    virtual tls_extensions ext__tls_extensions__empty();
    virtual void tls_extensions__append(tls_extensions& a, quic_server_test_stream::tls__extension v);
    virtual void ext__tls_extensions__append(tls_extensions& a, quic_server_test_stream::tls__extension v);
    virtual endpoint_id endpoint_to_pid(const ip__endpoint& src);
    virtual ip__endpoint ext__socket_endpoint(endpoint_id host, int s);
    virtual int endpoint_to_socket(const ip__endpoint& src);
    virtual ip__endpoint ext__tls_id_to_src(quic_server_test_stream::tls_api__id tls_id);
    virtual ip__endpoint ext__tls_id_to_dst(quic_server_test_stream::tls_api__id tls_id);
    virtual quic_server_test_stream::cid ext__tls_id_to_cid(quic_server_test_stream::tls_api__id tls_id);
    virtual bool dst_is_generated_tls(const ip__endpoint& dst);
    virtual quic_server_test_stream::tls_api__id src_tls_id(const ip__endpoint& src);
    virtual quic_server_test_stream::tls_api__id ext__src_tls_id(const ip__endpoint& src);
    virtual stream_data ext__http_request_file__read();
    virtual void ext__client_send_event(ip__endpoint src, ip__endpoint dst, quic_server_test_stream::cid dcid, unsigned s, unsigned long long end);
    virtual void show_tls_send_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, const stream_data& data, unsigned long long pos, quic_packet_type e, quic_server_test_stream::tls_api__id tls_id);
    virtual void ext__clear_packet(const ip__endpoint& src, const ip__endpoint& dst, unsigned rnum, const stream_data& pkt);
    virtual quic_transport_parameters make_transport_parameters();
    virtual quic_transport_parameters ext__make_transport_parameters();
    virtual void time_api__c_timer__start();
    virtual void ext__time_api__c_timer__start();
    virtual void time_api__c_timer__timeout();
    virtual int time_api__c_timer__now_sec();
    virtual int time_api__c_timer__now_micros();
    virtual int ext__time_api__c_timer__now_micros();
    virtual int time_api__c_timer__now_millis();
    virtual int time_api__c_timer__now_micros_last_bp();
    virtual int time_api__c_timer__now_millis_last_bp();
    virtual void time_api__chrono_timer__start();
    virtual void time_api__chrono_timer__timeout();
    virtual int time_api__chrono_timer__now_micros();
    virtual int time_api__chrono_timer__now_millis();
    virtual int time_api__chrono_timer__now_micros_last_bp();
    virtual int time_api__chrono_timer__now_millis_last_bp();
    virtual int ext__milliseconds_to_microseconds(int delay);
    virtual void _finalize();
    virtual void ext___finalize();
    virtual void imp__prot__show_token_len(unsigned long long ver);
    virtual void imp__prot__show_header(const prot__header_info& h);
    virtual void imp__show_test();
    virtual void imp__show_initial_request_initial();
    virtual void imp__show_detect_and_remove_lost_packets(int lost_sent_time, int loss_delay, unsigned long long sent_packets_size);
    virtual void imp__show_ack_eliciting_threshold_current_val(unsigned long long val);
    virtual void imp__ack_freq_generated();
    virtual void imp__show_tls_send_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, const stream_data& data, unsigned long long pos, quic_packet_type e, quic_server_test_stream::tls_api__id tls_id);
    virtual void imp__show_latest_rtt(int t, quic_server_test_stream::cid c);
    virtual void imp__show_include_ack_eliciting(bool res, quic_packet_type pn_space);
    virtual void imp__recv_vn_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_vn& spkt);
    virtual void imp__show_socket_debug_event(int n);
    virtual void imp__show_largest_acked_packet(unsigned largest_acked, unsigned largest_acked2d, quic_packet_type pn_space);
    virtual void imp__undecryptable_packet_event(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const stream_data& pkt);
    virtual void imp__show_loss_detection_timer(int loss_detection_timer);
    virtual void imp__padding_packet_event(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const stream_data& pkt);
    virtual void imp__show_detect_and_remove_lost_packets_size(quic_packet_type pn_space, unsigned long long lost_packets_end);
    virtual void imp__show_biatch_debug_event(const ip__endpoint& src);
    virtual void imp__show_num_ack_pkt(unsigned long long s);
    virtual void imp__show_get_loss_time_space(int t, quic_packet_type s);
    virtual void imp__show_on_pn_space_discarded(quic_packet_type pn_space);
    virtual void imp__show_tls_keys_established_event(quic_server_test_stream::cid scid, quic_packet_type e);
    virtual void imp__show_set_initial_keys(const stream_data& ik, quic_server_test_stream::tls_api__id id);
    virtual void imp__show_retransmit_lost_packet(const frame__arr& paylo);
    virtual void imp__show_on_ack_received(unsigned largest_acked, int ack_delay, quic_packet_type pn_space);
    virtual void imp__server__show_data_received(unsigned long long s);
    virtual void imp__on_purpose_lost_packet_event(endpoint_id host, const ip__endpoint& src, const prot__arr& pkt);
    virtual void imp__recv_retry_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_retry& spkt);
    virtual void imp__app_server_open_event_retry(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void imp__show_on_packet_received(unsigned long long sent_packets_end, unsigned sent_packets_packet_number, int sent_packets_time_sent, bool sent_packets_ack_eliciting, bool sent_packets_in_flight, unsigned long long sent_packets_sent_bytes);
    virtual void imp__show_seqnum_to_streampos(unsigned long long p);
    virtual void imp__show_queued_frames(quic_server_test_stream::cid scid, const frame__arr& queued_frames);
    virtual void imp__app_server_open_event_vn(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void imp__show_get_pto_time_and_space(int pto_timeout_res, quic_packet_type pto_space);
    virtual void imp__server__show_rnum(unsigned s);
    virtual void imp__server__show_data_sent(unsigned long long s);
    virtual void imp__show_time_of_last_ack_eliciting_packet(int time_of_last_ack_eliciting_packet, quic_packet_type ptype);
    virtual void imp__app_server_open_event_0rtt(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void imp__show_ack_generated();
    virtual void imp__show_probe_idle_timeout(int e);
    virtual void imp__show_update_rtt(int latest_rtt, int min_rtt, int smoothed_rtt, int rttvar, quic_server_test_stream::cid dcid);
    virtual void imp__client__show_rnum(unsigned s);
    virtual void imp__version_not_found_event();
    virtual void imp__clear_packet(const ip__endpoint& src, const ip__endpoint& dst, unsigned rnum, const stream_data& pkt);
    virtual void imp__show_seqnum(unsigned p);
    virtual void imp__recv_packet(endpoint_id host, const ip__endpoint& src, const ip__endpoint& dst, const quic_packet& pkt);
    virtual void imp__infer_frame(quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid, quic_server_test_stream::frame f);
    virtual void imp__show_num_ack_eliciting_pkt(unsigned long long s);
    virtual void imp__show_detect_and_remove_acked_packets(unsigned largest_acked, unsigned long long sent_packets_size, unsigned long long newly_acked_packets_end, unsigned long long sent_packets_end);
    virtual void imp__show_pkt_num(unsigned p);
    virtual void imp__is_generating(bool b);
    virtual void imp__show_is_retransmitted(unsigned long long p, unsigned c_time);
    virtual void imp__max_idle_timeout_update(int e);
    virtual void imp__show_loss_detection_timeout();
    virtual void imp__app_server_open_event_1rtt(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::cid scid, quic_server_test_stream::cid dcid);
    virtual void imp__show_loss_time_update(int t, quic_packet_type pn_space);
    virtual void imp__show_current_idle_timeout(int e);
    virtual void imp__show_need_sent_ack_eliciting_handshake_packet();
    virtual void imp__show_need_sent_ack_eliciting_application_packet();
    virtual void imp__show_connection_timeout(int idle_timeout, int max_idle_timeout_used, int pto_timeout);
    virtual void imp__show_current_time(int t);
    virtual void imp__show_need_sent_ack_eliciting_initial_packet();
    virtual void imp__respect_idle_timeout_none();
    virtual void imp__tls__handshake_event(const ip__endpoint& src, const ip__endpoint& dst, quic_server_test_stream::tls__handshake h);
    virtual void imp__recv_0rtt_pkt(const ip__endpoint& src, const ip__endpoint& dst, const quic_packet_0rtt& spkt);
    virtual void imp__show_on_packet_sent(unsigned long long sent_packets_end, unsigned sent_packets_packet_number, int sent_packets_time_sent, bool sent_packets_ack_eliciting, bool sent_packets_in_flight, unsigned long long sent_packets_sent_bytes, bool ack_eliciting_packet_in_flight);
    virtual void imp__show_ack_credit(quic_server_test_stream::cid c, unsigned p, bool eli, bool non_ack, unsigned pp);
    virtual void imp__show_ack_delay_exponent(int e);
    virtual void imp__show_last_datagram_size(unsigned long long size);
    virtual void imp__undefined_host_error(endpoint_id host, int s, const ip__endpoint& src);
    virtual void imp__show_ack_eliciting_threshold_val(unsigned long long val);
    virtual void imp__show_max_ack_delay(int e);
    virtual void imp__is_ack_frequency_respected(bool b);
    void __tick(int timeout);
};
inline bool operator ==(const quic_server_test_stream::tls__handshake &s, const quic_server_test_stream::tls__handshake &t);;
inline bool operator ==(const quic_server_test_stream::tls__extension &s, const quic_server_test_stream::tls__extension &t);;
inline bool operator ==(const quic_server_test_stream::frame &s, const quic_server_test_stream::frame &t);;
inline bool operator ==(const quic_server_test_stream::transport_parameter &s, const quic_server_test_stream::transport_parameter &t);;
inline bool operator ==(const quic_server_test_stream::tls__unknown_extension &s, const quic_server_test_stream::tls__unknown_extension &t){
    return ((s.etype == t.etype) && (s.content == t.content));
}
inline bool operator ==(const quic_server_test_stream::tls__early_data &s, const quic_server_test_stream::tls__early_data &t){
    return ((s.max_early_data_size == t.max_early_data_size));
}
inline bool operator ==(const quic_server_test_stream::tls__end_of_early_data &s, const quic_server_test_stream::tls__end_of_early_data &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::tls__psk_key_exchange_modes &s, const quic_server_test_stream::tls__psk_key_exchange_modes &t){
    return ((s.content == t.content));
}
inline bool operator ==(const quic_server_test_stream::tls__psk_identity &s, const quic_server_test_stream::tls__psk_identity &t){
    return ((s.identity == t.identity) && (s.obfuscated_ticket_age == t.obfuscated_ticket_age));
}
inline bool operator ==(const quic_server_test_stream::tls__pre_shared_key_client &s, const quic_server_test_stream::tls__pre_shared_key_client &t){
    return ((s.psk_identities == t.psk_identities) && (s.psk_binder == t.psk_binder));
}
inline bool operator ==(const quic_server_test_stream::tls__pre_shared_key_server &s, const quic_server_test_stream::tls__pre_shared_key_server &t){
    return ((s.selected_identity == t.selected_identity));
}
inline bool operator ==(const quic_server_test_stream::tls__random &s, const quic_server_test_stream::tls__random &t){
    return ((s.gmt_unix_time == t.gmt_unix_time) && (s.random_bytes == t.random_bytes));
}
inline bool operator ==(const quic_server_test_stream::tls__client_hello &s, const quic_server_test_stream::tls__client_hello &t){
    return ((s.client_version == t.client_version) && (s.rand_info == t.rand_info) && (s.session_id == t.session_id) && (s.cipher_suites == t.cipher_suites) && (s.compression_methods == t.compression_methods) && (s.extensions == t.extensions));
}
inline bool operator ==(const quic_server_test_stream::tls__server_hello &s, const quic_server_test_stream::tls__server_hello &t){
    return ((s.server_version == t.server_version) && (s.rand_info == t.rand_info) && (s.session_id == t.session_id) && (s.the_cipher_suite == t.the_cipher_suite) && (s.the_compression_method == t.the_compression_method) && (s.extensions == t.extensions));
}
inline bool operator ==(const quic_server_test_stream::tls__new_session_ticket &s, const quic_server_test_stream::tls__new_session_ticket &t){
    return ((s.ticket_lifetime == t.ticket_lifetime) && (s.ticket_age_add == t.ticket_age_add) && (s.ticket_nonce == t.ticket_nonce) && (s.ticket == t.ticket) && (s.extensions == t.extensions));
}
inline bool operator ==(const quic_server_test_stream::tls__encrypted_extensions &s, const quic_server_test_stream::tls__encrypted_extensions &t){
    return ((s.extensions == t.extensions));
}
inline bool operator ==(const quic_server_test_stream::tls__unknown_message &s, const quic_server_test_stream::tls__unknown_message &t){
    return ((s.mtype == t.mtype) && (s.unknown_message_bytes == t.unknown_message_bytes));
}
inline bool operator ==(const quic_server_test_stream::tls__finished &s, const quic_server_test_stream::tls__finished &t){
    return ((s.mtype == t.mtype) && (s.unknown_message_bytes == t.unknown_message_bytes));
}

bool operator ==(const quic_server_test_stream::tls__handshake &s, const quic_server_test_stream::tls__handshake &t){
    if (s.tag != t.tag) return false;
    switch (s.tag) {
        case 0: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__client_hello >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__client_hello >(t);
        case 1: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__server_hello >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__server_hello >(t);
        case 2: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__new_session_ticket >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__new_session_ticket >(t);
        case 3: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__encrypted_extensions >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__encrypted_extensions >(t);
        case 4: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__unknown_message >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__unknown_message >(t);
        case 5: return quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__finished >(s) == quic_server_test_stream::tls__handshake::unwrap< quic_server_test_stream::tls__finished >(t);

    }
    return true;
}
inline bool operator ==(const quic_server_test_stream::ip__endpoint &s, const quic_server_test_stream::ip__endpoint &t){
    return ((s.protocol == t.protocol) && (s.addr == t.addr) && (s.port == t.port) && (s.interface == t.interface));
}
inline bool operator ==(const quic_server_test_stream::tls__handshake_parser__result &s, const quic_server_test_stream::tls__handshake_parser__result &t){
    return ((s.pos == t.pos) && (s.value == t.value));
}
inline bool operator ==(const quic_server_test_stream::frame__ping &s, const quic_server_test_stream::frame__ping &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::frame__ack__range &s, const quic_server_test_stream::frame__ack__range &t){
    return ((s.gap == t.gap) && (s.ranges == t.ranges));
}
inline bool operator ==(const quic_server_test_stream::frame__ack &s, const quic_server_test_stream::frame__ack &t){
    return ((s.largest_acked == t.largest_acked) && (s.ack_delay == t.ack_delay) && (s.ack_ranges == t.ack_ranges));
}
inline bool operator ==(const quic_server_test_stream::frame__ack_ecn__range &s, const quic_server_test_stream::frame__ack_ecn__range &t){
    return ((s.gap == t.gap) && (s.ranges == t.ranges));
}
inline bool operator ==(const quic_server_test_stream::frame__ack_ecn &s, const quic_server_test_stream::frame__ack_ecn &t){
    return ((s.largest_acked == t.largest_acked) && (s.ack_delay == t.ack_delay) && (s.ack_ranges == t.ack_ranges) && (s.ecnp == t.ecnp) && (s.ect0 == t.ect0) && (s.ect1 == t.ect1) && (s.ecn_ce == t.ecn_ce));
}
inline bool operator ==(const quic_server_test_stream::frame__rst_stream &s, const quic_server_test_stream::frame__rst_stream &t){
    return ((s.id == t.id) && (s.err_code == t.err_code) && (s.final_offset == t.final_offset));
}
inline bool operator ==(const quic_server_test_stream::frame__stop_sending &s, const quic_server_test_stream::frame__stop_sending &t){
    return ((s.id == t.id) && (s.err_code == t.err_code));
}
inline bool operator ==(const quic_server_test_stream::frame__crypto &s, const quic_server_test_stream::frame__crypto &t){
    return ((s.offset == t.offset) && (s.length == t.length) && (s.data == t.data));
}
inline bool operator ==(const quic_server_test_stream::frame__new_token &s, const quic_server_test_stream::frame__new_token &t){
    return ((s.length == t.length) && (s.data == t.data));
}
inline bool operator ==(const quic_server_test_stream::frame__stream &s, const quic_server_test_stream::frame__stream &t){
    return ((s.off == t.off) && (s.len == t.len) && (s.fin == t.fin) && (s.id == t.id) && (s.offset == t.offset) && (s.length == t.length) && (s.data == t.data));
}
inline bool operator ==(const quic_server_test_stream::frame__max_data &s, const quic_server_test_stream::frame__max_data &t){
    return ((s.pos == t.pos));
}
inline bool operator ==(const quic_server_test_stream::frame__max_stream_data &s, const quic_server_test_stream::frame__max_stream_data &t){
    return ((s.id == t.id) && (s.pos == t.pos));
}
inline bool operator ==(const quic_server_test_stream::frame__max_streams &s, const quic_server_test_stream::frame__max_streams &t){
    return ((s.id == t.id));
}
inline bool operator ==(const quic_server_test_stream::frame__max_streams_bidi &s, const quic_server_test_stream::frame__max_streams_bidi &t){
    return ((s.id == t.id));
}
inline bool operator ==(const quic_server_test_stream::frame__data_blocked &s, const quic_server_test_stream::frame__data_blocked &t){
    return ((s.pos == t.pos));
}
inline bool operator ==(const quic_server_test_stream::frame__stream_data_blocked &s, const quic_server_test_stream::frame__stream_data_blocked &t){
    return ((s.id == t.id) && (s.pos == t.pos));
}
inline bool operator ==(const quic_server_test_stream::frame__streams_blocked &s, const quic_server_test_stream::frame__streams_blocked &t){
    return ((s.id == t.id));
}
inline bool operator ==(const quic_server_test_stream::frame__streams_blocked_bidi &s, const quic_server_test_stream::frame__streams_blocked_bidi &t){
    return ((s.id == t.id));
}
inline bool operator ==(const quic_server_test_stream::frame__new_connection_id &s, const quic_server_test_stream::frame__new_connection_id &t){
    return ((s.seq_num == t.seq_num) && (s.retire_prior_to == t.retire_prior_to) && (s.length == t.length) && (s.scid == t.scid) && (s.token == t.token));
}
inline bool operator ==(const quic_server_test_stream::frame__retire_connection_id &s, const quic_server_test_stream::frame__retire_connection_id &t){
    return ((s.seq_num == t.seq_num));
}
inline bool operator ==(const quic_server_test_stream::frame__path_challenge &s, const quic_server_test_stream::frame__path_challenge &t){
    return ((s.data == t.data));
}
inline bool operator ==(const quic_server_test_stream::frame__path_response &s, const quic_server_test_stream::frame__path_response &t){
    return ((s.data == t.data));
}
inline bool operator ==(const quic_server_test_stream::frame__connection_close &s, const quic_server_test_stream::frame__connection_close &t){
    return ((s.err_code == t.err_code) && (s.frame_type == t.frame_type) && (s.reason_phrase_length == t.reason_phrase_length) && (s.reason_phrase == t.reason_phrase));
}
inline bool operator ==(const quic_server_test_stream::frame__application_close &s, const quic_server_test_stream::frame__application_close &t){
    return ((s.err_code == t.err_code) && (s.reason_phrase_length == t.reason_phrase_length) && (s.reason_phrase == t.reason_phrase));
}
inline bool operator ==(const quic_server_test_stream::frame__handshake_done &s, const quic_server_test_stream::frame__handshake_done &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::frame__ack_frequency &s, const quic_server_test_stream::frame__ack_frequency &t){
    return ((s.seq_num == t.seq_num) && (s.ack_eliciting_threshold == t.ack_eliciting_threshold) && (s.request_max_ack_delay == t.request_max_ack_delay) && (s.reordering_threshold == t.reordering_threshold));
}
inline bool operator ==(const quic_server_test_stream::frame__immediate_ack &s, const quic_server_test_stream::frame__immediate_ack &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::frame__unknown_frame &s, const quic_server_test_stream::frame__unknown_frame &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::frame__malicious_frame &s, const quic_server_test_stream::frame__malicious_frame &t){
    return ((s.data == t.data));
}

bool operator ==(const quic_server_test_stream::frame &s, const quic_server_test_stream::frame &t){
    if (s.tag != t.tag) return false;
    switch (s.tag) {
        case 0: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ping >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ping >(t);
        case 1: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack >(t);
        case 2: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_ecn >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_ecn >(t);
        case 3: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__rst_stream >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__rst_stream >(t);
        case 4: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stop_sending >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stop_sending >(t);
        case 5: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__crypto >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__crypto >(t);
        case 6: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_token >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_token >(t);
        case 7: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream >(t);
        case 8: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_data >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_data >(t);
        case 9: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_stream_data >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_stream_data >(t);
        case 10: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams >(t);
        case 11: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams_bidi >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__max_streams_bidi >(t);
        case 12: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__data_blocked >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__data_blocked >(t);
        case 13: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream_data_blocked >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__stream_data_blocked >(t);
        case 14: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked >(t);
        case 15: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked_bidi >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__streams_blocked_bidi >(t);
        case 16: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_connection_id >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__new_connection_id >(t);
        case 17: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__retire_connection_id >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__retire_connection_id >(t);
        case 18: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_challenge >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_challenge >(t);
        case 19: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_response >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__path_response >(t);
        case 20: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__connection_close >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__connection_close >(t);
        case 21: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__application_close >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__application_close >(t);
        case 22: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__handshake_done >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__handshake_done >(t);
        case 23: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_frequency >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__ack_frequency >(t);
        case 24: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__immediate_ack >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__immediate_ack >(t);
        case 25: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__unknown_frame >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__unknown_frame >(t);
        case 26: return quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__malicious_frame >(s) == quic_server_test_stream::frame::unwrap< quic_server_test_stream::frame__malicious_frame >(t);

    }
    return true;
}
inline bool operator ==(const quic_server_test_stream::quic_packet_vn &s, const quic_server_test_stream::quic_packet_vn &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.supported_version == t.supported_version));
}
inline bool operator ==(const quic_server_test_stream::original_destination_connection_id &s, const quic_server_test_stream::original_destination_connection_id &t){
    return ((s.dcid == t.dcid));
}
inline bool operator ==(const quic_server_test_stream::initial_max_stream_data_bidi_local &s, const quic_server_test_stream::initial_max_stream_data_bidi_local &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::initial_max_data &s, const quic_server_test_stream::initial_max_data &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::initial_max_stream_id_bidi &s, const quic_server_test_stream::initial_max_stream_id_bidi &t){
    return ((s.stream_id_16 == t.stream_id_16));
}
inline bool operator ==(const quic_server_test_stream::max_idle_timeout &s, const quic_server_test_stream::max_idle_timeout &t){
    return ((s.seconds_16 == t.seconds_16));
}
inline bool operator ==(const quic_server_test_stream::preferred_address &s, const quic_server_test_stream::preferred_address &t){
    return ((s.ip_addr == t.ip_addr) && (s.ip_port == t.ip_port) && (s.ip6_addr == t.ip6_addr) && (s.ip6_port == t.ip6_port) && (s.pcid_len == t.pcid_len) && (s.pcid == t.pcid) && (s.pref_token == t.pref_token));
}
inline bool operator ==(const quic_server_test_stream::max_packet_size &s, const quic_server_test_stream::max_packet_size &t){
    return ((s.stream_pos_16 == t.stream_pos_16));
}
inline bool operator ==(const quic_server_test_stream::stateless_reset_token &s, const quic_server_test_stream::stateless_reset_token &t){
    return ((s.data_8 == t.data_8));
}
inline bool operator ==(const quic_server_test_stream::ack_delay_exponent &s, const quic_server_test_stream::ack_delay_exponent &t){
    return ((s.exponent_8 == t.exponent_8));
}
inline bool operator ==(const quic_server_test_stream::initial_max_stream_id_uni &s, const quic_server_test_stream::initial_max_stream_id_uni &t){
    return ((s.stream_id_16 == t.stream_id_16));
}
inline bool operator ==(const quic_server_test_stream::disable_active_migration &s, const quic_server_test_stream::disable_active_migration &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::initial_max_stream_data_bidi_remote &s, const quic_server_test_stream::initial_max_stream_data_bidi_remote &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::initial_max_stream_data_uni &s, const quic_server_test_stream::initial_max_stream_data_uni &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::max_ack_delay &s, const quic_server_test_stream::max_ack_delay &t){
    return ((s.exponent_8 == t.exponent_8));
}
inline bool operator ==(const quic_server_test_stream::active_connection_id_limit &s, const quic_server_test_stream::active_connection_id_limit &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::initial_source_connection_id &s, const quic_server_test_stream::initial_source_connection_id &t){
    return ((s.scid == t.scid));
}
inline bool operator ==(const quic_server_test_stream::retry_source_connection_id &s, const quic_server_test_stream::retry_source_connection_id &t){
    return ((s.rcid == t.rcid));
}
inline bool operator ==(const quic_server_test_stream::loss_bits &s, const quic_server_test_stream::loss_bits &t){
    return ((s.unknown == t.unknown));
}
inline bool operator ==(const quic_server_test_stream::grease_quic_bit &s, const quic_server_test_stream::grease_quic_bit &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::enable_time_stamp &s, const quic_server_test_stream::enable_time_stamp &t){
    return ((s.stream_pos_32 == t.stream_pos_32));
}
inline bool operator ==(const quic_server_test_stream::min_ack_delay &s, const quic_server_test_stream::min_ack_delay &t){
    return ((s.exponent_8 == t.exponent_8));
}
inline bool operator ==(const quic_server_test_stream::version_information &s, const quic_server_test_stream::version_information &t){
    return ((s.chosen_version == t.chosen_version) && (s.other_version == t.other_version));
}
inline bool operator ==(const quic_server_test_stream::unknown_ignore &s, const quic_server_test_stream::unknown_ignore &t){
    return true;
}
inline bool operator ==(const quic_server_test_stream::unknown_transport_parameter &s, const quic_server_test_stream::unknown_transport_parameter &t){
    return ((s.unknown == t.unknown));
}

bool operator ==(const quic_server_test_stream::transport_parameter &s, const quic_server_test_stream::transport_parameter &t){
    if (s.tag != t.tag) return false;
    switch (s.tag) {
        case 0: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::original_destination_connection_id >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::original_destination_connection_id >(t);
        case 1: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_local >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_local >(t);
        case 2: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_data >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_data >(t);
        case 3: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_bidi >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_bidi >(t);
        case 4: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_idle_timeout >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_idle_timeout >(t);
        case 5: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::preferred_address >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::preferred_address >(t);
        case 6: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_packet_size >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_packet_size >(t);
        case 7: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::stateless_reset_token >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::stateless_reset_token >(t);
        case 8: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::ack_delay_exponent >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::ack_delay_exponent >(t);
        case 9: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_uni >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_id_uni >(t);
        case 10: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::disable_active_migration >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::disable_active_migration >(t);
        case 11: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_remote >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_bidi_remote >(t);
        case 12: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_uni >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_max_stream_data_uni >(t);
        case 13: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_ack_delay >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::max_ack_delay >(t);
        case 14: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::active_connection_id_limit >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::active_connection_id_limit >(t);
        case 15: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_source_connection_id >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::initial_source_connection_id >(t);
        case 16: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::retry_source_connection_id >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::retry_source_connection_id >(t);
        case 17: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::loss_bits >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::loss_bits >(t);
        case 18: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::grease_quic_bit >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::grease_quic_bit >(t);
        case 19: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::enable_time_stamp >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::enable_time_stamp >(t);
        case 20: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::min_ack_delay >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::min_ack_delay >(t);
        case 21: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::version_information >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::version_information >(t);
        case 22: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_ignore >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_ignore >(t);
        case 23: return quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_transport_parameter >(s) == quic_server_test_stream::transport_parameter::unwrap< quic_server_test_stream::unknown_transport_parameter >(t);

    }
    return true;
}
inline bool operator ==(const quic_server_test_stream::trans_params_struct &s, const quic_server_test_stream::trans_params_struct &t){
    return ((s.original_destination_connection_id__is_set == t.original_destination_connection_id__is_set) && (s.original_destination_connection_id__value == t.original_destination_connection_id__value) && (s.initial_max_stream_data_bidi_local__is_set == t.initial_max_stream_data_bidi_local__is_set) && (s.initial_max_stream_data_bidi_local__value == t.initial_max_stream_data_bidi_local__value) && (s.initial_max_data__is_set == t.initial_max_data__is_set) && (s.initial_max_data__value == t.initial_max_data__value) && (s.initial_max_stream_id_bidi__is_set == t.initial_max_stream_id_bidi__is_set) && (s.initial_max_stream_id_bidi__value == t.initial_max_stream_id_bidi__value) && (s.max_idle_timeout__is_set == t.max_idle_timeout__is_set) && (s.max_idle_timeout__value == t.max_idle_timeout__value) && (s.preferred_address__is_set == t.preferred_address__is_set) && (s.preferred_address__value == t.preferred_address__value) && (s.max_packet_size__is_set == t.max_packet_size__is_set) && (s.max_packet_size__value == t.max_packet_size__value) && (s.stateless_reset_token__is_set == t.stateless_reset_token__is_set) && (s.stateless_reset_token__value == t.stateless_reset_token__value) && (s.ack_delay_exponent__is_set == t.ack_delay_exponent__is_set) && (s.ack_delay_exponent__value == t.ack_delay_exponent__value) && (s.initial_max_stream_id_uni__is_set == t.initial_max_stream_id_uni__is_set) && (s.initial_max_stream_id_uni__value == t.initial_max_stream_id_uni__value) && (s.disable_active_migration__is_set == t.disable_active_migration__is_set) && (s.disable_active_migration__value == t.disable_active_migration__value) && (s.initial_max_stream_data_bidi_remote__is_set == t.initial_max_stream_data_bidi_remote__is_set) && (s.initial_max_stream_data_bidi_remote__value == t.initial_max_stream_data_bidi_remote__value) && (s.initial_max_stream_data_uni__is_set == t.initial_max_stream_data_uni__is_set) && (s.initial_max_stream_data_uni__value == t.initial_max_stream_data_uni__value) && (s.max_ack_delay__is_set == t.max_ack_delay__is_set) && (s.max_ack_delay__value == t.max_ack_delay__value) && (s.active_connection_id_limit__is_set == t.active_connection_id_limit__is_set) && (s.active_connection_id_limit__value == t.active_connection_id_limit__value) && (s.initial_source_connection_id__is_set == t.initial_source_connection_id__is_set) && (s.initial_source_connection_id__value == t.initial_source_connection_id__value) && (s.retry_source_connection_id__is_set == t.retry_source_connection_id__is_set) && (s.retry_source_connection_id__value == t.retry_source_connection_id__value) && (s.loss_bits__is_set == t.loss_bits__is_set) && (s.loss_bits__value == t.loss_bits__value) && (s.grease_quic_bit__is_set == t.grease_quic_bit__is_set) && (s.grease_quic_bit__value == t.grease_quic_bit__value) && (s.enable_time_stamp__is_set == t.enable_time_stamp__is_set) && (s.enable_time_stamp__value == t.enable_time_stamp__value) && (s.min_ack_delay__is_set == t.min_ack_delay__is_set) && (s.min_ack_delay__value == t.min_ack_delay__value) && (s.version_information__is_set == t.version_information__is_set) && (s.version_information__value == t.version_information__value) && (s.unknown_ignore__is_set == t.unknown_ignore__is_set) && (s.unknown_ignore__value == t.unknown_ignore__value) && (s.unknown_transport_parameter__is_set == t.unknown_transport_parameter__is_set) && (s.unknown_transport_parameter__value == t.unknown_transport_parameter__value));
}
inline bool operator ==(const quic_server_test_stream::quic_transport_parameters &s, const quic_server_test_stream::quic_transport_parameters &t){
    return ((s.transport_parameters == t.transport_parameters));
}

bool operator ==(const quic_server_test_stream::tls__extension &s, const quic_server_test_stream::tls__extension &t){
    if (s.tag != t.tag) return false;
    switch (s.tag) {
        case 0: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__unknown_extension >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__unknown_extension >(t);
        case 1: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__early_data >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__early_data >(t);
        case 2: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__end_of_early_data >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__end_of_early_data >(t);
        case 3: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__psk_key_exchange_modes >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__psk_key_exchange_modes >(t);
        case 4: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_client >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_client >(t);
        case 5: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_server >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::tls__pre_shared_key_server >(t);
        case 6: return quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::quic_transport_parameters >(s) == quic_server_test_stream::tls__extension::unwrap< quic_server_test_stream::quic_transport_parameters >(t);

    }
    return true;
}
inline bool operator ==(const quic_server_test_stream::quic_packet &s, const quic_server_test_stream::quic_packet &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.token == t.token) && (s.seq_num == t.seq_num) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::quic_packet_retry &s, const quic_server_test_stream::quic_packet_retry &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.token == t.token) && (s.integrity_token == t.integrity_token));
}
inline bool operator ==(const quic_server_test_stream::quic_packet_0rtt &s, const quic_server_test_stream::quic_packet_0rtt &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.seq_num == t.seq_num) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::quic_packet_coal_0rtt &s, const quic_server_test_stream::quic_packet_coal_0rtt &t){
    return ((s.ptype_i == t.ptype_i) && (s.pversion_i == t.pversion_i) && (s.dst_cid_i == t.dst_cid_i) && (s.src_cid_i == t.src_cid_i) && (s.token_i == t.token_i) && (s.seq_num_i == t.seq_num_i) && (s.payload_i == t.payload_i) && (s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.seq_num == t.seq_num) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::forged_protected_quic_packet &s, const quic_server_test_stream::forged_protected_quic_packet &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.token == t.token) && (s.protected_payload == t.protected_payload));
}
inline bool operator ==(const quic_server_test_stream::forged_quic_packet &s, const quic_server_test_stream::forged_quic_packet &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.token == t.token) && (s.seq_num == t.seq_num) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::forged_quic_packet_retry &s, const quic_server_test_stream::forged_quic_packet_retry &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.token == t.token) && (s.integrity_token == t.integrity_token));
}
inline bool operator ==(const quic_server_test_stream::forged_quic_packet_vn &s, const quic_server_test_stream::forged_quic_packet_vn &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.supported_version == t.supported_version));
}
inline bool operator ==(const quic_server_test_stream::replayed_quic_packet_0rtt &s, const quic_server_test_stream::replayed_quic_packet_0rtt &t){
    return ((s.ptype == t.ptype) && (s.pversion == t.pversion) && (s.dst_cid == t.dst_cid) && (s.src_cid == t.src_cid) && (s.seq_num == t.seq_num) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::prot__header_info &s, const quic_server_test_stream::prot__header_info &t){
    return ((s.hdr_long == t.hdr_long) && (s.hdr_type == t.hdr_type) && (s.dcid == t.dcid) && (s.scid == t.scid) && (s.payload_length == t.payload_length) && (s.token_length == t.token_length) && (s.payload_length_pos == t.payload_length_pos) && (s.pkt_num_pos == t.pkt_num_pos));
}
inline bool operator ==(const quic_server_test_stream::tls_api__upper__decrypt_result &s, const quic_server_test_stream::tls_api__upper__decrypt_result &t){
    return ((s.ok == t.ok) && (s.data == t.data) && (s.payload == t.payload));
}
inline bool operator ==(const quic_server_test_stream::clients__client &s, const quic_server_test_stream::clients__client &t){
    return ((s.ep == t.ep) && (s.tls_id == t.tls_id) && (s.enc_level == t.enc_level));
}
inline bool operator ==(const quic_server_test_stream::servers__server &s, const quic_server_test_stream::servers__server &t){
    return ((s.ep == t.ep) && (s.tls_id == t.tls_id) && (s.enc_level == t.enc_level));
}
