class Num:
    def __init__(self):
        self.n, self.mu, self.m2 =0, 0, 0
        self.max, self.min = -100000000000000, 100000000000000
    
    def add(self, value):
        if type(value) == int:
          self.n+=1
          d = value-self.mu
          self.mu += d/self.n
          self.m2 += d*(value-self.mu)
          self.min = min(value, self.min)
          self.max = min(value, self.max)