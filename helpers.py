import seaborn as sns
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt


# Used to display the different matrix so that it is easier to visualise the structure of the project
def bitmapViewer(location):
    matrix = np.genfromtxt(location, delimiter=',')
    plt.imshow(matrix)
    plt.show()

def matrixViewer(matrix, labels):
    plt.imshow(matrix)
    plt.show()

# Used to fetch the class names based on the matrix
# TO BE USED ON THE BITMAP OUTPUTS
def classNames(location):
    header = pd.read_csv(location, nrows=1).columns.tolist()
    return header

# Removes all headers from the matrix so that we only have the actualy matrix itself
# Removes top and first row
def bitmapStripper(bitmapLocation):
    data = np.genfromtxt(bitmapLocation, delimiter = ',', encoding="utf-8")
    matrix = np.array(data[1:,1:])
    return matrix

# Editing out comments and text from java file source code
def deleteComments(contents):
    
    partialOutput = re.sub(re.compile(r"/\*.*?\*/",re.DOTALL ) ,"" ,contents) # Single-line comments
    partialOutput = re.sub(re.compile(r"\".*?\"",re.DOTALL), "",partialOutput) # Multi-line comments
    output = re.sub(re.compile(r"//.*?\n" )," \n" ,partialOutput) # Text within log files

    return output