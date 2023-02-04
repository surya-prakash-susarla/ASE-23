class Row:
    def __init__(self, contents):
        if type(contents) is not list:
            raise Exception("Row being initialized without list, contents : ", contents)
        self.cells = contents
