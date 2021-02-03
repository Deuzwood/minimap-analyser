import numpy as np
from PIL import Image


# Compare np.Array in %
def compare(source , target):
    if(target.shape[:2] != source.shape[:2]):
        return -1
    result = np.zeros(source.shape)
    for i in range(np.size(source,0)):
        for j in range(np.size(source,1)):
            result[i,j] = 1 if(source[i,j][0]==target[i,j][0] and source[i,j][1]==target[i,j][1] and source[i,j][2]==target[i,j][2]) else 0
    #print(result)
    #print(result.sum()/source.size)
    return np.sum(result)


# load the image
source = Image.open("./res/Blitzcrank.png")
target = Image.open("./res/Blitzcrank.png")
# convert image to numpy array
source = np.asarray(source)
target = np.asarray(target)

compare(source, target)

#find the best pos between source (Blitz) and generated map
# 10,195,36,221,12 blitz
target = Image.open("./4_Analysis/match/map0.jpg")
target = np.asarray(target)

result = np.zeros(target.shape)

for i in range(np.size(target,0)):
    for j in range(np.size(target,1)):
        result[i,j] = compare(source, target[i:i+26, j:j+26])
print(np.unravel_index(np.argmax(result, axis=None), result.shape[:2]))