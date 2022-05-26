from data_package import DataPackage

class BinaryDataPackage(DataPackage):
    def __init__(self, rows, cols, data = [], domain = []):
        super().__init__(data, rows, cols)
        self.domain = domain

    def read_data_from_file(self, filename):
        self.data = []
        f1 = open(filename)
        lines = f1.readlines()
        row = 0
        for line in lines:
            col = 0
            arr = []
            for x in line:
                if x != '\n':
                    arr.append(x)
                    self.vars_with_domain[(row, col)] = self.domain
                col += 1
            row += 1
            self.data.append(arr)

    