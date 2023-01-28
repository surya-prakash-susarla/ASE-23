import math

from globals import *
from csv import get_csv_rows
from cols import Cols
from Row import row

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

    def dist(self, row_1, row_2, cols = self.cols.x):
        n = 0
        d = 0
        for col in cols:
            n = n + 1
            d = d + (col.dist(row_1.cells[col.at], row_2.cells[col.at])**global_options[K_DISTANCE_COEF])
        return (d/n)**(1/global_options[K_DISTANCE_COEF])

    def around(self, row):
        print("TODO - IMPLEMENT DATA.AROUND")

    def half(self, row):
        print("TODO - IMPLEMENT DATA.HALF")

    def cluster(self):
        print("TODO - IMPLEMENT DATA.CLUSTER")

    def sway(self):
        print("TODO - IMPLEMENT DATA.SWAY")

