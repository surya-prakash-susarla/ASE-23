from sym import Sym 
class Range:
    def __init__(self, at, txt , x):
        self.at = at
        self.txt = txt
        self.max = x
        self.min = x
        #SYM object
        self.y = Sym(self.at, self.txt)

