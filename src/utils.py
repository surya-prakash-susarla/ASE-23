import math
def rnd(n, nPlaces = 3):
    """
    Rounds of the output to nPlaces places.
    """
    if nPlaces:
        mult = 10**nPlaces
    #return math.floor(n*mult+0.5)/mult
    return math.floor(n*mult)/mult

def rand(seed = 937162211, lo = 0, hi=1):
  seed = 16807*seed % 2147483647
  return lo+(hi-lo)*seed/2147483647

def rint(lo, hi):
  return math.floor(0.5+rand(lo,hi))