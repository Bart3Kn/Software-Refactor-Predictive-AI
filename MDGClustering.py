import pathlib
import random
import numpy as np
import pandas as pd
import helpers as he
from tqdm import tqdm

# Iterate through all the files in the folder
# Main used to execture all files in the system
def directoryNavigation():
    location = pathlib.Path('Systems\MDGs')
    for mdg in tqdm(location.iterdir()):
        numberOfClasses = len(he.classNames(mdg))-1
        matrix = he.bitmapStripper(mdg)
        clusterOutput, bestEVM = munchClustering(1000,matrix, numberOfClasses)
        saveCluster2CSV(clusterOutput, mdg.name)
        print(bestEVM)
        saveEVM2CSV(bestEVM, mdg.name)

def saveCluster2CSV(clusters,mdgName):
    df = pd.DataFrame(clusters)
    df.to_csv(str('Systems\munchClusters\\'+mdgName), index=False, header=False)
    print("Clusters Saved!")

def saveEVM2CSV(bestEVM,mdgName):
    df = pd.DataFrame([bestEVM])
    df.to_csv(str('Systems\EVMFitness\\'+mdgName), index=False, header=False)
    print("EVM Fitness Saved!")

# MUNCH hierarchical clustering
def munchClustering(iter, matrix, numberOfClasses):
    
    cycles = 50
    startingSolution = generateSolution(matrix, numberOfClasses)

    bestSolution = startingSolution
    bestEVM = EVMFitness(startingSolution, matrix)

    
    for cycle in range(1,cycles+1):

        # Generates new Solution for each cycle
        startingSolution = generateSolution(matrix, numberOfClasses)
        
        for i in range(iter//cycles):
            
            newSolution = smallChange(startingSolution, numberOfClasses)
            newFitness = EVMFitness(newSolution, matrix)


            # Treat Zero as the optimal solution
            if newFitness > bestEVM:
                bestEVM = newFitness
                bestSolution = newSolution

            print("Cycle:", cycle, "Iteration:",i, "CurrentFitness:", newFitness, "BestFitness", bestEVM)
    return bestSolution, bestEVM

# Calculation of Fitness
def EVMFitness(currentSolution,mdg):
    
    EVM = 0

    for j in range(0,len(mdg[0])-1):
        for k in range(1,len(mdg[0])):
            C1 = currentSolution[j]
            C2 = currentSolution[k]

            # COMPARES NEARBY OBJECTS IN SOLUTION IF THEY ARE THE SAME GROUP THEN
            if C1 == C2:

                # CHANGES EVM VALUE
                # IF THE MATRIX VALUES ARE THE SAME WE GET A VALUE OF 1
                EVM = EVM + (2*mdg[j][k])-1
    return EVM

    
#Returns random number between two values, inclusive
def randomNumberGen(first,last):
    return random.randint(first,last)

def generateSolution(matrix, numberOfClasses):
    length = matrix.size
    solution = []
    for x in range(length):
        solution.append(randomNumberGen(1,numberOfClasses))
    return solution

def smallChange(solution, numberOfClasses):
    value2Change = randomNumberGen(1, (len(solution)-1))
    randomValue = randomNumberGen(1,numberOfClasses)
    while randomValue == solution[value2Change]:
        randomValue = randomNumberGen(1,numberOfClasses)
    solution[value2Change] = randomValue

    return solution

if __name__ == "__main__":
    directoryNavigation()