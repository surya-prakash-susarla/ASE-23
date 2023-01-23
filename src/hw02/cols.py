class Cols:
    def __init__(self, header_row):
        # Required during clone where original data is re-parsed.
        self.original = header_row

        self.all = []
        self.x = []
        self.y = []
        self.klass = []
        self._parse_header_row(header_row)

    def _parse_header_row(self, header_row):
        print("TODO: CREATE META STRUCTURE USING HEADER ROW")
        print("REFER TO UTILS IN UTILS.PY FOR HEADER REGEX TYPE OF UTILS")
        print("UTILS ALSO HAS , DELIMITER SPLITTER FOR RE-USE")

    def add(self, row):
        print("TODO: ADD ROW TO COL STRUCTURES")

    def get_y_value_statistics(self, is_mid):
        print("TODO: FILTER Y VALUE COLUMNS AND CALL FUNCTION BELOW")

    def get_statistic_for_column(self, col, is_mid):
        print("TODO - RETURN ASKED STAT FROM MEMBER COLS")

    def rnd(self, value):
        print("TODO - IMPLEMENT RND FUNCTION")

