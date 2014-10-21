#Brian Mitzel       893038547
#Sorasit Wanichpan  897260477
#Abeer Salam        899423594
#CPSC 335
#Project 2

import candidate
import sys
import time

def lcs(L, R):
    B = None

    #Convert L from a string to a list, and
    #generate all subsets (i.e.: subsequences) of the list
    factory = candidate.SubsetFactory(list(L))

    #Find the best candidate, if one exists
    while factory.has_next():
        subsequence = factory.next()
        if verify_subsequence(R, subsequence):
            if (B is None or
                    len(subsequence) > len(B)):
                B = subsequence

    #Convert B to a string and return it
    return "".join(B)
    
def verify_subsequence(string_to_match, candidate_subsequence):
    next = 0

    #Verify that each letter in the candidate subsequence appears in order in the string
    for letter in candidate_subsequence:
        r = next
        while (r < len(string_to_match) and
                letter != string_to_match[r]):
            r = r + 1

        if r < len(string_to_match):                    #Match found
            next = r + 1                                #Advance to the next letter
        else:                                           #Match not found
            return False                                #The candidate is not a subsequence of the string

    #All the letters in the candidate were matched in sequence with letters in the string successfully
    #Therefore, the candidate is a subsequence of the string
    return True

def main():
    #Verify the correct number of command line arguments were used
    if len(sys.argv) != 5:
        print('error: you must supply exactly four arguments\n\n' +
              'usage: python3 lcs.py <text file L> <text file R> <n(L)> <n(R)>')
        sys.exit(1)

    #Capture the command line arguments
    fileL = sys.argv[1]
    fileR = sys.argv[2]
    nL    = int(sys.argv[3])
    nR    = int(sys.argv[4])

    print('LCS:')
    string_a = open(fileL).read()[:nL]                  #First input
    string_b = open(fileR).read()[:nR]                  #Second input
    assert(len(string_a) == nL)
    assert(len(string_b) == nR)
    print('  a = ' + string_a + ', length', str(len(string_a)))
    print('  b = ' + string_b + ', length', str(len(string_b)))
    
    start    = time.perf_counter()                      #Get start time
    result   = lcs(string_a, string_b)                  #Find the LCS
    end      = time.perf_counter()                      #Get end time

    #Display the results
    print('  Elapsed time = ' + str(end - start))
    print('  Longest Common Subsequence = "' + result + '", length', len(result))

if __name__ == "__main__":
    main()