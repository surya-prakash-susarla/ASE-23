# TODO: data class goes here.

from csv import CSV_Reader

class Data:
    def __init__(self, source_file = None, _source_rows = None):
        self.rows = []
        self.cols = None

        if source_file != None:
            print("TODO: PASS FILENAME TO CSV AND GET STUFF INSERTED")
        else:
            print("TODO: ADD ROWS TO THE CURRENT OBJECT HERE")

    def add_row(self, row):
        print("Adding contents to the data object")
        if self.cols != None:
            print("TODO: ADD INCOMING ROW TO ROWS OBJECT")
            print("TODO: UPDATE COLS WITH STATS OF INCOMING DATA")
        else:
            print("TODO: INITIALIZE COLS OF CURRENT OBJECT")

    def clone(self):
        print("TODO: IMPLEMENT CLONE")

    def stats(self):
        print("TODO: IMPLEMENT STATS")
            

