import copy
import math
from globals import *
from csv import get_csv_rows
from cols import Cols
from row import Row
from utils import rint, cosine, show, get_repgrid_file_contents, many , rand
from node import Node
from range import Range

import collections
class Data:
    def __init__(self, source_file = K_DEFAULT_DATA_FILE, source_rows = None):
        self.rows = []
        self.cols = None

        if source_file != None:
            for row in get_csv_rows(source_file):
                self.add_row(row)

        if source_rows != None:
            for row in source_rows:
                self.add_row(row)

    def add_row(self, row):
        if self.cols != None:
            if type(row) is list:
                row = Row(row)
            elif not isinstance(row, Row):
                raise Exception("row being added is not of type list or row, contents: ", row)
            self.rows.append(row)
            self.cols.add(row)
        else:
            self.cols = Cols(row)

    def clone(self, new_rows):
        new_data = Data(source_file=None, source_rows=[self.cols.original])
        for row in new_rows:
            new_data.add_row(row)
        return new_data

    def stats(self, nPlaces: int = 2, cols: [] = None, is_mid = True): 
        results = []
        if cols != None:
            for col in cols:
                result = self.cols.get_statistic_for_column(col, is_mid)
                result[1] = col.rnd(result[1], nPlaces)
                results.append(result)
        else:
            results = self.cols.get_y_value_statistics(is_mid, nPlaces)
        return results

    def better(self, row_1: Row, row_2: Row):
        s1 = 0
        s2 = 0
        ys = self.cols.y
        x = None
        y = None
        l = len(ys)
        for col in ys:
            x = col.norm(row_1.cells[col.at])
            y = col.norm(row_2.cells[col.at])
            s1 = s1 - (math.exp(col.wt*((x-y)/l)))
            s2 = s2 - (math.exp(col.wt*((y-x)/l)))
        return (s1/l) < (s2/l)

    def dist(self, row_1, row_2, cols = None):
        if cols == None:
            cols = self.cols.x
        n = 0
        d = 0
        for col in cols:
            n = n + 1
            d = d + (col.dist(row_1.cells[col.at], row_2.cells[col.at])**global_options[K_DISTANCE_COEF])
        return (d/n)**(1/global_options[K_DISTANCE_COEF])

    def around(self, row_1,rows = None ):
        if rows==None:
            rows = copy.deepcopy(self.rows)
        return sorted(rows, key=lambda row: self.dist(row_1, row))

    def half(self,  rows=None, cols=None, above=None):
        if rows == None:
            rows = copy.deepcopy(self.rows)
        A = above if above != None else rows[rint(0,len(rows))]
        B = self.furthest(A, rows)
        c = self.dist(A,B,cols)

        # project lambda
        def project(row):
            x, y = cosine(self.dist(row, A, cols), self.dist(row, B, cols), c)
            row.x = x if row.x == None else row.x
            row.y = y if row.y == None else row.y
            return x

        rows = sorted(rows, key = lambda row: project(row))

        left=[]
        right=[]
        for i in range (len(rows)):
            if i < len(rows)//2:
                left.append(rows[i])
            else:
                right.append(rows[i])
        mid = right[0]
        return left, right, A, B, mid, c

    

    def cluster(self, rows = None, min = None, cols = None, above = None):
        if rows == None:
            rows = self.rows
        if min == None:
            min = len(rows)**K_MIN_DEFAULT_VALUE
        if cols == None:
            cols = self.cols.x
        node = Node()
        node.data = self.clone(rows)
        if len(rows) >= 2:
            left, right, node.A, node.B, node.mid, node.c = self.half(rows, cols, above)
            node.left  = self.cluster(left,  min, cols, node.A)
            node.right = self.cluster(right, min, cols, node.B)
        return node

    def worker(self, rows, worse=[],above=None):
        if(len(rows)<=(len(self.rows)**K_MIN_DEFAULT_VALUE)):
             return rows, many(worse, K_REST_DEFAULT_VALUE*len(rows)) 
        l,r,A,B,_,__ =self.half(rows=rows,above=above)
        if self.better(B,A):
            l,r,A,B = r,l,B,A 
        for row in r :
            worse.append(row)
        return self.worker(l,worse,A)

    def sway(self, rows=None,min=None,cols=None,above=None):
        if rows == None :
            rows = copy.deepcopy(self.rows)
        best, rest = self.worker(rows,[])
        return self.clone(best),self.clone(rest)
    
    def furthest(self, row_1, rows=None):
        if rows == None:
            rows = copy.deepcopy(self.rows)
        return self.around(row_1, rows=rows)[-1]

    def bins(self, cols , rowss):
        out =[]
        for col in cols :
            ranges={}
            count=0
            for y in rowss:
                rows = rowss[y]
                for row in rows:
                    x = row.cells[col.at]
                    if x != '?':
                        k = self.bin(col,x)
                        if((k in ranges)==False):
                            ranges[k]=Range(col.at,col.txt,x)
                        count+=1
                        self.extend(ranges[k],x,y)
            ranges = list(ranges.values())
            ranges = sorted(ranges , key = lambda range : range.lo)
            if col.isSym :
                out.append(ranges)
            else:
                out.append(self.mergeAny(ranges))
        
        return out 


    def noGaps(self, t):

        if t == []:
            return
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo = -10000000000
        t[-1].hi = 10000000000
        return t

    def mergeAny(self, ranges0):
        ranges1 = []
        
        j = 0
        while j < len(ranges0)-1:
            left, right = ranges0[j], ranges0[j+1]
            if right:
                y = self.merge2(left.y, right.y)
                
                if y:
                    j+=1
                    left.hi, left.y = right.hi, y
            ranges1.append(left)
            j+=1
        if(j<len(ranges0)):
            ranges1.append(ranges0[-1])
        if len(ranges0) == len(ranges1):
            return self.noGaps(ranges0)
        else:
            return self.mergeAny(ranges1)
        
    def merge2(self, col1, col2):
        new = self.merge(col1, col2)
        if new.div() <= (col1.div()*col1.n + col2.div()*col2.n)/new.n:
            return new
        return []

    def merge(self, col1, col2):
        new = copy.deepcopy(col1)
        if col1.isSym:
            for x in col2.has:
                self.add(new, x,col2.has[x])
        else:
            for x in col2.has:
                self.add(new, n=col2.has[x])
            new.lo = min(col1.lo, col2.lo)
            new.hi = max(col1.hi, col2.hi)
        return new

    def bin(self, col , x):
        if x=='?' or col.isSym :
            return x
        if col.max == col.min:
            return 1
        temp = (col.max - col.min)/(K_BINS_DEFAULT_VALUE-1)
        return math.floor(x/temp +0.5)*temp
    
    def extend(self,range , n,s):
        range.lo = min(n, range.lo)
        range.hi = max(n, range.hi)
        self.add(range.y,s)
        
    def add(self, col, x, n = 1):
        if x != '?':
            col.n += n
            if col.isSym:
                
                col.has[x] = n + col.has[x]
                if col.has[x] > col.most:
                    col.most, col.mode = col.has[x], x
            else:
                col.min, col.max = min(x, col.min), max(x, col.max)
        
                all = len(col.has)
                pos = 0
                if all < K_MAX_DEFAULT_VALUE:
                    pos = all+1
                elif rand() < K_MAX_DEFAULT_VALUE/col.n:
                    pos = rint(1, all)
                if pos:
                    col.has[pos] = x
                    col.ok = False

