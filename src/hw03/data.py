from csv import get_csv_rows
from cols import Cols
from globals import global_options, K_FILE, K_DEFAULT_DATA_FILE

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

    def better(self, row_1, row_2):
        print("TODO - IMPLEMENT DATA.BETTER")

    def dist(self, row_1, row_2):
        print("TODO - IMPLEMENT DATA.DIST")

    def around(self, row):
        print("TODO - IMPLEMENT DATA.AROUND")

    def half(self, row):
        print("TODO - IMPLEMENT DATA.HALF")

    def cluster(self):
        print("TODO - IMPLEMENT DATA.CLUSTER")

    def sway(self):
        print("TODO - IMPLEMENT DATA.SWAY")

