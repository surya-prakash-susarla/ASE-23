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
          self.max = max(value, self.max)
    
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
