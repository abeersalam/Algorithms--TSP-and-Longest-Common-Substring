#Sorasit Wanichpan 897260477
#CPSC 335
#Project 2

#Please add your name and CWID
import sys
import time
import tsplib
import candidate

#TSP Algorithm from the lecture notes, modified to use lazy permutation over eager
#Run time is limited by memory size if use eager permutation

def tsp_algo(g):
    best = None                                 #Best
    list = []                                   #Empty list

    list.extend(range(0,g.vertex_count()))      #Fills the list from 0 to n

    factory = candidate.PermutationFactory(list) #Generates permutations lazily, uses the factory class
    while factory.has_next():                    #Iterates through n! lazily, eager resulted in memory error
        perm = factory.next()                    #Next permutation
        cycle = perm + [perm[0]]                 #Path of distinct vertices/closed off by duplicating first vertex
        if verify_tsp(g, cycle):                 #Verifier
            if best is None or cycle_weight(g, cycle) < cycle_weight(g, best):  #Check for the best
                best = cycle
    return best

#From the lecture notes
def cycle_weight(g, cycle):
    total = 0
    for i in range(len(cycle)-1):
        total += g.distance(cycle[i], cycle[i+1])
    return total

#From the lecture notes
def verify_tsp(g, cycle):
    for i in range(len(cycle)-1):
        if not g.is_edge(cycle[i], cycle[i+1]):
            return False
    return True

def main():
    filename = input('TSP Instance: ')               #Get file input
    tspfile = tsplib.load(filename)                  #Load the TSP file based upon user input
    print("n = ", tspfile.vertex_count())            #Print out the # of vertices
    start = time.perf_counter()                      #Get beginning time
    result = tsp_algo(tspfile)                       #Find the optimal path
    end = time.perf_counter()                        #Get end time
    cost = cycle_weight(tspfile, result)             #Compute the cost

    #Prints out the result
    print('Elapsed time: ' + str(end - start))
    print('Optimal Cycle: ' + str(result))
    print('Optimal Cost: ' + str(cost))

if __name__ == "__main__":
    main()

