from problem import Problem

class BinaryProblem(Problem):
    
    def __init__(self, grid, rows, cols, vars_with_domain = None):
        self.grid = grid
        self.cols = cols
        self.rows = rows
        self.vars_with_domain = vars_with_domain

    def setGrid(self, grid):
        self.grid = grid

    def check_constraints(self, grid):
        return self.check_horizontal(grid) and self.check_vertical(grid) and self.check_uniqueness(grid)
    
    def check_uniqueness(self, grid):
        actual_grid = grid
        transposed = self.transpose(actual_grid)
        for x in range(len(actual_grid)):
            for y in range(len(actual_grid)):
                if x < y:
                    if actual_grid[x] == actual_grid[y]:
                        return False

        for x in range(len(transposed)):
            for y in range(len(transposed)):
                if x != y:
                    if actual_grid[x] == actual_grid[y]:
                        return False
        return True

    def check_horizontal(self, grid):
        actual_grid = grid
        for x in actual_grid:
            counter_in_row = 1
            counter_0_horizontal = 0
            counter_1_horizontal = 0
            previous_char = ' '
            for y in x:
                if y == '1':
                    counter_1_horizontal += 1
                    if previous_char == '1':
                        counter_in_row += 1
                        if counter_in_row == 2:
                            return False
                    else:
                        counter_in_row = 0
                if y == '0':
                    counter_0_horizontal += 1
                    if previous_char == '0':
                        counter_in_row += 1
                        if counter_in_row == 2:
                            return False
                    else:
                        counter_in_row = 0
                if counter_1_horizontal > len(actual_grid)/2 or counter_0_horizontal > len(actual_grid)/2:
                    return False
                previous_char = y
        return True

    def check_vertical(self, grid):
        actual_grid = grid
        transposed = self.transpose(actual_grid)
        for x in transposed:
            counter_in_row = 1
            counter_0_horizontal = 0
            counter_1_horizontal = 0
            previous_char = ' '
            for y in x:
                if y == '1':
                    counter_1_horizontal += 1
                    if previous_char == '1':
                        counter_in_row += 1
                        if counter_in_row == 2:
                            return False
                    else:
                        counter_in_row = 0
                if y == '0':
                    counter_0_horizontal += 1
                    if previous_char == '0':
                        counter_in_row += 1
                        if counter_in_row == 2:
                            return False
                    else:
                        counter_in_row = 0
                if counter_1_horizontal > len(actual_grid)/2 or counter_0_horizontal > len(actual_grid)/2:
                    return False
                previous_char = y
        return True

    def transpose(self, l):
        return [*zip(*l)]
            
    def insert(self, value, grid, domain, posX = -1, posY = -1):
        if posX == -1:
            x = 0
            for line in grid:
                y = 0
                for elem in line:
                    if elem == 'x':
                        grid[x][y] = value
                        return
                    y += 1
                x += 1
        else:
            grid[posX][posY] = value

    def insert_backwards(self, value, grid, domain, posX = -1, posY = -1):
        if posX == -1:
            x = 0
            for line in grid:
                y = 0
                for elem in line:
                    if elem == 'x':
                        grid[x][y] = value
                        return
                    y += 1
                x += 1
        else:
            grid[posX][posY] = value

    def end(self, grid) -> bool:
        for line in grid:
            for elem in line:
                if elem == 'x':
                    return False
        return True
        
    def choose_variable(self, grid):
        x = 0
        for line in grid:
            y = 0
            for elem in line:
                if elem == 'x':
                    return (x, y)
                y += 1
            x += 1
        return (-1, -1)

    def forward_check_domain(self, variable, value, domain, grid) -> bool:
        grid[variable[0]][variable[1]] = value
        check = self.check_constraints(grid)
        grid[variable[0]][variable[1]] = None
        return check
