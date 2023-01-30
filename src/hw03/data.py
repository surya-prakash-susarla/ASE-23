import copy
import math

from globals import *
from csv import get_csv_rows
from cols import Cols
from row import Row
from utils import rint, cosine 
from node import Node 
class Data:
    def __init__(self, source_file = K_DEFAULT_DATA_FILE, source_rows = None):
        self.rows = []
        self.cols = None

        if source_file != None:
            for row in get_csv_rows(source_file):
                self.add_row(row)

        if source_rows != None:
            try:
                for row in rows:
                    self.add_row(row)
            except:
                print("Error - Could not parse non-source file data for addition to data")

    def add_row(self, row):
        if self.cols != None:
            self.rows.append(row)
            self.cols.add(row)
        else:
            self.cols = Cols(row)

    def clone(self, new_rows):
        new_data = Data(source_rows=self.cols.original)
        for row in new_rows:
            new_data.add_row(row)
        return new_data

    def stats(self, nPlaces: int, cols: [] = None, is_mid = True): 
        results = []
        if cols != None:
            for col in cols:
                result = self.cols.get_statistic_for_column(col, is_mid)
                result[1]= col.rnd(result[1],nPlaces)
                results.append(result)
                #results.append(col.rnd(self.cols.get_statistic_for_column(col, is_mid)[1], nPlaces))
        else:
            results = self.cols.get_y_value_statistics(is_mid)
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
            s1 = s1 - (math.e**(math.log(col.wt*((x-y)/l), 10)))
            s2 = s2 - (math.e**(math.log(col.wt*((y-x)/l), 10)))
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

    def half(self,  cols, above,rows=None):
        if rows == None:
            rows = copy.deepcopy(self.rows)
        some = self.many(rows)
        A = above if above != None else some[rint(len(some))]
        B = self.around(A,some)[(global_options[K_DEFAULT_FARAWAY_VALUE]*len(rows))//1]
        c = self.dist(A,B,cols)
        sorted(rows ,key = lambda row: cosine(self.dist(row,A,cols), self.dist(row,B,cols),c))
        left=[]
        right=[]
        for i in range (len(rows)):
            if i < len(rows)//2:
                left.append(rows[i])
                mid = rows[i]
            else:
                right.append(rows[i])
        return left, right, A,B, mid,c

    def many(self, row):
        row_len= len(row)
        rows=[]
        for i in range(global_options[K_DEFAULT_SAMPLE_VALUE]):
            j = rint(0,row_len)
            rows.append(row[i])
        return rows

    def cluster(self):
        print("TODO - IMPLEMENT DATA.CLUSTER")

    def sway(self, rows,min,cols,above):
        if rows == None :
            rows = self.rows
        if min == None:
            min = len(rows)* global_options[K_DEFAULT_MIN_VALUE]
        if cols == None:
            cols = self.cols.x
        node = Node()
        node.data =  self.clone(rows)
        if len(rows)> 2*min:
            left,right,node.A,node.B,node.mid = self.half(rows,cols,above)
            if (self.better(node.A,node.B)):
                left,right,node.A,node.B = right,left,node.B,node.A 
            node.left = self.sway(left,min,cols,node.A)
        return node
        print("TODO - IMPLEMENT DATA.SWAY")

