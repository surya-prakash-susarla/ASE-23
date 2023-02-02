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
                for row in source_rows:
                    self.add_row(row)
            except:
                print("Error - Could not parse non-source file data for addition to data")
        

    def add_row(self, row):
        if self.cols != None:
            new_row = row
            self.rows.append(new_row)
            self.cols.add(row)
        else:
            self.cols = Cols(row)

    def clone(self, new_rows):
        new_data = Data(source_file=None, source_rows=[self.cols.original])
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
            x = col.norm(row_1[col.at])
            y = col.norm(row_2[col.at])
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
            d = d + (col.dist(row_1[col.at], row_2[col.at])**global_options[K_DISTANCE_COEF])
        return (d/n)**(1/global_options[K_DISTANCE_COEF])

    def around(self, row_1,rows = None ):
        if rows==None:
            rows = copy.deepcopy(self.rows)
        return sorted(rows, key=lambda row: self.dist(row_1, row))

    def half(self,  rows=None, cols=None, above=None):
        if rows == None:
            rows = copy.deepcopy(self.rows)
        some = self.many(rows)
        total_length = len(rows)
        A = above if above != None else some[rint(0,len(some))]
        far_point = math.floor(total_length*K_DEFAULT_FARAWAY_VALUE)
        B = self.around(A,some)[far_point]
        c = self.dist(A,B,cols)
        rows = sorted(rows ,key = lambda row: cosine(self.dist(row,A,cols), self.dist(row,B,cols), c))
        left=[]
        right=[]
        for i in range (len(rows)):
            if i < len(rows)//2:
                left.append(rows[i])
            else:
                right.append(rows[i])
        mid = right[0]
        return left, right, A,B, mid,c

    def many(self, row):
        row_len= len(row)
        temp=[]
        
        for i in range(K_DEFAULT_SAMPLE_VALUE):
            j = rint(0,row_len-1)
            if(j>=row_len):
                print("j val out of range:", j,i,row_len)
            temp.append(row[j])
        return temp

    def cluster(self, rows = None, min = None, cols = None, above = None):
        if rows == None:
            rows = self.rows
        if min == None:
            min = len(rows)**K_DEFAULT_MIN_VALUE
        if cols == None:
            cols = self.cols.x
        node = Node()
        node.data = self.clone(rows)
        if len(rows) > 2*min:
            left, right, node.A, node.B, node.mid,c = self.half(rows, cols, above)
            node.left  = self.cluster(left,  min, cols, node.A)
            node.right = self.cluster(right, min, cols, node.B)
        return node

    def sway(self, rows=None,min=None,cols=None,above=None):
        if rows == None :
            rows = copy.deepcopy(self.rows)
        if min == None:
            min = len(rows)**K_DEFAULT_MIN_VALUE
        if cols == None:
            cols = self.cols.x
        node = Node()
        node.data =  self.clone(rows)
        if len(rows)> 2*min:
            left,right,node.A,node.B,node.mid,c = self.half(rows,cols,above)
            if (self.better(node.B,node.A)):
                left,right,node.A,node.B = right,left,node.B,node.A 
            node.left = self.sway(left,min,cols,node.A)
        return node

