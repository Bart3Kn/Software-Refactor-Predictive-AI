import os
import pandas as pd
import numpy as np
import helpers as helper

directory = os.fsencode('Systems\myOutput')

def bitmapIterator():
    for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".csv"):
                data = pd.read_csv(os.fsdecode(directory)+'\\'+filename, header=None)
                createBitmap(data,filename)

# Runs at 0(3n) could be improved but get the job done            
def createBitmap(data, filename):
    df = pd.DataFrame(data)
    dfClasses = pd.concat([data[0], data[1]]).unique()
    
    #S orts classes into alphabeitcal order
    # not sure if I want to actually implement this as it may skew the data.
    # dfClasses = sorted(dfClasses)
    zeroes = np.zeros((len(dfClasses),len(dfClasses)))

    class_dict ={}
    for x in range(len(dfClasses)):
        class_dict[dfClasses[x]] = x



    for x in range(len(data[0])):
        x_coord = class_dict.get(data[0][x])
        y_coord = class_dict.get(data[1][x])

        zeroes[x_coord][y_coord] = 1


    # Makes all diagonals become 1 to show self calls and creates a symmetrical view across the diagonal through optimisaiton
    np.fill_diagonal(zeroes,1)
    zeroes = np.maximum(zeroes, zeroes.transpose())

    # OUTPUTS DATA TO /MDGs/
    df = pd.DataFrame(zeroes,index=dfClasses, columns=dfClasses)
    df.to_csv('Systems\MDGs\\'+filename, index=True, header=True, sep=',')
    print("Done", filename)
    
if __name__ == "__main__":
    bitmapIterator()