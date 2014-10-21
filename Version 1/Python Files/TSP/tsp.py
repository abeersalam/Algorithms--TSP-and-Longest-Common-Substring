#Brian Mitzel      893038547
#Sorasit Wanichpan 897260477
#Abeer Salam        899423594
#CPSC 335
#Project 2 v1
#python3 tsp.py <weighted_graph.xml.zip>

import sys
import time
import tsplib
import candidate

#TSP Algorithm from the lecture notes, modified to use lazy permutation over eager
def tsp_algo(weighted_graph):
    best = None

    #Generates all the permutations of the list
    factory = candidate.PermutationFactory(list(range(0,weighted_graph.vertex_count())))

    #Find the best candidate if one exists
    while factory.has_next():                    #Iterates through n! lazily, eager resulted in memory error
        perm = factory.next()                    #Next permutation
        cycle = perm + [perm[0]]                 #Path of distinct vertices/closed off by duplicating first vertex
        if verify_tsp(weighted_graph, cycle):    #Verifier
            if best is None or cycle_weight(weighted_graph, cycle) < cycle_weight(weighted_graph, best):
                best = cycle

    #return the best Hamiltonian cycle candidate
    return best

#From the lecture notes
def cycle_weight(graph, cycle):
    total = 0
    for i in range(len(cycle)-1):
        total += graph.distance(cycle[i], cycle[i+1])
    return total

#From the lecture notes
def verify_tsp(graph, cycle):
    for i in range(len(cycle)-1):
        if not graph.is_edge(cycle[i], cycle[i+1]):
            return False
    return True

def main():
    #Verify the correct number of command line arguments were used
    if len(sys.argv) != 2:
        print('error: you must supply exactly one arguments\n\n' +
              'usage: python3 tsp.py <weighted_graph.xml.zip file>')
        sys.exit(1)

    #Capture the command line arguments
    weighted_graph = sys.argv[1]

    print('TSP Instance:')                           #Get file input
    tspfile = tsplib.load(weighted_graph)            #Load the TSP file based upon user input
    print("n = ", tspfile.vertex_count())            #Print out the # of vertices
    start = time.perf_counter()                      #Get beginning time
    result = tsp_algo(tspfile)                       #Find the Hamiltonian cycle of minimum total weight
    end = time.perf_counter()                        #Get end time
    cost = cycle_weight(tspfile, result)             #Compute the cost

    #Prints out the result
    print('Elapsed time: ' + str(end - start))
    print('Optimal Cycle: ' + str(result))
    print('Optimal Cost: ' + str(cost))

if __name__ == "__main__":
    main()