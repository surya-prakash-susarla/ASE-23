import collections
import math
class Sym:
    def __init__(self, at=0, txt = ""):
        self.at, self.txt = at, txt
        self.n = 0 #total number of elements in the stream
        self.has = collections.defaultdict(int) #the dictionary which stores values of each alphabet in the stream
        self.most, self.mode = 0, "" # self.mode contains the alphabet which is recurring the highest number of times and self.most is its count

    def print(self):
        has = self.has if len(self.has) > 0 else "{}"
        print_st = "Sym at : {}, has : {}, most : {}, txt: {}".format(self.at, has, self.most, self.txt)
        print(print_st)
        
    def add(self, value):
        if value != '?':
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
        for i in keys:
            self.entropy += fun(i/self.n)
        return -self.entropy
    
    def rnd(self,value, nPlaces):
        return value

    def dist(self, symbol_1, symbol_2):
        if symbol_1 == symbol_2 == '?':
            return 1 
        elif symbol_1 == symbol_2:
            return 0
        return 1
