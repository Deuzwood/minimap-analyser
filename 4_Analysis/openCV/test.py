import path
import sys
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os

img_name = "H:\M1\Projet\minimap-analyser\Data\Source_Images\Training_Images\map0.jpg"
img_rgb = cv.imread(img_name)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template_name = "H:\M1\Projet\minimap-analyser\Data\Source_Images\Minimap"
template_name = os.path.join(template_name,"tower.png")
template = cv.imread(template_name,0)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
print(res)
threshold = 0.6
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imwrite('res.png',img_rgb)