from sym import Sym
from num import Num
from utils import rand ,rint, rnd
from data import Data
from csv import get_csv_rows
from globals import global_options, K_FILE
from collections import OrderedDict

def test_global_options() -> bool:
    print(global_options)
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

def test_get_stats():
    data = Data(global_options[K_FILE])
    x_div={}
    x_mid={}
    y_div={}
    y_mid={}
    
    for col in data.cols.x:
        col = [col]
        mid_temp = data.stats(2, col, True)
        x_mid[mid_temp[0][0]] = mid_temp[0][1]
        div_temp = data.stats(2, col, False)
        x_div[div_temp[0][0]] = div_temp[0][1]

    for col in data.cols.y :
        col = [col]
        mid_temp = data.stats(2, col, True)
        y_mid[mid_temp[0][0]] = mid_temp[0][1]
        div_temp = data.stats(2, col, False)
        y_div[div_temp[0][0]] = div_temp[0][1]
    x_mid = OrderedDict(sorted(x_mid.items()))
    x_div = OrderedDict(sorted(x_div.items()))
    x_mid_p = {}
    x_div_p = {}
    for i in x_mid:
        x_mid_p[i] = x_mid[i]
        x_div_p[i] = x_div[i]
    y_mid = OrderedDict(sorted(y_mid.items()))
    y_div = OrderedDict(sorted(y_div.items()))
    y_mid_p = {}
    y_div_p = {}
    for i in y_mid:
        y_mid_p[i] = y_mid[i]
        y_div_p[i] = y_div[i]
    print("x")
    print(f"x \t mid \t {x_mid_p}")
    print(f"  \t div \t {x_div_p}")
    print("y")
    print(f"y \t mid \t {y_mid_p}")
    print(f"  \t div \t {y_div_p}")

    return True


def test_read_from_csv():    
    rows = get_csv_rows(global_options[K_FILE])
    total_rows = len(rows)
    total_columns = len(rows[0])
    return total_columns*total_rows==8*399

def test_read_data_csv():
    data = Data(global_options[K_FILE])
    return (len(data.rows)==398) and (data.cols.x[0].at==0) and (len(data.cols.x)==4) and (data.cols.y[0].wt==-1) 

