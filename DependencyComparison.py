import os
import pandas as pd
import numpy as np


# TESTING FOR MDG FILES, USED DURING DEVELOPMENT, NO NEED FOR ACTUAL USAGE
# UNLESS LOOKING FOR DEBUGGING

def comparison(file1, file2):
    mdg1 = pd.read_csv(file1, delimiter=',', header=None)
    mdg1 = columnCombiner(mdg1)

    mdg2 = pd.read_csv(file2, delimiter=',', header=None)
    mdg2 = columnCombiner(mdg2)

    # USAGE OF XOR TO FIND TEH DIFFERENCES BETWEEN THE TWO MDGS    
    allDiff = set(mdg1) ^ set(mdg2)
    allSame = set(mdg1) and set(mdg2)
    
    Accuraccy = len(allSame)/(len(allSame)+len(allDiff))

    understandDiff = set(mdg1) - set(mdg2)
    myOutputDiff = set(mdg2) - set(mdg1)

    # BASIC DEBUGGING PRINTS
    print("Accuracy:", Accuraccy*100)
    # print("Number of similar entries: ",len(allSame))
    # print("Number of differences between two sets: ", len(allDiff))
    #p rint("Difference between two sets are: \n", allDiff)

    #More detailed prints with actual differences:
    print("What appears in Understand  but not mine: ", len(understandDiff), "\n", understandDiff)
    print("What appears in mine but not Understand:", len(myOutputDiff), "\n", myOutputDiff)


def columnCombiner(mdg):
    list = []
    for x in range(len(mdg)):
        list.append(str(mdg[0][x]+","+mdg[1][x]))
    return list
