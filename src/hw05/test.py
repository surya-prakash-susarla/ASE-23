from sym import Sym
from num import Num
from utils import rand ,rint, rnd, show, show_tree, tree
from data import Data, rep_cols , rep_rows, rep_grid, rep_place, transpose
from csv import get_csv_rows
from collections import OrderedDict
from globals import *

import copy

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
    data = Data()
    data2 = data.clone(data.rows)
    print("TODO - CHECK VALUES IN STATS NOT MATCHING WITH OUTPUT")
    print(data.stats())
    print(data2.stats())
    return True

def test_dist() -> bool:
    data = Data()
    num = Num()
    for row in data.rows:
        num.add(data.dist(row, data.rows[0]))
    num.print()
    return True

def test_cliffs() -> bool:
    print("TODO - implement test for cliffs")
    return True

def test_tree() -> bool:
    show_tree(tree(Data()))
    return True

def test_sway() -> bool:
    print("TODO - implement test for sway")
    return True

def test_bins() -> bool:
    print("TODO - implement test for bins")
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
    print(A,c)
    print(mid)
    print(B)
    return True

