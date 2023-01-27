import math

from globals import global_options, K_SEED, K_DEFAULT_SEED_VALUE

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

