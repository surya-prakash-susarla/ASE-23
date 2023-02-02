import math

from globals import global_options, K_SEED, K_DEFAULT_SEED_VALUE
from node import Node

def rnd(n, nPlaces = 3):
    """
    Rounds of the output to nPlaces places.
    """
    if nPlaces:
        mult = 10**nPlaces
    return math.floor(n*mult+0.5)/mult

def rand( lo = 0, hi=1, default_seed=math.inf):
  global global_options
  global_options[K_SEED] = int(global_options[K_SEED])
  if default_seed != math.inf:
    global_options[K_SEED] = default_seed 
  global_options[K_SEED] = (16807*global_options[K_SEED]) % 2147483647
  return lo+(hi-lo)*global_options[K_SEED]/2147483647

def rint(lo, hi):
  return math.floor(0.5+rand(lo,hi))

def extract_entities_from_csv_row(row) -> []:
    # NOTE: Splitting completed at parse run.
    return row

def is_name_numeric_header(name: str) -> bool:
    return ord(name[0]) in range(ord('A'), ord('Z')+1)

def is_name_symbolic_header(name: str) -> bool:
    return not is_name_numeric_header(name)

def is_goal_header(name: str) -> bool:
    return name[-1] in ['!', '+', '-']

def should_exclude_header(name: str) -> bool:
    return name[-1] == 'X'

def cosine(a, b, c) -> tuple[int, int]:
    x1 = (a*a + c*c - b*b) / (2*c + 0.00001)
    x2 = max(0, min(1, x1))
    y = (abs(a*a - x2*x2))**(0.5)
    # print("returning : ", (x2, y))
    return (x2, y)

def show(node, cols, nPlaces, level = 0, is_mid=True):
    if node != None:
        print('|'*level, end=' ')
        print(" ", len(node.data.rows), end=' ')
        if node.left == None or level == 0:
            stats = node.data.stats(nPlaces, node.data.cols.y, is_mid)
            # print("stats : ", stats)
            print(stats)
        else:
            print("")
        show(node.left, cols, nPlaces, level+1, is_mid)
        show(node.right, cols, nPlaces, level+1, is_mid)

