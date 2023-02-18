from utils import rnd, rand, rint
from globals import *

class Num:
    def __init__(self, at=0, txt = ""):
        if txt and txt[-1] == '-':
          self.wt = -1
        elif txt and txt[-1] != '-':
          self.wt = 1
        else:
          self.wt = 0
        self.at, self.txt = at, txt
        self.n, self.mu, self.m2 =0, 0, 0
        self.max, self.min = -1000000000000000, 1000000000000000
        self.has = []
        self.ok = True
        self.isSym=False 

    def print(self):
        print_st = "Num at : {}, hi : {}, lo : {}, m2 : {}, mu : {}, txt : {}, w : {}, n : {}, mid : {}"
        print_st = print_st.format(self.at, self.max, self.min, round(self.m2, 2), round(self.mu, 2), self.txt, self.wt, self.n, self.mid())
        print(print_st)
    
    def add(self, value):
        if type(value) == int or type(value) == float:
            self.n += 1
            all_count = len(self.has)
            pos = -1
            if all_count < global_options[K_MAX]:
                pos = -2
            elif rand() < (global_options[K_MAX]/ self.n):
                pos = rint(0, all_count)
            if pos == -2 or pos < all_count:
                if pos == -2:
                    self.has.append(value)
                else:
                    self.has[pos] = value
                d = value-self.mu
                self.mu += d/self.n
                self.m2 += d*(value-self.mu)
                self.min = min(value, self.min)
                self.max = max(value, self.max)
                self.ok = False
    
    def mid(self):
        return self.mu
    
    def div(self):
        if self.m2 < 0 or self.n < 2:
          return 0
        else:
          return ((self.m2)/(self.n -1))**0.5

    def rnd(self, value, nPlaces):
      if value == '?':
        return value
      return rnd(value, nPlaces)
    
    def norm(self, n):
      if n == '?':
        return n
      return (n-self.min)/(self.max - self.min+0.00001)

    def dist(self, n_1, n_2):
      if n_1 == '?' and n_2 == '?':
        return 1
      n1, n2 = self.norm(n_1), self.norm(n_2)
      if n1 =='?':
        if n2<0.5:
          n1 = 1
        else:
          n1 = 0
      if n2 == '?':
        if n1<0.5:
          n2 = 1
        else:
          n2 = 0
      return abs(n1 - n2)
