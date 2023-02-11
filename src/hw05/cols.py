from utils import *
from num import Num
from sym import Sym

class Cols:
    def __init__(self, header_row):
        # Required during clone where original data is re-parsed.
        self.original = header_row

        self.all = []
        self.x = []
        self.y = []
        self.klass = []
        self.parse_header_row(header_row)

    def print_cols(self):
        for col in self.all:
            col.print()

    def parse_header_row(self, header_row):
        col_names= extract_entities_from_csv_row (header_row)
        # iterating over the column names
        for i in range(len(col_names)):
            if(is_name_numeric_header(col_names[i])):
                col = Num(i,col_names[i])
            else:
                col = Sym(i,col_names[i])
            #updating self.all
            self.all.append(col)

            #updating the columns that are not excluded 
            if(should_exclude_header(col_names[i])):
                continue
            else:
                if(col_names[i][-1]=='!'):
                    self.klass=col
                if(is_goal_header(col_names[i])):
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row):
        for col in self.y:
            col.add(row.cells[col.at])
        for col in self.x:
            col.add(row.cells[col.at])

    def get_y_value_statistics(self, is_mid):
        result =[]
        for col in self.y :
            result.append(self.get_statistic_for_column(col,is_mid))
        return result

    def get_statistic_for_column(self, col, is_mid):
        val = None
        if (is_mid):
            val = col.mid()
        else:
            val = col.div()
        return [col.txt, val]


