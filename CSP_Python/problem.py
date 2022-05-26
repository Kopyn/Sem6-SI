from xmlrpc.client import Boolean


class Problem:
    def __init__(self, filename, domain, vars_with_domain = []):
        f1 = open(filename)
        self.grid = []
        lines = f1.readlines()
        for line in lines:
            self.grid.append(line.split())
        self.domain = domain
        self.vars_with_domain = vars_with_domain

    def check_constraints(self) -> bool:
        return True

    def forward_check(self, grid, variable, value) -> bool:
        grid[variable[0]][variable[1]] = value
        worth = self.check_constraints(grid)
        grid[variable[0]][variable[1]] = None
        return worth

    def forward_check_domain(self, variable, value, domain, grid) -> bool:
        return True