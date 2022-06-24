class Construction_link():
    def __init__(self) -> None:
        self.link = []

    def expansion(self):
        self.link.append([[{'in': None, 'out': None}],
                          [{'in': None, 'out': None}],
                          [{'in': None, 'out': None}],
                          [{'in': None, 'out': None}]]
                         )

    def contraction(self, index):
        self.link.pop(index)

    
    def add_link(self, indexindex_connector, line_bezier, direction)

        self.construction_link[index_connector][direction] = line_bezier
            def add_link(self, index_connector, line_bezier, direction):

        self.construction_link[index_connector][direction] = line_bezier