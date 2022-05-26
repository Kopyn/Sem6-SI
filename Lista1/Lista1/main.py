from Algorithm import Algorithm

# popNum = 10
# genNum = 10
# numOfRows = 5
# numOfCols = 6
# numOfMachines = 24
# tournamentN = 30

# def genPopulation():
#     returnedPopulation = []
#     for x in range(popNum):
#         s = Subject(mapToMachines(genArray()), numOfRows, numOfCols)
#         returnedPopulation.append(s)
#     return returnedPopulation

# def genSubjectFromArray(array):
#     return Subject(mapToMachines(array), numOfRows, numOfCols)

# def genArray():
#     a = []
#     for x in range(numOfCols*numOfRows):
#         if x >= numOfMachines:
#             a.append(-1)
#         else:
#             a.append(x)
#     random.shuffle(a)
#     return a


# def mapToMachines(array):
#     returnedMachines = []
#     for x in range(len(array)):
#         coordinates = mapIndexToCoordiates(x)
#         m = Machine(array[x], coordinates[0], coordinates[1])
#         returnedMachines.append(m)
#     return returnedMachines

# def mapIndexToCoordiates(i):
#     row = i%numOfRows
#     if numOfRows == 1:
#         col = i
#     else:
#         col = int(i/numOfCols)
#     return (row, col)

# def selectTournament(subjects):
#     a = random.sample(subjects, tournamentN)
#     selected = a[0]
#     for x in a:
#         if x.getFitnessValue() < selected.getFitnessValue():
#             selected = x
#     return selected

# def selectRoulette(subjects):
#     weightArray = []
#     valuesArray = []
#     value = 0
#     for x in subjects:
#         v = x.getFitnessValue()
#         value += v
#         valuesArray.append(v)
#     for x in valuesArray:
#         weightArray.append(x/value)
#     roulette = random.random()
#     weightsSummary = 0.0
#     for x in range(len(weightArray)):
#         if roulette <= weightsSummary:
#             return subjects[x]
#         weightsSummary += weightArray[x]
#     return subjects[len(subjects)-1]

# def merge(p1, p2):
#     mergePoint = random.randint(0, len(p1.returnGrid()) - 1)
#     childArray = []
#     for x in range(len(p1.returnGrid())):
#         if x < mergePoint:
#             if p1.returnGrid()[x].number == -1:
#                 childArray.append(p1.returnGrid()[x].number)
#             elif (p1.returnGrid()[x].number in childArray):
#                 childArray.append(p2.returnGrid()[x].number)
#             else:
#                 childArray.append(p1.returnGrid()[x].number)
#         else:
#             if p2.returnGrid()[x].number == -1:
#                 childArray.append(p2.returnGrid()[x].number)
#             elif (p2.returnGrid()[x].number in childArray):
#                 childArray.append(p1.returnGrid()[x].number)
#             else:
#                 childArray.append(p2.returnGrid()[x].number)
#     return fixChild(Subject(mapToMachines(childArray), numOfRows, numOfCols))
    
 
# def fixChild(child):
#     newArray = []
#     machineCounts = []
#     print(child)
#     oldArray = child.returnMachineNumbersInGrid()

#     for x in range(len(oldArray)):
#         if oldArray.count(oldArray[x]) > 1 and oldArray[x] != -1:
#             c = 0
#             while oldArray.count(c) < 1:
#                 c += 1
#             if c == numOfMachines:
#                 oldArray[x] = -1
#             else:
#                 oldArray[x] = c
#     return Subject(mapToMachines(oldArray), numOfRows, numOfCols)

# def findBest(population):
#     bestVal = population[0]
#     for x in population:
#         val = x.getFitnessValue()
#         if val > bestVal.getFitnessValue():
#             bestVal = x
#     return bestVal

if __name__ == "__main__":
    
    a = Algorithm()
    a.init()

    #easy
    # array = [6, 1, 0, 7, 8, 4, 3, 2, 5]
    # test = genSubjectFromArray(array)

    # print("test array")
    # print(str(test))
    # print("expected value 7078")
    # print("---------------------")

    #flat
    # array = [6, 2, 5, 9, 1, 3, 7, 0, 8, 10, 11, 4]
    # test = genSubjectFromArray(array)

    # print("test array")
    # print(str(test))
    # print("expected value 16990")
    # print("---------------------")
    
    #hard
    # array = [-1, 14, 0, 7, 16, 22, 1, 23, -1, 11, 3, 19, 21, 12, 13, 10, 5, 9, -1, -1, 17, 20, 4, 18, 8, 15, 2, 6, -1]
    # test = genSubjectFromArray(array)

    # print("test array")
    # print(str(test))
    # print("expected value 30922")
    # print("---------------------")


    # pop = genPopulation()

    # for x in pop:
    #     print(str(x))

    # best = findBest(pop)
    # while best.getFitnessValue() > 4900:
    #     print(best.getFitnessValue())
    #     newPop = []
    #     for x in range(popNum):
    #         newPop.append(merge(selectTournament(pop), selectTournament(pop)))
    #     pop = newPop
    #     best = findBest(pop)
    #     print(best)
    #     print(best.getFitnessValue())