def cliffsDelta(ns1, ns2):
        if(len(ns1)>256):
            ns1=many(ns1,256)
        if(len(ns2)>256):
            ns2=many(ns2,256)
        if(len(ns1)> 10*len(ns2)):
            ns1=many(ns1,10*ns1)
        if(len(ns2)>10*len(ns1)):
            ns2=many(ns2,10*len(ns1))
        n=0
        gt=0
        lt=0
        for x in ns1:
            for y in ns2:
                n=n+1
                if x>y:
                    gt = gt+1
                elif  y>x:
                    lt = lt+1
        return  ((abs(lt-gt))/n) > K_CLIFFS_DEFAULT_VALUE


def diffs(nums1, nums2):
    out = []
    for k1, k2 in zip(nums1, nums2):
        out.append(cliffsDelta(k1.has,k2.has))
    return out

def rep_cols(orig_cols):
    cols = copy.deepcopy(orig_cols)
    for col in cols:
        col[-1] = col[0] + ":" + col[-1]
        del col[0]
    col_names = []
    for i in range(1, 11):
        col_names.append('Num'+str(i))
    col_names.append('thingX')
    cols.insert(0, col_names)
    return Data(source_file=None, source_rows=cols)

def rep_rows(orig_data, orig_rows):
    rows = copy.deepcopy(orig_rows)
    for i in range(len(rows[-1])):
        rows[0][i] = rows[0][i]+":"+rows[-1][i]
    del rows[-1]
    for i in range(len(rows)):
        if(i==0):
            rows[i].append('thingX')
        else:
            u = orig_data['rows'][(len(orig_data['rows'])-i)]
            rows[i].append(u[-1])
    for row in rows:
        print(row)
    return Data(source_file=None, source_rows=rows)
    
