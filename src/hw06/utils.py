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

def value (has, nB=1, nR=1 , sGoal=True):
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
    for txt in rule:
        n = n+1
        if len(rule[txt]) == maxSize[txt]:
            n = n+1
            rule[txt] = None
    if n > 0:
        return rule
    else:
        return None

def rule(ranges, maxSize):
    t = dict()
    for r in ranges:
        t[r.txt] = {'max': r.max, 'min': r.min,'at':r.at}
    return prune(t, maxSize)

def showRule(rule):
    #print("inside show rule", rule)
    def pretty(rang):
        return rang['min'] if rang['max'] == rang['min'] else {'max': rang['max'], 'min': rang['min']}
    def merge(t0):
        # print('t0 : ', t0)

        # print("len of t0 : ", len(t0))
        t, j, left, right = [], 0,None,None
        
        while j+1 < len(t0):
            left, right = list(t0.values())[j], list(t0.values())[j+1]
            # print('t0 :', t0)
            # print('left : ', left)
            # print('right : ', right)
            if right and left['max'] == right['min']:
                left['max'] = right['max']
                j = j+1
            t.append({'min': left['min'], 'max': left['max']})
            j = j+1
        if j < len(t0):
            keys = list(t0.keys())
            t.append({'min': t0[keys[j]]['min'], 'max': t0[keys[j]]['max']})
        return t if len(t0) == len(t) else merge(t)

    def merges( ranges):
        # print("TODO: resolve attr")
        # print("\n\n ranges in merges:", ranges)
        if (len(ranges)>=2):
            ranges = sorted(ranges.items(), key = lambda d: d[1]['min'])
        if type(ranges) != dict:
            temp = {}
            for x in ranges:
                temp[x[0]] = x[1]
            ranges = temp
        # print('ranges  : ', ranges)
        temp = []
        for i in merge(ranges):
            temp.append(pretty(i))
        return temp

    temp = []
    for i in rule:
        temp.append(merges(rule))
    return temp

def firstN(sorted_list, scoring_function):
    print("")
    def print_range(r):
        for i in r :
            print(i['range'].txt,i['range'].min,i['range'].max, rnd(i['val']))
    print_range(sorted_list)
    first  = sorted_list[0]['val']
    def useful(ranges):
        if ranges['val'] >0.05 and ranges['val'] > first/10 :
            return ranges
    sorted_ranges= []
    for ranges in sorted_list:
        if(useful(ranges)):
            sorted_ranges.append(ranges) 
    out = []
    most = -1
    n= 1
    new_sorted_range=[]
    while n <= len(sorted_ranges):
        new_sorted_range.append(sorted_ranges[n-1]['range'])
        tmp,rule = scoring_function(new_sorted_range), None
        # print('tmp : ', tmp)
        # print('most : ', most) 
        if tmp and tmp[0]>most :
            most = tmp[0]
            out.append(tmp[1])
        n+=1
    print("returning out : ", out)
    print("returning most : " , most)
    return out, most

def selects(rule, rows):
    def disjunction(ranges, row):
        # print('ranges : ', ranges)
        for range in ranges:
            # print("range : ", range)
            lo,hi,at = range['min'], range['max'], range['at']
            x = rows.index(row)
            if x=='?':
                return True
            if lo == hi and lo == x :
                return True
            if lo<=x and x<hi:
                return True
        return False
    def conjunction(row):
        # print('in conjuction')
        # print('rule : ', rule)
        for ranges in rule.values():
            # print('conjunction range : ', ranges)
            if not disjunction([ranges],row) :
                return False
        return True
    selected_rows=[]
    for row in rows :
        if(conjunction(row)):
            selected_rows.append(row)
    return selected_rows

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows), len(rest.rows), "best")
    
    def score(ranges):
        r = rule(ranges, maxSizes)
        if r:
            showRule(r)
            bestr = selects(r, best.rows)
            restr = selects(r, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({'best': len(bestr), 'rest': len(restr)}), r
    
    tmp, maxSizes = [], {}
    for ranges in data.bins(data.cols.x, {'best': best.rows, 'rest': rest.rows}):
        maxSizes[ranges[0].txt] = len(ranges)
        print("")
        for r in ranges:
            print(r.txt, " ", r.min, " ", r.max)
            tmp.append({'range': r, 'max': len(ranges), 'val': v(r.y.has)})
    sorted_list = sorted(tmp, key = lambda d: d['val'], reverse=True)
    # print("sorted list : ", sorted_list)
    # print('*'*10)
    r, most = firstN(sorted_list, score)

    print("\n")
    #print("returning rule from xpln  : ", r)
    return r, most

def add(col, x, n = 1):
        def sym_(col,x,n):
            col.has[x]+=n
            if(col.has[x]>col.most):
                col.most = col.has[x]
                col.mode = x
            return col
        def num_(col,x):
            col.min = min(x,col.min)
            col.max = max(x,col.max)
            if( len(col.has)< K_MAX_DEFAULT_VALUE):
                col.ok= False 
                col.has.append(x)
            elif(rand() < K_MAX_DEFAULT_VALUE/col.n) :
                col.ok= False
                col.has[rint(0,len(col.has))]=x
        if x!='?':
            col.n +=n
            if isinstance(col, Sym):
                return sym_(col,x,n)
            else:
                return num_(col,x)

def extend(range , n,s):
        range.min = min(n, range.min)
        range.max = max(n, range.max)
        add(range.y,s)

def merge(col1, col2):
        new = copy.deepcopy(col1)
        if isinstance(col1, Sym):
            for x in col2.has:
                add(new, x,col2.has[x])
        else:
            for x in col2.has:
                add(new, col2.has[x])
            new.min = min(col1.min, col2.min)
            new.max = max(col1.max, col2.max)
        return new

def merged(col1, col2 ,nSmall , nFar):
    new  = merge(col1, col2)
    if (nSmall and col1.n< nSmall) or col2.n < nSmall :
        return new
    if nFar and (not isinstance(col1, Sym)) and abs(col1.mid-col2.mid)<nFar :
        return new
    if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
        return new

def merges(ranges0, nSmall, nFar):
    def noGaps(t):
        if t == []:
            return
        for j in range(1, len(t)):
            t[j].min = t[j-1].max
        t[0].min = -10000000000
        t[-1].max = 10000000000
        return t
    def try2merge(left, right,j):
        y = merged(left.y,right.y,nSmall,nFar)
        if y :
            j+=1
            left.max  = right.max
            left.y = y
        return j,left
    ranges1,j,here = [],0,None
    while j< len(ranges0):
        here = ranges0[j]
        if j+1< len(ranges0):
            j, here = try2merge(here, ranges0[j+1],j)
        j+=1
        ranges1.append(here)
    if len(ranges0) == len(ranges1):
        return noGaps(ranges0)
    return merges(ranges1,nSmall,nFar)

