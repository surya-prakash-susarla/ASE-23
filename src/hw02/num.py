from utils import rnd
class Num:
  
    def __init__(self, at=0, txt = ""):
        if txt and txt[-1] == '-':
          self.wt = -1
        elif txt and txt[-1] != '-':
          self.wt = 1
        self.at, self.txt = at, txt
        self.n, self.mu, self.m2 =0, 0, 0
        self.max, self.min = -1000000000000000, 1000000000000000
    
    def add(self, value):
        if type(value) == int or type(value) == float:
          self.n+=1
          d = value-self.mu
          self.mu += d/self.n
          self.m2 += d*(value-self.mu)
          self.min = min(value, self.min)
          self.max = min(value, self.max)
    
    def mid(self):
        return self.mu
    
    def div(self):
        if self.m2 < 0 or self.n < 2:
          return 0
        else:
          return ((self.m2)/(self.n -1))**0.5
    def rnd(self, value, nPlaces):
        return rnd(value, nPlaces)
