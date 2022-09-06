from multiprocessing import reduction
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow as tf
import pathlib
import helpers as he
import numpy as np
from matplotlib import pyplot as plt
from tensorflow import keras
from keras import layers, datasets, models
from keras.metrics import Precision, Recall, BinaryAccuracy
from keras.models import load_model
from sklearn.metrics import r2_score






def processData():
    data = tf.keras.utils.image_dataset_from_directory('Systems\ResizedBitmaps', image_size = (400,400))
    data_iterator = data.as_numpy_iterator()
    batch = data_iterator.next()

    #print(len(data))
    trainSize = int(len(data)*.7)
    validationSize = int(len(data)*.2)+1
    testSize = int(len(data)*.1)+1
    
    train = data.take(trainSize)
    validate = data.skip(trainSize).take(validationSize)
    test = data.skip(trainSize+validationSize).take(testSize)

    #CREATING AND TRAINING MODEL
    cnn = createModel()
    cnnEpochLogs = cnn.fit(train, epochs=35, validation_data=validate)

    #PRINTING RESULTS FROM EPOCHS
    #Mean Squared Error over Epochs
    fig = plt.figure()
    plt.plot(cnnEpochLogs.history['mse'], color='red', label='mse')
    plt.plot(cnnEpochLogs.history['val_mse'], color='blue', label='val_mse')
    fig.suptitle('Mean Squared Error', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()

    #Mean Absolute Error over Epochs
    fig = plt.figure()
    plt.plot(cnnEpochLogs.history['mae'], color='red', label='mae')
    plt.plot(cnnEpochLogs.history['val_mae'], color='blue', label='val_mae')
    fig.suptitle('Mean Absolute Error', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()

    #Mean Absolute Percentage Error over Epochs
    fig = plt.figure()
    plt.plot(cnnEpochLogs.history['mape'], color='red', label='mape')
    plt.plot(cnnEpochLogs.history['val_mape'], color='blue', label='val_mape')
    fig.suptitle('Mean Absolute Percentage Error', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()

    #PRINTING RESULTS FROM EPOCHS
    #Loss over Epochs
    fig = plt.figure()
    plt.plot(cnnEpochLogs.history['loss'], color='red', label='loss')
    plt.plot(cnnEpochLogs.history['val_loss'], color='blue', label='val_loss')
    fig.suptitle('Loss', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()

    for batch in test.as_numpy_iterator():
        testData, testEVMValue = batch
        predictedEVM = np.squeeze(cnn.predict(testData))

    print("Test EVM Value:", testEVMValue)
    print("Predicted EVM: ",predictedEVM)

    #Calculating the MEAN SQUARE ERROR ON TEST SET
    RMSE = np.sqrt(np.mean((testEVMValue - predictedEVM)**2))
    print("Root Mean Squared Error: ", RMSE)
    
    # DISTRIBUTION OF ERRORS, PERFECT SCORE IS 1.0, BASELINE MODEL IS 0 and anything below is worse than baseline
    r2Score = r2_score(testEVMValue, predictedEVM)
    print("Test R^2 score: ", r2Score)


    cnn.save(os.path.join('Model', 'mdgEVMFitnessModel'))


def EVMFitnessArray():
    location = pathlib.Path('Systems\EVMFitness')
    EVMCountArray = []

    rootDirectory = 'Systems\ResizedBitmaps'

    for evmValue in location.iterdir():
            fitnessVal = int(np.genfromtxt(evmValue, encoding = 'utf-8'))
            EVMCountArray.append(fitnessVal)
            try:
                path = os.path.join(rootDirectory,str(fitnessVal))
                os.mkdir(path)
            except FileExistsError:
                pass
    
    return EVMCountArray


def Move2CorrectFolder(EVMarr):
    location = pathlib.Path('Systems\ResizedBitmaps')

    i = 0

    for bitmap in location.iterdir():
        if os.path.isfile(bitmap):
            print(EVMarr[i])
            newLocation = os.path.join(location,str(EVMarr[i]),bitmap.name)
            os.rename(bitmap, newLocation)
            i+=1



def getClassCounts():
    location = pathlib.Path('Systems\Bitmaps')
    classCountArray = []
    for bitmap in location.iterdir():
            classCountArray.append(len(he.classNames(bitmap))-1)
    
    return classCountArray

def createModel():
    model = models.Sequential()

    model.add(layers.Conv2D(16,(4,4), 1, activation='relu', input_shape = (400,400,3)) )
    model.add(layers.AveragePooling2D((2,2)))

    model.add(layers.Conv2D(32, (2,2), 1, activation='relu'))
    model.add(layers.AveragePooling2D((2,2)))


    model.add(layers.Flatten())

    model.add(layers.Dense(32,activation='relu'))
    model.add(layers.Dense(20, activation='relu'))
    model.add(layers.Dense(1))                      # FINAL OUTPUT LAYER


    model.compile(optimizer='adam',
    loss = tf.keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error"),
    metrics = ['mse', 'mae', 'mape'])

    print(model.summary())

    return model

def performance():
    print("test")

if __name__ == "__main__":

    # USED TO CREATE FOLDER IN THE SYSTEMS/RESIZEDBITMAPS WITH THE CORRECT EVM VALUES AS NAMES
    # THE FOLDERS ARE USED AS LABELS IN THE KERAS PIPELINE
    # EVMarr = EVMFitnessArray()

    # MOVES THE RESIZEDBITMAPS TO THE CORRECT FOLDER BASED ON THE EVM VALUE THAT HAS BEEN PREVIOUSLY CALCULATED
    # Move2CorrectFolder(EVMarr)


    processData()

