import os
import sys


def get_current_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


def get_const_dir():
    return os.path.join(get_current_dir(1), "Const")


const = get_const_dir()
sys.path.append(const)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


stats = [[0, 0], [0, 0]]


# generate confusion matrix
size = 154
confusion = [[0] * 2 for i in range(size)]

predictions = pd.read_csv(
    os.path.join(get_current_dir(1), "Data", "Evaluation", "detection.csv")
)

# adapted from https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
def intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(int(boxA[0]), boxB["xmin"])
    yA = max(int(boxA[1]), boxB["ymin"])
    xB = min(int(boxA[2]), boxB["xmax"])
    yB = min(int(boxA[3]), boxB["ymax"])
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (int(boxA[2]) - int(boxA[0]) + 1) * (int(boxA[3]) - int(boxA[1]) + 1)
    boxBArea = (boxB["xmax"] - boxB["xmin"] + 1) * (boxB["ymax"] - boxB["ymin"] + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


with open(
    os.path.join(get_current_dir(1), "Data", "Evaluation", "data_train.txt")
) as dataTrain:
    line = dataTrain.readline()
    cnt = 0
    # for each line
    while line:
        line = line.split(" ")
        imgPath = line.pop(0)

        i = 0
        for o in line:
            line[i] = o.replace("\n", "").split(",")
            i += 1

        # find all prediction corresponding to this line
        savedPredicitions = predictions.loc[
            lambda predictions: predictions["image_path"] == imgPath
        ]

        # compare prediction and data
        # check same label and postion using IoU
        to_rm = []
        success = False
        for index, prediction in savedPredicitions.iterrows():
            for d in line:
                if (
                    int(d[4]) == int(prediction.label)
                    and intersection_over_union(d, prediction) > 0.5
                ):
                    confusion[int(d[4])][0] += 1
                    stats[0][0] += 1
                    to_rm.append(index)
                    success = True
            if not success:
                confusion[int(prediction.label)][1] += 1
            success = False

        # rm all index already find

        # suivant
        line = dataTrain.readline()
        cnt += 1


ax = sb.heatmap(confusion)
plt.show()
print(confusion)

print(stats)
