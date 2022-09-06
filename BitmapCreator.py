import matplotlib.pyplot as plt
import helpers as he
import pathlib
import cv2
from tqdm import tqdm


def directoryNavigation():
    location = pathlib.Path('Systems\MDGs')
    for mdg in tqdm(location.iterdir()):

        matrix = he.bitmapStripper(mdg)

        mdgname = mdg.name.removesuffix(".csv")
        saveLocation = 'Systems\Bitmaps\\'+mdgname+'.png'
        resizeLocation = 'Systems\ResizedBitmaps\\'+mdgname+'--Resized.png'

        plt.imsave(saveLocation,matrix)

        resizeImages(saveLocation, resizeLocation)

def resizeImages(location, newLocation):
    image = cv2.imread(location, cv2.IMREAD_UNCHANGED)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    desiredSize = [400,400]
    dimension = image.shape
    if dimension[0]>desiredSize[0]:
        resizedImage = cv2.resize(grayImage, desiredSize, interpolation= cv2.INTER_AREA)
    else:
        resizedImage = cv2.resize(grayImage, desiredSize, interpolation= cv2.INTER_NEAREST_EXACT)
    

    
    cv2.imwrite(newLocation, resizedImage)

if __name__ == "__main__":
    directoryNavigation()
