'''

Kristel Tan (ktan@bu.edu), Joseph Cho (chojoe@bu.edu)
CAS CS330 Spring 2016 - Professor Byers
hw5 - numPart.py

'''

import heapq
import math
import random
import pandas #for use of DataFrame for visualization of the problem
import time

'''

Problem 4 (Part a)

'''
def knapsack(A):
    # Partition A in half 
    halfSum = math.floor(sum(A)/2) 
    n = len(A)
    
    # costTable = 2D array where: 
    # row represnts indices of A 
    # column represents 0 up to halfSum
    costTable = [[0 for x in range(halfSum+1)] for x in range(n+1)]

    #we know we can always reach a sum of 0 via the empty set
    for i in range(n):
        costTable[i][0] = 0
    
    #the only sum with a subset of 0 is 0
    for i in range(halfSum+1):
        costTable[0][i] = 0

    start = min(A)
    for item in range(1, n+1): #check all possible numbers up to halfSum 
        for max_val in range(start, halfSum+1):
            currentVal = A[item - 1]
            #check if we can use this current element
            if currentVal > max_val: 
                #set current slot to be the same value as the slot above it
                costTable[item][max_val] = costTable[item - 1][max_val]
            else:
                #find the correct entry for this slot of the 2D matrix
                costTable[item][max_val] = max(costTable[item - 1][max_val], costTable[item - 1][max_val - currentVal] + currentVal)

    
#    Uncomment to print out a visualization of the cost table as a 2D matrix
#    print("--------------------------")
#    print("       Cost Table         ")
#    print("--------------------------")
#    print(pandas.DataFrame(costTable))
    return costTable

def findSubset(A, ct):
    # columns
    j = len(ct[0])-1
    # rows
    i = len(ct)-1
    subset = [1 for i in range(len(A))]
        
    while (i >= 0 and j >=0):
        if (i==0 and ct[i][j]>0) or (ct[i][j] != ct[i-1][j]):
            subset[i-1] = -1
            j -= A[i-1]
        i -= 1
    return subset


'''

Problem 4 (Part b)

'''
def karmarkarKarp(A):
    heapq.heapify(A)
    # Sort the array of integers in descending order
    A.sort(reverse=True)
    
    while(len(A) > 1):
        A.sort(reverse=True)
        n1 = heapq.heappop(A)
        A.sort(reverse=True)
        n2 = heapq.heappop(A)
        heapq.heappush(A, abs(n1 - n2))
    
    return heapq.heappop(A)

for j in range(1, 12):
    
    startTime = time.time()
    
    print()
    print("Testing 10^", j, "...")
    A = []
    for i in range(100):
        A.append(random.randint(1, 10**j))
        
    ct = knapsack(A)
    signArray = findSubset(A, ct)
    print()
    print("NUMBER PARTITION ALGORTIHM")
    print()
    print("Sign array: ", signArray)
    print()
    newA = [a*b for a,b in zip(A,signArray)]
    print("Minimal residue: ", sum(newA))
    print("Duration: ", time.time() - startTime)
    
    print()
    print("KK ALGORITHM")
    print()
    startTime = time.time()
    print("Minimal residue: ", karmarkarKarp(A))
    print("Duration: ", time.time() - startTime)