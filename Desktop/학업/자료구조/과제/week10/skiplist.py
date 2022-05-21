
from collections.abc import MutableMapping
import math, random

class SkipList(MutableMapping):
    # add additional slots as you need
    __slots__ = '_head', '_tail', '_n','_level'   

    #------------------------------- nested _Node class -------------------------------
    class _Node:
        __slots__ = '_key', '_value', '_prev', '_next', '_below', '_above'

        """Lightweight composite to store key-value pairs as map items."""
        def __init__(self, k, v, prev=None, next=None, below=None, above=None):
            self._key = k
            self._value = v
            self._prev = prev
            self._next = next
            self._below = below
            self._above = above

        def __eq__(self, other):               
            if other == None:
                return False
            return self._key == other._key   # compare items based on their keys

        def __ne__(self, other):
            return not (self == other)       # opposite of __eq__

        def __lt__(self, other):               
            return self._key < other._key    # compare items based on their keys
        

    def __init__(self):
        """Create an empty map."""
        self._head = self._Node(-math.inf, None, None, None, None, None)   # Head: the first node in a skip list
        self._tail = self._Node(math.inf, None, None, None, None, None)    # Tail: the last node in a skip list
        self._head._next = self._tail         # Initially, there's no item -> head is directly linked to the tail
        self._n = 0                              # Initially, there's no item, so _n = 0
        self._level=0
        
        
    def _get(self,k):
        p=self._head
        while p._below != None:
            p=p._below
            try:
                while k>=p._next._key:
                    p=p._next
            except:
                pass#끝
        return p
    
    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        p=self._get(k)
        if p==None:
            raise KeyError('The key {} is not found'.format(k))
        return p._value

    
    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        p = self._get(k)
        q = None
        c=self._CoinFlip()# 최소값 0
        if p._key == k:
            
            while p._above != None:
                p._value = v
                p = p._above

            p._value = v
            p._next._prev = p
        else:
            for i in range(c+1): 
                if i>=self._level:
                    self._level += 1
                    t = self._tail
                    s = self._head
                    self._head = self._Node(-math.inf, None, None, None, None, None)
                    
                    s._above = self._head#서로 이어주기
                    self._head._below = s
                    self._tail = self._Node(math.inf, None, self._head, None, t, None)
                    t._above = self._tail
                    self._head._next = self._tail

                if i == 0:
                    self._n += 1
                    q = self._Node(k,v,p, p._next, q, None)
                    #a=p._next
                    q._prev._next = q
                    q._next._prev = q
                    #p._next = q
                    #a._prev = q
                else:
                    while p._above == None:
                        p = p._prev
                    p = p._above
                    q2 = q
                    q = self._Node(k, v, p, p._next, q2, None)
                    q2._above = q
                    a = p._next
                    p._next = q
                    a._prev = q
        return q


    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""

        p = self._get(k)
        ret = 0
        if p == None:
            raise KeyError('The key {} is not found'.format(k))
        while p._above != None:
            p = p._above #꼭대기에서 시작


        while p._below != None:
            try:
                if p._prev._above == self._head and p._next._above == self._tail:
                    self._head = self._head._below
                    self._head._above = None
                    self._tail = self._tail._below
                    self._tail._above = None
            except:
                pass
            ret = p._value
            s = p._prev
            n = p._next
            
            s._next = n
            n._prev = s
            p._prev = None
            p._next = None
            p._above = None
            p = p._below
        s = p._prev
        n = p._next
        s._next = n
        n._prev = s
        p._prev = None
        p._next = None
        p._above = None
        self._n -= 1
        return ret

      
        
    def __len__(self):
        """Return number of items in the map."""
        return self._n

    def __iter__(self):                             
        """Generate iteration of the map's keys."""
        # hint: iterate over the base height (where the nodes that node._below is None)        
        node = self._head
        while node._below !=None:
            node = node._below
        node = node._next
        try:
            while node._next._key != math.inf:
                yield node._key
                node = node._next
            yield node._key
        except:
            pass
    
            
        #node = node._next
        # go down all the way to the bottom
        # yield node._key while node._next is not having math.inf as the key
        
    def _CoinFlip(self):
        i=-1
        s=-1
        while s != 1:
            i+=1
            s=random.randint(0,1)
        return i
        