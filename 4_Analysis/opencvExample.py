import os
import sys


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


const_path = os.path.join(get_parent_dir(1), "Const")
sys.path.append(const_path)

import cv2
import numpy as np
import json
import const

large_image = cv2.imread('./Data/Source_Images/Training_Images/map1.jpg')
method = cv2.TM_SQDIFF_NORMED

with open(const.CHAMPIONS_LIST_PATH, 'r') as json_file:
    data = json.load(json_file)
    data = data['data']
    for p in data:

        small_image  = cv2.imread('./res/'+p+'.png')
        result = cv2.matchTemplate(small_image, large_image, method)
        # We want the minimum squared difference
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        if(mn<0.3):
            # Draw the rectangle:
            # Extract the coordinates of our best match
            MPx,MPy = mnLoc
            # Step 2: Get the size of the template. This is the same size as the match.
            trows,tcols = small_image.shape[:2]
            # Step 3: Draw the rectangle on large_image
            cv2.rectangle(large_image, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),1)
            cv2.putText(large_image, p, (MPx,MPy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.3,(255,255,255),1,cv2.FILLED)


cv2.imwrite('result.png', large_image)