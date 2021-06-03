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
from csv import reader
import const


stats = [[0, 0], [0, 0]]


# generate confusion matrix
size = 154
confusion = [[0] * 2 for i in range(size)]
trueFalseTab = [[0] * 2 for i in range(size)]

predictions = pd.read_csv(
    os.path.join(get_current_dir(1), "Data", "Evaluation", "detection.csv")
)

positions = pd.read_csv(
    os.path.join(get_current_dir(1), "Data", "Evaluation", "data_train.csv")
)

#pathList = positions["path"]
paths = positions.drop_duplicates(subset=['path'],keep='first')
pathList = []
for index, row in paths.iterrows():
    pathList.append(row["path"])

for image in pathList:
    pass

    savedPredicitions = predictions.loc[
        lambda predictions: predictions["image"] == image
    ]

    savedPosition = positions.loc[
        lambda positions: positions["image"] == image
        ]

    for index, prediction in savedPredicitions.iterrows():
        if()



# TP if IoU >= 0.5 0
# FP if IoU < 0.5  1
# FN in image but not detected 2    
#
#TP FP
#FN TN

# si etat différent de 0 alors on boucle sur l'image pour avoir le meilleur IoU
# pour savoir avec qui on s'est trompé (uniquement le max avec iou > 0.5)