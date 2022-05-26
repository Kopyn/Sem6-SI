import copy
from data_package import DataPackage

class FutoshikiDataPackage(DataPackage):
    def __init__(self, rows, cols, data = [], domain = []):
        super().__init__(rows, cols, data)
        self.constraints = {}
        self.domain = domain
        self.vars_constraint_count = {}
        for i in range(rows):
            for j in range(cols):
                self.vars_constraint_count[(i, j)] = 0
        

    def read_data_from_file(self, filename):
        f1 = open(filename)
        lines = f1.readlines()
        row = 0

        for line in range(len(lines)):
            col = 0
            if line % 2 == 0:
                arr = []
                for x in range(len(lines[line])):
                    if lines[line][x] != '\n':
                        if x % 2 == 0:
                            ch = lines[line][x]
                            if ch == 'x':
                                arr.append(None)
                                self.vars_with_domain[(row, col)] = copy.deepcopy(self.domain)
                            else:
                                self.vars_with_domain[(row, col)] = [int(ch)]
                                arr.append(int(ch))
                            col += 1
                        else:
                            if lines[line][x] != '-':
                                if (row, col - 1) not in self.vars_constraint_count:
                                    self.vars_constraint_count[(row, col - 1)] = 1
                                else:
                                    self.vars_constraint_count[(row, col - 1)] += 1
                                if (row, col) not in self.vars_constraint_count:
                                    self.vars_constraint_count[(row, col)] = 1
                                else:
                                    self.vars_constraint_count[(row, col)] += 1
                                self.constraints[((row, col - 1), (row, col))] = lines[line][x]
                self.data.append(arr)
                row += 1
            else:
                for x in range(len(lines[line])):
                    if lines[line][x] != '\n' and lines[line][x] != '-':
                        if (row - 1, col) not in self.vars_constraint_count:
                            self.vars_constraint_count[(row - 1, col)] = 1
                        else:
                            self.vars_constraint_count[(row - 1, col)] += 1
                        if (row, col) not in self.vars_constraint_count:
                            self.vars_constraint_count[(row, col)] = 1
                        else:
                            self.vars_constraint_count[(row, col)] += 1
                        self.constraints[((row - 1, col), (row, col))] = lines[line][x]
                    col += 1
        self.vars_constraint_count = dict(sorted(self.vars_constraint_count.items(), key = lambda item: item[1], reverse=True))
        
    
    def get_variables_with_domain(self):
        return self.vars_with_domain

    def modify_variables_with_domain_dict(self, key, domain):
        print()