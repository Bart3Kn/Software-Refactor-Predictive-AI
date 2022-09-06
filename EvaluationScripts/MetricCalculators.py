from collections import Counter
import sys
sys.path.append('C:/Users/barte/Desktop/Project')
import pathlib
import pandas as pd
from statistics import median, mode
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import helpers as he


def projectClassStatistics():
    location = pathlib.Path('Systems\Bitmaps')
    classCountArray = []
    for bitmap in location.iterdir():
            classCountArray.append(len(he.classNames(bitmap))-1)
    
    print("Min: \t", np.min(classCountArray))
    print("Max: \t", np.max(classCountArray))
    print("Mean: \t", np.mean(classCountArray))
    print("Median:\t", median(classCountArray))
    print("Mode: \t", mode(classCountArray))
    print("Count: \t", len(classCountArray))

    sns.set_theme(style="ticks")

    box = sns.boxplot(data = classCountArray, orient="h")
    box.set(xlabel = "Number of Classes", ylabel = "Count")
    plt.show()


def EVMFitnessStatistics():
    location = pathlib.Path('Systems\EVMFitness')
    EVMCountArray = []
    for evmValue in location.iterdir():
            EVMCountArray.append(int(np.genfromtxt(evmValue, encoding = 'utf-8')))
    

    print("Min: \t", np.min(EVMCountArray))
    print("Max: \t", np.max(EVMCountArray))
    print("Mean: \t", np.mean(EVMCountArray))
    print("Median:\t", median(EVMCountArray))
    print("Count: \t", len(EVMCountArray))
    print(EVMCountArray)

if __name__ == "__main__":
    EVMFitnessStatistics()