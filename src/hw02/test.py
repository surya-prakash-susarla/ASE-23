from sym import Sym
from num import Num
from utils import rand ,rint, rnd
from data import Data
from csv import get_csv_rows
from globals import global_options, K_FILE

def test_global_options() -> bool:
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

    x_mid = data.stats(2, data.cols.x, True)
    x_div = data.stats(2, data.cols.x, False)
    y_mid = data.stats(2, data.cols.y, True)
    y_div = data.stats(2, data.cols.y, False)

    print("x")
    print(f"x \t mid \t {x_mid}")
    print(f"  \t div \t {x_div}")
    print("y")
    print(f"y \t mid \t {y_mid}")
    print(f"  \t div \t {y_div}")

    return True
'''
    for col in data.cols.x:
        col = [col]
        #x_mid.append(data.stats(2,col,True))
        mid_temp = data.stats(2, col, True)
        print(mid_temp)
        x_mid[mid_temp[0]] = mid_temp[1]
        #x_div.append(data.stats(2,col,False))
        div_temp = data.stats(2, col, False)
        x_div[div_temp[0]] = div_temp[1]
    
    for col in data.cols.y :
        col = [col]
        #y_mid.append(data.stats(2,col,True))
        #y_div.append(data.stats(2,col,False))
        mid_temp = data.stats(2, col, True)
        y_mid[mid_temp[0]] = mid_temp[1]
        div_temp = data.stats(2, col, False)
        y_div[div_temp[0]] = div_temp[1]
'''

def test_read_from_csv():    
    rows = get_csv_rows(global_options[K_FILE])
    total_rows = len(rows)
    total_columns = len(rows[0])
    return total_columns*total_rows==8*399

def test_read_data_csv():
    data = Data(global_options[K_FILE])
    return (len(data.rows)==398) and (data.cols.x[1].at==1) and (len(data.cols.x)==4)
    # TODO: ADD WEIGHT TEST
# and (data.cols.y[1].wt==-1) 

