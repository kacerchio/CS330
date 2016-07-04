'''

Kristel Tan (ktan@bu.edu), Joseph Cho (chojoe@bu.edu)
CAS CS330 Spring 2016 - Professor Byers
hw7 - hw7-question4.py

'''

import heapq
import math
import random
import pandas
import matplotlib.pyplot as plt

arrays = [] # Holds all the arrays
array = []  # Array that we're currently inserting

# Generate 50 random instances
for i in range(50):
    array = []                 # Reinitialize to empty
    for j in range(100):       # Add sets of 100 integers chosen uniformly from [1, 10^12]
        array.append(random.randint(1, 10**12))
    arrays.append(array)
    
'''

Karmarkar-Karp Implementation

'''
def karmarkarKarp(A):
    a = A[:]
    heapq.heapify(a)
    # Sort the array of integers in descending order
    a.sort(reverse=True)
    
    while(len(a) > 1):
        a.sort(reverse=True)
        n1 = heapq.heappop(a)
        a.sort(reverse=True)
        n2 = heapq.heappop(a)
        heapq.heappush(a, abs(n1 - n2))
    
    return heapq.heappop(a)

kkArray = []

# Perform Karmarkar-Karp for each array in arrays
for a in arrays:
    kkArray.append(karmarkarKarp(a))

print('Karmarkar-Karp Solutions:', kkArray)


'''

Repeated Random Implementation

'''
def repeatedRandom(A, K):
    solutions = []
    current = []

    for k in range(K):
        s = []
        for i in range(len(A)):
            # Flip a coin to generate a sign
            coin = random.randint(1,10)
            if coin <= 5:
                s.append(1)
            elif coin > 5:
                s.append(-1)

        for j in range(len(s)):
            # Multiply the randomly generated sign array with the current array being looked at
            current.append((A[j] * s[j]))       
            # Append the current array to the solutions array
            solutions.append(abs(sum(current)))

    # Return the solution with the minimal residue 
    return min(solutions)

rrArray = []

# Perform Repeated Random for each array in arrays
for a in arrays:
    rrArray.append(repeatedRandom(a, 250))

print()
print('Repeated Random Solutions: ', rrArray)


'''

Gradient Descent Implementation

'''
def gradientDescent(A, K):
    s = []
    sPrime = []
    
    # Generate an initial random solution S
    for i in range(len(A)):
        coin = random.randint(1,10)
        if coin <= 5:
            s.append(1)
        elif coin > 5:
            s.append(-1)
          
    for k in range(K):
        sPrime = s[:]  
        # Choose two random indices to define the swap 
        i, j = random.sample(range(1, 100), 2)
        
        sPrime[i] *= -1            # Set s[i] to its negation with probability of 1
        coin = random.random()    
        if coin < 0.5:
            sPrime[j] *= -1        # Set s[j] to its negation with probability of 0.5
        
        newS = [a*b for a,b in zip(A,s)]
        newSPrime = [a*b for a,b in zip(A,sPrime)]
        
        sRes = abs(sum(newS))
        sPrimeRes = abs(sum(newSPrime))
        if sPrimeRes < sRes: 
            s = sPrime

    solution = [a*b for a,b in zip(A,s)]
    return abs(sum(solution))
            
gdArray = []

# Perform Gradient Descent for each array in arrays
for a in arrays:
    gdArray.append(gradientDescent(a, 250))

print()
print('Gradient Descent Solutions: ', gdArray)


'''

Simulated Annealing Implementation

''' 
def simulatedAnnealing(A, K):
    s = []
    sPrime = []
    
    # Generate an initial random solution S
    for i in range(len(A)):
        coin = random.randint(1,10)
        if coin <= 5:
            s.append(1)
        elif coin > 5:
            s.append(-1)
          
    for k in range(K):
        sPrime = s[:]  
        # Choose two random indices to define the swap 
        i, j = random.sample(range(1, 100), 2)
        
        sPrime[i] *= -1            # Set s[i] to its negation with probability of 1
        coin = random.random()     # Set s[j] to its negation with probability of 0.5
        if coin < 0.5:
            sPrime[j] *= -1
        
        newS = [a*b for a,b in zip(A,s)]
        newSPrime = [a*b for a,b in zip(A,sPrime)]
        
        sRes = abs(sum(newS))
        sPrimeRes = abs(sum(newSPrime))
        if sPrimeRes < sRes: 
            s = sPrime
        else:
            temp = (10**10)*(0.8**(k/300))
            prob = math.exp(sPrime - sRes) / temp
            coin = random.random()
            if coin < prob:
                s = sPrime

    solution = [a*b for a,b in zip(A,s)]
    return abs(sum(solution))

saArray = []

# Perform Gradient Descent for each array in arrays
for a in arrays:
    saArray.append(gradientDescent(a, 250))

print()
print('Simulated Annealing Solutions: ', saArray)

kkAvg = [sum(list(kkArray)[:x])/x for x in range(1, 51)]
rrAvg = [sum(list(rrArray)[:x])/x for x in range(1, 51)]
gdAvg = [sum(list(gdArray)[:x])/x for x in range(1, 51)]
saAvg = [sum(list(saArray)[:x])/x for x in range(1, 51)]

residues = {'Karmarkar-Karp': kkAvg, 'Repeated Random': rrAvg, 
            'Gradient Descent': gdAvg, 'Simulated Annealing': saAvg}
            
pandas.DataFrame(residues).plot()
plt.show()
pandas.DataFrame(residues).plot(figsize=(12,10))
plt.savefig('hw7-question4-plot')
