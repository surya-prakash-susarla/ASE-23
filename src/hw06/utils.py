import math
import json
import collections
from globals import *
from node import Node
from pathlib import Path
import copy
from sym import Sym
 

def rnd(n, nPlaces = 3):
    """
    Rounds of the output to nPlaces places.
    """
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
    return (x2, y)

def show(node, cols, nPlaces, level = 0, is_mid=True):
    if node != None:
        print('|'*level, end=' ')
        if node.left == None:
            print(last(last(node.data.rows).cells))
        else:
            print("{c:.1f}".format(c=rnd(100*node.c)))
        show(node.left, cols, nPlaces, level+1, is_mid)
        show(node.right, cols, nPlaces, level+1, is_mid)

def get_repgrid_file_contents(filepath):
    filepath = (Path(__file__) / filepath).resolve()
    data = None
    with open(filepath) as file:
        data = json.load(file)
    return data

def last(list_values):
    return list_values[-1]

def tree(data, rows = None, above=None):
    input_rows = rows if rows != None else data.rows
    here = {}
    here['data'] = data.clone(input_rows)
    if len(input_rows) >= (2*(len(data.rows)))**global_options[K_MIN]:
        left, right, A, B, _, _ = data.half(input_rows)
        here['left'] = tree(data, left, A)
        here['right'] = tree(data, right, B)
    return here

def show_tree(tree, lvl=0):
    if tree:
         print('|'+'.'*lvl,len(tree['data'].rows), end=' ')
         if lvl == 0 or len(tree.keys()) == 1:
             print(tree['data'].stats())
         else:
             print("")
         if 'left' in tree:
             show_tree(tree['left'], lvl+1)
         if 'right' in tree:
             show_tree(tree['right'], lvl+1)

def many(row, new_size):
        row_len= len(row)
        temp=[]
        
        for i in range(new_size):
            j = rint(0,row_len-1)
            temp.append(row[j])
        return temp

def value (has ,  nB=None, nR=None , sGoal=None):
    if(sGoal==None):
        sGoal=True
    if nB==None:
        nB=1
    if nR==None:
        nR=1
    b=0
    r=0
    for x in has :
        if x==sGoal :
            b+=has[x]
        else:
            r+=has[x]
    b=b/(nB+0.0000000001)
    r=r/(nR+0.0000000001)
    return (b*b)/(b+r)

def prune(rule, maxSize):
    n = 0
    for key in rule.keys():
        n = n+1
        if len(rule) == maxSize[key]:
            n = n+1
            rule[key] = None
    if n > 0:
        return rule
    else:
        return None

def rule(ranges, maxSize):
    t = dict()
    for r in ranges:
        t[r[txt]]['lo'] = r['lo']
        t[r[txt]]['hi'] = r['hi']
    return prune(t, maxSize)

def showRule(rule):
    print("TODO - CHECK TYPE OF RANGE TO UPDATE THESE FUNCTIONS")
    def pretty(rang):
        return rang['lo'] if rang['hi'] == rang['lo'] else {'hi': rang['hi'], 'lo': rang['lo']}
    def merge(t0):
        t, j, left, right = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j+1]
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j = j+1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j = j+1
        return t if len(t0) == len(t) else merge(t)

    def merges(attr, ranges):
        temp = []
        for i in merge(sorted(ranges, lambda d: d['lo'])):
            temp.append(pretty(i))
        return temp, attr

    temp = []
    for i in rule:
        temp.append(merges(rule))
    return temp

def firstN(sorted_list, scoring_function):
    print("")
    print("TODO - IMPLEMENT FIRST N FUNCTION")
    def print_range(r):
        print(r)
    return None

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")
    
    def score(ranges):
        r = rule(ranges, maxSize)
        if r:
            showRule(r)
            bestr = selects(r, best.rows)
            restr = selects(r, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({'best': len(bestr), 'rest': len(restr)}), r
    
    tmp, maxSizes = [], []
    print("TODO - reimplement bins function for updated params")
    for ranges in data.bins(data.cols.x, {'best': best.rows, 'rest': rest.rows}):
        maxSizes[ranges[1].txt] = len(ranges)
        print("")
        for r in ranges:
            print(r['txt'], " ", r['lo'], " ", r['hi'])
            print("TODO - FIX RANGES BASED ON BINS OUTPUT")
            tmp.append({'range': r, 'max': len(ranges), 'val': v(range.y.has)})
    sorted_list = sorted(tmp, key = lambda d: d['val'], reverse=True)
    r, most = firstN(sort(tmp, gt, "val"), score)
    return r, most

