import collections
class Sym:
    def __init__(self):
        self.n = 0 #total number of elements in the stream
        self.has = collections.defaultdict(int) #the dictionary which stores values of each alphabet in the stream
        self.most, self.mode = 0, "" # self.mode contains the alphabet which is recurring the highest number of times and self.most is its count
        
    def add(self, value):
        if value.isalpha():
            self.n+=1
            self.has[value]+=1
            if self.has[value] > self.most:
                self.most, self.mode = self.has[value], value