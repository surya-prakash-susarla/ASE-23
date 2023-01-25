import collections
import math
class Sym:
    def __init__(self, at=0, txt = ""):
        self.at, self.txt = at, txt
        self.n = 0 #total number of elements in the stream
        self.has = collections.defaultdict(int) #the dictionary which stores values of each alphabet in the stream
        self.most, self.mode = 0, "" # self.mode contains the alphabet which is recurring the highest number of times and self.most is its count
        
    def add(self, value):
        # TODO: CLEANUP - if value.isalpha():
        self.n+=1
        self.has[value]+=1
        if self.has[value] > self.most:
            self.most, self.mode = self.has[value], value
    
    def mid(self, value=0):
        return self.mode

    def div(self, value = 0, entropy =0):
        def fun(x):
            return x*math.log(x,2)
        self.entropy = 0
        keys = list(self.has.values())
        print(keys)
        for i in keys:
            self.entropy += fun(i/self.n)
        return -self.entropy
    
    def rnd(self,value, nPlaces):
        return value
