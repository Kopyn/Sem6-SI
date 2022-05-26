class DataPackage():
    def __init__(self, rows, cols, data = []):
        self.data = data
        self.constraints = {}
        self.graph = {}
        self.vars_with_domain = {}
        self.vars_constraint_count = {}
        self.rows = rows
        self.cols = cols
    
    def get_data_package(self):
        return self.data

    def get_constraints(self):
        return self.constraints

    def get_graph(self):
        return {}
    
    def get_variables_with_domain(self):
        return self.vars_with_domain
