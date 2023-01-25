from sym import Sym
from num import Num
from utils import rand ,rint, rnd
from data import Data
from csv import get_csv_rows
from globals import global_options, K_FILE

def test_global_options() -> bool:
    return True

def test_rand() -> bool:
    num1 = Num()
    num2 = Num()
    num1.add(rand(0,1,937162211))
    for i in range(1000):
        num1.add(rand(0,1))
    num2.add(rand(0,1,937162211))
    for i in range(1000):
        num2.add(rand(0,1))
    m1= rnd(num1.mid(),10)
    m2= rnd(num2.mid(),10)
    return m1==m2 and .5 == rnd(m1,1)

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
    total_rows = 1+ len(rows) # header contributes a row
    total_columns = len(rows[0])

    return total_columns*total_rows==8*399


def test_read_data_csv():
    data = Data(global_options[K_FILE])
    return (len(data.rows)==398) and (data.cols.y[1].wt==-1) and (data.cols.x[1].at==1) and (len(data.cols.x)==4)



