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
from Champion import Champion

find = []

methods = [
    # "cv2.TM_CCOEFF",
    # "cv2.TM_CCOEFF_NORMED",
    # "cv2.TM_CCORR",
    # "cv2.TM_CCORR_NORMED",
    "cv2.TM_SQDIFF",
    "cv2.TM_SQDIFF_NORMED",
]
large_image = cv2.imread(
        "./Data/Source_Images/Training_Images/map0.jpg"
    )

for m in methods:
    method = eval(m)
    index = 0
    for p in ["icon_ui_inhibitor_minimap_v2_red"]:
        structure = cv2.imread("./4_Analysis/match/" + p + ".png" )

        #structure_color = cv2.cvtColor(structure, cv2.COLOR_G2RGBA)
        structure = cv2.resize(structure, (17,17))
        result = cv2.matchTemplate(structure, large_image, method)
        
         # averga color grey * color red

        # We want the minimum squared difference
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        # add result
        find.append(
            {
                "index": index,
                "champ": p,
                "confidence": min_val,
                "function": method,
                "location": min_loc,
                "result": -1,
            }
        )
        index += 1

print(find)

r = []

for c in find:
    trows, tcols = structure.shape[:2]
    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(
        large_image,
        (c["location"][0], c["location"][1]),
        (c["location"][0] + tcols, c["location"][1] + trows),
        (0, 0, 255),
        1,
    )
    cv2.putText(
        large_image,
        c["champ"],
        (c["location"][0], c["location"][1] - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.3,
        (255, 255, 255),
        1,
        cv2.FILLED,
    )


    cv2.imwrite("tmp/result+" +"tw"+ ".png", large_image)

    indexFind = []
    for a in r:
        if a["index"] not in indexFind:
            indexFind.append(a["index"])

    

    print(len(indexFind))