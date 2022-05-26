from binary_data_package import BinaryDataPackage
from csp import CSP
from binary_problem import BinaryProblem
from futoshiki_data_package import FutoshikiDataPackage
from futoshiki_problem import FutoshikiProblem
from data_package import DataPackage
from datetime import datetime

FUTOSHIKI = 6
BINARY = 6

if __name__ == "__main__":
    #initializing binary data array
    dp = BinaryDataPackage(BINARY, BINARY, domain = ('0', '1'))
    b = "binary_%ix%i" % (BINARY, BINARY)
    dp.read_data_from_file(b)

    #initializing constraints object
    b = BinaryProblem(dp.get_data_package(), BINARY, BINARY, vars_with_domain=dp.get_variables_with_domain())
    first = datetime.now()
    #initializing csp object
    csp = CSP(b, ('0', '1'), dp)
    
    csp.start()
    print("results")
    res = csp.get_results()
    for x in res:
        for y in x:
            print(y)
        print()
    print("finished")
    now = datetime.now()
    print("Time: ", now-first)
    print("Visited nodes: ", csp.visited_nodes)

    #FUTOSHIKI
    print("-----------------------")
    dp = FutoshikiDataPackage(FUTOSHIKI, FUTOSHIKI, domain = [*range(1, FUTOSHIKI+1, 1)])
    f = "futoshiki_%ix%i" % (FUTOSHIKI, FUTOSHIKI)
    dp.read_data_from_file(f)
    f = FutoshikiProblem(dp.get_data_package(), dp.get_constraints(), dp.get_variables_with_domain(), dp.vars_constraint_count, FUTOSHIKI, FUTOSHIKI)
    csp = CSP(f, [*range(1, FUTOSHIKI+1, 1)], dp)

    first = datetime.now()

    print(f.constraints)
    print(dp.vars_constraint_count)
    print(f.vars_with_domain)

    csp.start()

    now = datetime.now()
    print("Time: ", now-first)
    print("Visited nodes: ", csp.visited_nodes)

    res = csp.get_results()
    print(len(res))
    # for x in res:
    #     for y in x:
    #         print(y)
    #     print()
    # print("finished")