def transpose(original):
    rows =[]
    for i in range (len(original[0])):
        current_row=[]
        for j in range (len(original)):
            current_row.append(original[j][i])
        rows.append(current_row)
    return rows

def rep_place(data):
    n, g = 20, collections.defaultdict(list)
    for i in range(1, n+1):
        for _ in range(1, n+1):
            g[i].append(" ")
    maxy = 0
    print("")
    for r, row in enumerate(data.rows):
        c = chr(64 + r)
        print(c, row.cells[-1])
        x, y = math.floor(row.x*n), math.floor(row.y*n)
        maxy = max(maxy, y+1)
        g[y+1][x+1] = c
    print("")
    for y in range(1, maxy):
        print(g[y])

def rep_grid(s_file):
    t = get_repgrid_file_contents(s_file)
    rows = rep_rows(t, transpose(t['cols']))
    cols = rep_cols(t['cols'])
    show(rows.cluster(), cols.cluster(), nPlaces=2)
    rep_place(rows)

def person_1():

    person_1=[['Violence', 'Cringe', 'Romance', 'Fantasy', 'Thriller', 'Gore', 'Strong-Language', 'Comedy', 'thingX'],
       [5,1,2,1,4,3,4,2,'Fightclub'],
       [5,1,2,3,5,2,3,2, 'Top Gun'],
       [3,1,2,5,4,1,2,5, 'Spiderman'],
       [5,5,1,1,5,5,3,3, 'The Menu'],
       [2,3,4,3,2,1,5,5, 'Ted'],
       [3,2,3,1,3,1,5,5, 'Jumpstreet'],
       [3,5,5,1,1,1,3,5, 'Titanic'],
       [1,3,1,5,5,2,1,3, 'Martian'],
       [5,4,5,5,2,3,2,3, 'Twilight'],
       [4,1,2,1,4,1,5,5,'Bad boys']]
    
    return Data(source_file=None, source_rows=person_1)

def person_2():

    person_2=[['Action', 'Drama', 'Family Friendly', 'Comedy', 'Psychotic', 'Budget', 'Romance', 'thingX'],
       [5,3,2,3,2,3,3,'Fightclub'],
       [4,4,3,2,1,5,4, 'Top Gun'],
       [5,2,5,4,1,5,3, 'Spiderman'],
       [2,5,1,2,5,2,1, 'The Menu'],
       [1,2,1,5,2,2,4, 'Ted'],
       [2,2,1,5,1,1,4, 'Jumpstreet'],
       [2,4,2,3,1,4,5, 'Titanic'],
       [2,2,4,3,1,5,2, 'Martian'],
       [5,4,2,4,3,5,5, 'Twilight'],
       [4,4,2,5,1,3,3, 'Bad boys']]
    return Data(source_file=None, source_rows=person_2)

def person_3():
    person_3=[['Close to reality', 'cast diversity', 'director-popularity', 'Comedy', 'Action', 'Vfx', 'Romance', 'thingX'],
       [2,3,3,4,5,2,3,'Fightclub'],
       [3,4,3,2,5,4,2, 'Top Gun'],
       [1,4,2,5,5,5,3, 'Spiderman'],
       [1,3,1,2,4,1,1, 'The Menu'],
       [3,2,3,5,2,2,4, 'Ted'],
       [5,1,1,5,2,1,4, 'Jumpstreet'],
       [4,1,5,4,2,5,5, 'Titanic'],
       [1,2,4,2,2,5,2, 'Martian'],
       [1,4,3,2,5,4,4, 'Twilight'],
       [4,5,2,5,5,1,4,'Bad boys']]
    return Data(source_file=None, source_rows=person_3)
    
