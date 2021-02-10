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

lineNumber = 1
for lineNumber in range(0, 20):
    large_image = cv2.imread(
        "./Data/Source_Images/Training_Images/map" + str(lineNumber) + ".jpg"
    )
    # method = cv2.TM_SQDIFF_NORMED
    find = []

    """ cv::TemplateMatchModes {
    cv::TM_SQDIFF = 0,
    cv::TM_SQDIFF_NORMED = 1,
    cv::TM_CCORR = 2,
    cv::TM_CCORR_NORMED = 3,
    cv::TM_CCOEFF = 4,
    cv::TM_CCOEFF_NORMED = 5
    }
    """

    """ with open(const.CHAMPIONS_LIST_PATH, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        index = 0
        for m in range(0, 5):
            for p in data:

                small_image = cv2.imread("./res/" + p + ".png")
                result = cv2.matchTemplate(small_image, large_image, m)
                # We want the minimum squared difference
                mn, _, mnLoc, _ = cv2.minMaxLoc(result)
                if mn < 0.3:
                    # Draw the rectangle:
                    # Extract the coordinates of our best match
                    MPx, MPy = mnLoc
                    # Step 2: Get the size of the template. This is the same size as the match.
                    trows, tcols = small_image.shape[:2]
                    # Step 3: Draw the rectangle on large_image
                    cv2.rectangle(
                        large_image, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 1
                    )
                    cv2.putText(
                        large_image,
                        p,
                        (MPx, MPy - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.3,
                        (255, 255, 255),
                        1,
                        cv2.FILLED,
                    )
                    # add result
                    find.append(
                        {
                            "index": index,
                            "champ": p,
                            "confidence": mn,
                            "function": cv2.TM_SQDIFF_NORMED,
                            "location": mnLoc,
                            "result": -1,
                        }
                    )
                index += 1


    cv2.imwrite("result.png", large_image) """

    methods = [
        # "cv2.TM_CCOEFF",
        # "cv2.TM_CCOEFF_NORMED",
        # "cv2.TM_CCORR",
        # "cv2.TM_CCORR_NORMED",
        "cv2.TM_SQDIFF",
        "cv2.TM_SQDIFF_NORMED",
    ]

    with open(const.CHAMPIONS_LIST_PATH, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]

        for m in methods:
            method = eval(m)
            index = 0
            for p in data:
                small_image = cv2.imread("./res/" + p + ".png")
                result = cv2.matchTemplate(small_image, large_image, method)
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

    real = []
    champs = []

    with open("./Data/Source_Images/Training_Images/data_train.txt", "r") as data:
        for i in range(0, lineNumber + 1):
            real = data.readline()

    real = real.replace("C:\\Users\\nicol\\Documents\\minimap-analyser\\Data\\Source_Images\\Training_Images/map" + str(lineNumber) + ".jpg ", "")
    real = real.split(" ")
    for s in real:
        s = s.split(",")
        champs.append(Champion(s))
    r = []
    for finded in find:

        for c in champs:
            if (
                finded["index"] == c.idChampion
                and finded["location"][0] == c.xmin
                and finded["location"][1] == c.ymin
            ):
                finded["result"] = 1
                r.append(finded)

    functionRes = []
    for m in range(0, 6):
        sum = 0
        for f in find:
            if f["function"] == m:
                sum += f["result"]

        functionRes.append(sum)
    print(functionRes)

    for c in r:
        trows, tcols = small_image.shape[:2]
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

    cv2.imwrite("tmp/result+" + str(lineNumber) + ".png", large_image)

    indexFind = []
    for a in r:
        if a["index"] not in indexFind:
            indexFind.append(a["index"])

    print(len(indexFind))