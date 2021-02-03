# 10,195,36,221,12 blitz

from PIL import Image
from numpy import asarray

# from https://www.pluralsight.com/guides/importing-image-data-into-numpy-arrays

# load the image
image = Image.open("./res/Blitzcrank.png")
m = Image.open("./4_Analysis/match/map0.jpg")
# convert image to numpy array
data = asarray(image)
print(type(data))

datam = asarray(m)
# summarize shape
print(data.shape)
print(datam.shape)

print(data[15][15])
match = 0

comparison = data == datam
equal_arrays = comparison.all()
print(equal_arrays)

print(match) 
# one solutions : circle champs on map into array to compare with real champs.
