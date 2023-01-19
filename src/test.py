from sym import Sym
from num import Num
from utils import rand ,rint, rnd
def test_global_options() -> bool:
    return True

def test_rand() -> bool:
    num1 = Num()
    num2 = Num()
    for i in range(1, 1001):
        num1.add(rand(937162211,0,1))
    for i in range(1, 1001):
        num2.add(rand(937162211,0,1))
    m1= rnd(num1.mid(),10)
    m2= rnd(num2.mid(),10)
    print(rnd(m1, 1))
    print(m1)
    print(m2)
    return m1==m2 and .5 == rnd(m1,1)

def test_num() -> bool:
    num=Num()
    nums=[1,1,1,1,2,2,3]
    for i in nums:
        num.add(i)
    a = 11/7 == num.mid() 
    b = .787 == rnd(num.div())
    print ( "a : ", a)
    print ( "b : ", b)
    print ( num.mid() )
    print ( rnd(num.div()) )
    result = a and b
    print("result : ", result)
    return result
    

def test_sym() -> bool:
    sym=Sym()
    symbols=["a","a","a","a","b","b","c"]
    for s in symbols:
        sym.add(s)
    return ("a"==sym.mid() and 1.379 == rnd(sym.div()))
