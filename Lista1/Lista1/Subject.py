import json
import Machine

class Subject:

    f1 = open('hard_flow.json')
    f2 = open('hard_cost.json')
    flows = json.load(f1)
    costs = json.load(f2)

    def __init__(self, machines, rows, cols):
        self.machines = machines
        self.rows = rows
        self.cols = cols
        self.fitnessValue = self.getFitness()

    def returnGrid(self):
        return self.machines
    
    def returnMachineNumbersInGrid(self):
        machines = []
        for x in self.machines:
            machines.append(x.number)
        return machines

    def returnFlowBetweenTwoMachines(self, m1, m2):
        if m1.number == -1 or m2.number == -1:
            return 0
        for x in Subject.flows:
            if x.get("source") == m1.number and x.get("dest") == m2.number:
                return x.get("amount")
        return 0

    def returnCostBetweenTwoMachines(self, m1, m2):
        if m1.number == -1 or m2.number == -1:
            return 0
        for x in Subject.costs:
            if x.get("source") == m1.number and x.get("dest") == m2.number:
                return x.get("cost")
        return 0

    def returnDistanceBetweenTwoMachines(self, m1, m2):
            return abs(m1.x - m2.x) + abs(m1.y - m2.y)

    def getFitnessValue(self):
        return self.fitnessValue

    def getFitness(self):
        value = 0
        for m1 in range(len(self.machines)):
            for m2 in range(len(self.machines)):
                if m1 != m2:
                    value += self.returnFlowBetweenTwoMachines(self.machines[m1], self.machines[m2]) * self.returnCostBetweenTwoMachines(self.machines[m1], self.machines[m2]) * self.returnDistanceBetweenTwoMachines(self.machines[m1], self.machines[m2])
        return value

    def __str__(self):
        s = ""
        for x in range(self.rows):
            for y in range(self.cols):
                s += str(self.machines[x*self.cols + y])
                s += " "
            s += "\n"
        s += "\n"
        s += str(self.getFitnessValue())
        return s
    