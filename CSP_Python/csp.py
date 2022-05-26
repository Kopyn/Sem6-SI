from data_package import DataPackage
from problem import Problem
import copy

class CSP:

    def __init__(self, problem : Problem, domain, data_package : DataPackage):
        self.results = []
        self.problem = problem
        self.grid = data_package.get_data_package()
        self.data_package = data_package
        self.domain = domain
        self.visited_nodes = 0
    
    def search(self, new_grid, domain):
        self.visited_nodes += 1
        chosen_variable = self.choose_variable(new_grid)
        for val in domain[chosen_variable]:
            worth = self.problem.forward_check_domain(chosen_variable, val, domain, new_grid)
            if worth: 
                copied = []
                for line in new_grid:
                    arr = []
                    for elem in line:
                        arr.append(elem)
                    copied.append(arr)
                domain_copy = domain
                self.problem.insert(val, copied, domain_copy, chosen_variable[0], chosen_variable[1])
                if self.end_recurency(copied):
                    self.results.append(copied)                        
                    # if self.check_constraints(copied):
                    #     self.results.append(copied)
                else:
                    self.search(copied, domain_copy)

    def backwards_search(self, new_grid, domain):
        self.visited_nodes += 1
        chosen_variable = self.choose_variable(new_grid)
        for val in domain[chosen_variable]:
            copied = []
            for line in new_grid:
                arr = []
                for elem in line:
                    arr.append(elem)
                copied.append(arr)
            self.problem.insert_backwards(val, copied, domain, chosen_variable[0], chosen_variable[1])
            if self.check_constraints(copied):
                if self.end_recurency(copied):
                    self.results.append(copied)
                else:
                    self.backwards_search(copied, domain)

    def check_constraints(self, new_grid):
        return self.problem.check_constraints(new_grid)

    def end_recurency(self, new_grid) -> bool:
        return self.problem.end(new_grid)


    def get_results(self):
        return self.results

    def start(self):
        # self.search(self.grid, self.problem.vars_with_domain)
        self.backwards_search(self.grid, self.problem.vars_with_domain)

    def choose_variable(self, grid):
        return self.problem.choose_variable(grid)

    def forward_check(self, grid, variable, value) -> bool:
        return self.problem.forward_check(grid, variable, value)

