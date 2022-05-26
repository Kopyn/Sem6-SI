import copy
from matplotlib.pyplot import xlim
from futoshiki_data_package import FutoshikiDataPackage
from problem import Problem

class FutoshikiProblem(Problem):
    
    def __init__(self, grid, constraints, vars_with_domain, vars_constraint_count, rows, cols):
        self.grid = grid
        self.constraints = constraints
        self.rows = rows
        self.cols = cols
        self.vars_with_domain = vars_with_domain
        self.vars_constraint_count = vars_constraint_count
        self.adapt_values()

    def setGrid(self, grid):
        self.grid = grid

    def check_constraints(self, grid):
        constraints_map_check = self.check_constraints_map(grid)
        if not constraints_map_check:
            return False

        horizontal_check = self.check_horizontal(grid)
        if not horizontal_check :
            return False
        
        vertival_check = self.check_vertical(grid)
        if not vertival_check: 
            return False
        
        return True
    
    def check_constraints_map(self, grid) -> bool:
        for pair in self.constraints:
            if self.constraints[pair] == '>':
                if grid[pair[0][0]][pair[0][1]] != None and grid[pair[1][0]][pair[1][1]] != None:
                    if grid[pair[0][0]][pair[0][1]] <= grid[pair[1][0]][pair[1][1]]:
                        return False
            else:
                if grid[pair[0][0]][pair[0][1]] != None and grid[pair[1][0]][pair[1][1]] != None:
                    if grid[pair[0][0]][pair[0][1]] >= grid[pair[1][0]][pair[1][1]]:
                        return False   
        return True

    def check_horizontal(self, grid) -> bool:
        for line in grid:
            for x in range(self.cols):
                if line.count(x+1) > 1:
                    return False
        return True

    def check_vertical(self, grid) -> bool:
        transposed = self.transpose(grid)
        for line in transposed:
            for x in range(self.cols):
                if line.count(x+1) > 1:
                    return False
        return True

    def transpose(self, l):
        return [*zip(*l)]
    
    def insert(self, value, grid, domain, posX = -1, posY = -1):
        if posX == -1:
            x = 0
            for line in grid:
                y = 0
                for elem in line:
                    if elem == None:
                        grid[x][y] = value
                        domain[(posX, posY)] = [value]
                        self.remove_from_domain(value, grid, (x, y), domain)
                        return
                    y += 1
                x += 1
        else:
            grid[posX][posY] = value
            domain[(posX, posY)] = [value]
            self.remove_from_domain(value, (posX, posY), domain)

    def insert_backwards(self, value, grid, domain, posX = -1, posY = -1):
        if posX == -1:
            x = 0
            for line in grid:
                y = 0
                for elem in line:
                    if elem == None:
                        grid[x][y] = value
                        return
                    y += 1
                x += 1
        else:
            grid[posX][posY] = value
                
    def remove_from_domain(self, value, variable, domain):
        for x in range(self.rows):
            if(variable[0] != x and variable[1] != x):
                if value in domain[(variable[0], x)]:
                    domain[(variable[0], x)].remove(value)
                if value in domain[(x, variable[1])]:
                    domain[(x, variable[1])].remove(value)

    def forward_check_domain(self, variable, value, domain, grid) -> bool:
        for x in domain:
            if len(x) == 0:
                return False
        return self.check_constraints(grid)
    
    def end(self, grid) -> bool:
        for line in grid:
            if None in line:
                return False
        return True

        
    def choose_variable(self, grid):
        for key in self.vars_constraint_count:
            if grid[key[0]][key[1]] == None:
                return (key[0], key[1])
        # x = 0
        # for line in grid:
        #     y = 0
        #     for elem in line:
        #         if elem == None:
        #             return (x, y)
        #         y += 1
        #     x += 1
        # return (-1, -1)

    def choose_value_order(self, variable):
        for pair in self.constraints:
            if pair[0] == (variable[0], variable[1]):
                if self.constraints[pair] == '>':
                    return self.vars_with_domain[variable][::-1]
                else:
                    return self.vars_with_domain[variable]
            if pair[1] == (variable[0], variable[1]):
                if self.constraints[pair] == '<':
                    return self.vars_with_domain[variable]
                else:
                    return self.vars_with_domain[variable][::-1]
        return self.vars_with_domain[variable]

    def adapt_values(self):
        for variable in self.vars_with_domain:
            for pair in self.constraints:
                if pair[0] == (variable[0], variable[1]):
                    if self.constraints[pair] == '>':
                        self.vars_with_domain[variable] = self.vars_with_domain[variable][::-1]
                    else:
                        self.vars_with_domain[pair[1]] = self.vars_with_domain[pair[1]][::-1]
