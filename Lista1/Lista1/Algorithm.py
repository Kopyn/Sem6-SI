from Subject import Subject
import random
from Machine import Machine
import matplotlib.pyplot as plt
import numpy as np

class Algorithm:

    popNum = 200
    genNum = 100
    numOfRows = 5
    numOfCols = 6
    numOfMachines = 24
    tournamentN = 20
    modifyChance = 0.3
    mergeChance = 0.3

    def __init__(self):
        print("algorithm started")


    def genPopulation(self):
        returnedPopulation = []
        for x in range(Algorithm.popNum):
            s = Subject(self.mapToMachines(self.genArray()), Algorithm.numOfRows, Algorithm.numOfCols)
            returnedPopulation.append(s)
        return returnedPopulation

    def genSubjectFromArray(self, array):
        return Subject(self.mapToMachines(array), Algorithm.numOfRows, Algorithm.numOfCols)

    def genArray(self):
        a = []
        for x in range(Algorithm.numOfCols*Algorithm.numOfRows):
            if x >= Algorithm.numOfMachines:
                a.append(-1)
            else:
                a.append(x)
        random.shuffle(a)
        return a


    def mapToMachines(self, array):
        returnedMachines = []
        for x in range(len(array)):
            coordinates = self.mapIndexToCoordiates(x)
            m = Machine(array[x], coordinates[1], coordinates[0])
            returnedMachines.append(m)
        return returnedMachines

    def mapIndexToCoordiates(self, i):
        row = i%Algorithm.numOfRows
        if Algorithm.numOfRows == 1:
            col = i
        else:
            col = int(i/Algorithm.numOfCols)
        return (row, col)

    def selectTournament(self, subjects):
        a = random.sample(subjects, Algorithm.tournamentN)
        selected = a[0]
        for x in a:
            if x.getFitnessValue() < selected.getFitnessValue():
                selected = x
        return selected

    def selectRoulette(self, subjects):
        weightsArray = []
        worstVal = subjects[0].getFitnessValue()
        value = 0
        for x in subjects:
            v = x.getFitnessValue()
            if v > worstVal:
                worstVal = v
        for x in subjects:
            weightsArray.append(1 + worstVal - x.getFitnessValue())
            
        return random.choices(subjects, weights = weightsArray, k = 1)[0]

    def merge(self, p1, p2):
        if random.random() < Algorithm.mergeChance:
            mergePoint = random.randint(0, len(p1.returnGrid()) - 1)
            childArray1 = []
            childArray2 = []
            p1Grid = p1.returnGrid()
            p2Grid = p2.returnGrid()
            for x in range(len(p1Grid)):
                if x < mergePoint:
                    childArray1.append(p1Grid[x].number)
                    childArray2.append(p2Grid[x].number)
                else:
                    childArray2.append(p1Grid[x].number)
                    childArray1.append(p2Grid[x].number)

            return [self.fixChild(childArray1), self.fixChild(childArray2)]
        else:
            return [p1, p2]
        

    
    def fixChild(self, child):
        lackingNumbers = []
        childArray = child
        for x in range(Algorithm.numOfMachines):
            lackingNumbers.append(x)
        for x in range((Algorithm.numOfCols*Algorithm.numOfRows)-Algorithm.numOfMachines):
            lackingNumbers.append(-1)

        length = len(lackingNumbers)

        for x in range(length):
            if childArray[x] in lackingNumbers:
                lackingNumbers.remove(childArray[x])
            else:
                a = lackingNumbers[0]
                lackingNumbers.remove(a)
                childArray[x] = a
        return Subject(self.mapToMachines(self.modifyChild(childArray)), Algorithm.numOfRows, Algorithm.numOfCols)

    def modifyChild(self, childArray):
        if random.random() <= Algorithm.modifyChance:
            i = random.randint(0, len(childArray)-1)
            j = random.randint(0, len(childArray)-1)
            childArray[i], childArray[j] = childArray[j], childArray[i]
        return childArray


    def findBest(self, population):
        bestVal = population[0]
        for x in population:
            val = x.getFitnessValue()
            if val < bestVal.getFitnessValue():
                bestVal = x
        return bestVal
    
    def findWorst(self, population):
        worstVal = population[0]
        for x in population:
            val = x.getFitnessValue()
            if val > worstVal.getFitnessValue():
                worstVal = x
        return worstVal

    def init(self):

        pop = self.genPopulation()
        
        best = self.findBest(pop).getFitnessValue()
        worst = self.findWorst(pop).getFitnessValue()
        avg = 0
        bestSubject = self.findBest(pop)
        bestValue = best
        avgAvg = 0
        bestAvg = 0
        worstAvg = 0

        # a = self.genSubjectFromArray([10,18,4,-1,-1,1,12,0,21,3,7,20,19,23,15,17,11,2,22,-1,5,14,13,6,-1,9,16,8,-1,-1])
        # print(a.getFitnessValue())

        worstValues = []
        averageValues = []
        bestValues = []
        index = 0
        index += 1
        a=0
        while index < 10:
            index += 1
            while a < Algorithm.genNum:
                a = a + 1
                newPop = []
                avg = 0.0
                for x in range(int(Algorithm.popNum/2)):
                    children = self.merge(self.selectTournament(pop), self.selectTournament(pop))
                    newPop.append(children[0])
                    newPop.append(children[1])
                    avg += children[0].getFitnessValue()
                    avg += children[1].getFitnessValue()
                pop = newPop
                # pop = self.genPopulation()
                best = self.findBest(pop).getFitnessValue()
                worst = self.findWorst(pop).getFitnessValue()
                # for x in range(Algorithm.popNum):
                #     avg += pop[x].getFitnessValue()
                avg /= Algorithm.popNum
                worstValues.append(worst)
                averageValues.append(avg)
                bestValues.append(best)
                if best < bestValue:
                    bestValue = best
                    bestSubject = self.findBest(pop)
            
            print("------------")
            print("best:")
            print(best)
            bestAvg += best
            print("------------")
            print("avg:")
            print(avg)
            avgAvg += avg
            print("------------")
            print("worst:")
            print(worst)
            worstAvg += worst
            print(self.genSubjectFromArray(bestSubject.returnMachineNumbersInGrid()))
            print("------------")

            print("bestValue:")
            print(bestValue)

        print("------------")
        print("best:")
        print(bestAvg/9)
        print("------------")
        print("avg:")
        print(avgAvg/9)
        print("------------")
        print("worst:")
        print(worstAvg/9)
        print(self.genSubjectFromArray(bestSubject.returnMachineNumbersInGrid()))
        print("------------")
        print("bestValue:")
        print(bestValue)
        title = "Population - {pop}, Generations - {gen}, Crossover chance - {cros}, Mutation chance - {mut}"
        title = title.format(pop = Algorithm.popNum, gen = Algorithm.genNum, cros = Algorithm.mergeChance, mut = Algorithm.modifyChance)
        plt.title(title)
        plt.plot(worstValues, label = 'worst')
        plt.plot(averageValues, label = 'average')
        plt.plot(bestValues, label = 'best')
        plt.legend()
        plt.show()

        
