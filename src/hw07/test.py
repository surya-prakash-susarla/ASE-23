from sym import Sym
from num import Num
from utils import rand ,rint, rnd, show, show_tree, tree, value, xpln, showRule
from data import Data, rep_cols , rep_rows, rep_grid, rep_place, transpose,cliffsDelta
from csv import get_csv_rows
from collections import OrderedDict
from globals import *
from data import diffs

import copy

def test_xpln():
    data = Data(global_options[K_FILE])
    best, rest, evals = data.sway()
    rule, most = xpln(data, best, rest)
    print('*'*10)
    print("rule from xpln : ", rule)
    for r in rule:
        print(showRule(r))
    
    return True

def test_global_options() -> bool:
    print(global_options)
    return True

def test_rand() -> bool:
    global_options[K_SEED] = 1
    max_range = 1000
    t = []
    for i in range(1, max_range):
        t.append(rand(hi=100))
    global_options[K_SEED] = 1
    u = []
    for i in range(1, max_range):
        u.append(rand(hi=100))
    return (t==u)

def test_some() -> bool:
    global_options[K_MAX] = 32
    num1 = Num()
    for i in range(1, 10000):
        num1.add(i)
    print(num1.has)
    print('length : ', len(num1.has))
    return True

def test_clone() -> bool:
    data = Data(global_options[K_FILE])
    data2 = data.clone(data.rows)
    print(data.stats())
    print(data2.stats())
    return True

def test_dist() -> bool:
    data = Data(global_options[K_FILE])
    num = Num()
    for row in data.rows:
        num.add(data.dist(row, data.rows[0]))
    num.print()
    return True

def test_cliffs() -> bool:
    if (False == cliffsDelta([8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3])):
        print("False")
    else:
        print("1")

    if (True  == cliffsDelta([8,7,6,2,5,8,7,3], [9,9,7,8,10,9,6])):
        print("True")
    else:
        print("2")

    t1=[]
    t2=[]
    for i in range(1000):
        random_number = rand()
        t1.append(random_number)
    for i in range(1000):
        random_number = rand()
        t2.append(random_number**0.5)
    
    if(cliffsDelta(t1,t1)):
        print("3")
    else:
        print("False")
    if(cliffsDelta(t1,t2)):
        print("True")
    else:
        print("4")
    diff=False
    j=1.0
    while(diff==False):
        t3=[]
        for i in t1 :
            t3.append(i*j)
        diff = cliffsDelta(t1,t3)
        print('>',rnd(j),diff)
        j=j*1.025
    return True

def test_tree() -> bool:
    show_tree(tree(Data()))
    return True

def test_sway() -> bool:
    data = Data(global_options[K_FILE])
    best, rest, evals = data.sway()
    print("\n all ", data.stats())
    print("    ",   data.stats(is_mid = False))
    print("\nbest", best.stats())
    print("    ",   best.stats(is_mid = False))
    print("\nrest", rest.stats()) 
    print("    ",   rest.stats(is_mid = False))
    print("\n all ~= best?", diffs(best.cols.y, data.cols.y))
    print("best ~= rest?", diffs(best.cols.y, rest.cols.y))
    return True

def test_bins() -> bool:
    data = Data(global_options[K_FILE])
    best, rest, evals =data.sway()
    rowss={}
    rowss['best']= best.rows
    rowss['rest']= rest.rows
    b4=None
     
    for t in (data.bins(data.cols.x,rowss)):
        for k in t:
            if k.txt != b4 :
                print(" ")
            b4=k.txt
            print(k.txt,k.min,k.max,rnd(value(k.y.has, len(best.rows), len(rest.rows),"best")),end=' ')
            for col in k.y.has:
                print(col,":",k.y.has[col],end=' ')
            print("\n")

    return True

def test_num() -> bool:
    num=Num()
    nums=[1,1,1,1,2,2,3]
    for i in nums:
        num.add(i)
    return 11/7 == num.mid() and 0.787 == rnd(num.div())

def test_sym() -> bool:
    sym=Sym()
    symbols=["a","a","a","a","b","b","c"]
    for s in symbols:
        sym.add(s)
    return ("a"==sym.mid() and 1.379 == rnd(sym.div()))

def test_read_from_csv():    
    rows = get_csv_rows(global_options[K_FILE])
    total_rows = len(rows)
    total_columns = len(rows[0])
    return total_columns*total_rows==8*399

def test_half():
    data = Data(global_options[K_FILE])
    left,right,A,B,mid,c = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells,c)
    print(mid)
    print(B.cells)
    return True



