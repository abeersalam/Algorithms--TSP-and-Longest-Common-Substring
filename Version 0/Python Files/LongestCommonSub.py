#Sorasit Wanichpan 897260477
#CPSC 335
#Project 2

#Please add your name and CWID
import candidate
import time

def longest_common_subseq(first_str,second_str):

    ###Variable Declarations
    ##For the final draft we can remove the redundant comments
    best = ""                                          #Best Candidate Solution
    second = list(second_str)                          #Convert the string into a list for sequential search for the common element


    ##Lazy Subset Generator.
    ##Instantiate the subset factory from the class provided for the project (candidate.py)
    factory = candidate.SubsetFactory(list(first_str)) #Convert the first string into a list, the SubsetFactory only accept lists (Check documentation included in candidate.py)
    while factory.has_next():                          #(Check documentation included in candidate.py)
        subseq_cand = ""                               #Empty string for each new subset generated, use to store common subsequence
        subseq_set = factory.next()                    #Gets the next subset generation

        ##Checking for common subsequences
        ##I want to make this into a separate function
        i = 0                                          #Index to traverse through the second string list, resets to zero with each new subset
        for x in subseq_set:                           #Loops through each element of the subset generated
            while i < len(second):                     #Loops through the length of the second string from i
               if x == second[i]:                      #Check if the element in the subset also exists in the string (or vice versa)
                    subseq_cand = subseq_cand + x      #If so, we concatenate it to the candidate string
                    i += 1                             #Increment the index
                    break                              #Break out of the inner loop, i holds our current position within the string
                                                       #This allows us to skip the characters we have already passed through
                                                       #This fixes the duplicate problem (the while loop)
               else:                                   #We still need to increment regardless
                i += 1

        ##Verifier, work in progress
        ##It works, but it's pretty bare bone
        ##I want to make this into a separate function
        if len(subseq_cand) > len(best):
            best = subseq_cand

        ##3 LOOPS!!!!
        ##AHHHHHHHHHHHHHHHHH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ##Refine this please!!!

    return best

def main():
    print('LCS:\n')

    #Take in input
    first_in = input('Enter X: ')                      #First input
    second_in = input('Enter Y: ')                     #Second input

    #Execute function and print out results
    print('a = "', first_in,'", length ',len(first_in))
    print('b = "',second_in,'", length ',len(second_in))
    start = time.perf_counter()                        #Get beginning time
    result = longest_common_subseq(first_in,second_in) #Find the LCS
    end = time.perf_counter()                          #Get end time
    print('Elapsed time: ' + str(end - start))
    print('Longest Common Subsequence = "',result,'" length ',len(result))

if __name__ == "__main__":
    main()








