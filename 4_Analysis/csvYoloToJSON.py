import os
import sys


def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


racine_path = get_parent_dir(1)
const_path = os.path.join(racine_path, "Const")

data_classes_file = os.path.join(
    racine_path, "Data", "Model_Weights", "data_classes.txt"
)
sys.path.append(const_path)

import argparse
import numpy as np
from PIL import Image, ImageDraw
import json
import const

if __name__ == "__main__":
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """

    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default=None,
        help="Fill to transcript. Default is " + str(None),
    )

    FLAGS = parser.parse_args()

    yolo = open(FLAGS.file)
    classes = open(data_classes_file)

    # skip first
    line = yolo.readline()

    line = yolo.readline()
    label = []
    while line:
        line = line.split(",")
        label.append(int(line[4]))
        line = yolo.readline()
    yolo.close()
    label.sort()
    current = 0
    last = -1
    l = []
    for i in label:
        if i != last:
            l.append({"label": i, "apparition": current})
            current = 0
            last = i
        current += 1
    maxA = []
    for i in range(11):
        m = {"apparition": 0}
        index = 0
        itor = 0
        for d in l:
            if m["apparition"] < d["apparition"]:
                m = d
                itor = index
            index += 1
        maxA.append(m)
        l.pop(itor)
    toKeep = []
    for o in maxA:
        toKeep.append(o["label"])

    toKeep.sort()
    print(toKeep)
    toKeep.pop(0)

    yolo = open(FLAGS.file)
    # skip first
    line = yolo.readline()
    line = yolo.readline()
    label = []
    frame = 0
    cleanYolo = []
    while line:
        if (
            int(line.split(",")[4]) + 1 in toKeep
            or float(line.split(",")[5].replace("\n", "")) == -1
        ):

            cleanYolo.append(line)
        line = yolo.readline()
    yolo.close()

    f = open(racine_path + "/t.txt", "w")
    f.write("".join(cleanYolo))
    f.close()

    ## TODO add xmin,ymin,xmax,ymax,label,confidence in head of file simple
    ## TODO
    ## TODO

    # continue with clean version
    analyse = []
    f = open(racine_path + "/t.txt")
    line = f.readline()
    allClasses = classes.readlines()
    while line:
        if float(line.split(",")[5].replace("\n", "")) == -1:
            frame += 1
        else:
            line = line.split(",")
            analyse.append(
                {
                    "center": {
                        "x": (int(line[0]) + int(line[2])) / 2,
                        "y": (int(line[1]) + int(line[3])) / 2,
                    },
                    "xmin": int(line[0]),
                    "ymin": int(line[1]),
                    "xmax": int(line[2]),
                    "ymax": int(line[3]),
                    "label": int(line[4]),
                    "name": allClasses[int(line[4])].replace("\n", ""),
                    "frame": frame,
                }
            )
        line = f.readline()
    f.close()

    f = open(racine_path + "/t_analyse.txt", "w")
    f.write("[")
    for li in analyse:
        f.write(json.dumps(li) + ",")
    f.write("]")
    f.close()

    greyRiftImage = Image.open(
        os.path.join(racine_path, "Data", "Source_Images", "Minimap", "grey.png")
    )

    # show the image
    a = np.asarray(greyRiftImage)

    greyRiftEquivalence = {
        0: "bluebase",
        93: "Red Jungle",
        130: "Top Lane",
        145: "Mid Lane",
        155: "Bottom Lane",
        187: "Blue Jungle",
        221: "River",
        255: "redbase",
    }

    #
    # Begin stats file
    # stats containe 10 champs, number of time yolo has detected them
    # the repartion concerning the position ( from greyRiftEquilence / greyRift)
    # Main role from position
    # BLUE TEAM value and RED TEAM

    # init
    print(toKeep)
    object_stats = {}
    for champ in toKeep:
        object_stats[champ - 1] = {
            "name": allClasses[champ - 1].replace("\n", ""),
            "label": champ - 1,
            "team": None,  # 0 blue , 1 red
            "position": {
                0: 0,
                93: 0,
                130: 0,
                145: 0,
                155: 0,
                187: 0,
                221: 0,
                255: 0,
            },
            "mainPosition": None,
        }

    # compute
    for li in analyse:
        tmp = a[int(li["center"]["y"]), int(li["center"]["x"])][0]
        object_stats[int(li["label"])]["position"][tmp] += 1

    # select blue or red team
    for obj in object_stats:
        object_stats[obj]["team"] = (
            0
            if object_stats[obj]["position"][0] < object_stats[obj]["position"][255]
            else 1
        )

    print(object_stats)

    # find main position
    for obj in object_stats:
        # find max from position
        max_ = 0
        max_index = 0
        for p in object_stats[obj]["position"].items():
            if p[1] > max_:
                max_ = p[1]
                max_index = p[0]

        for p in object_stats[obj]["position"].items():
            if p[1] == max_:
                print(max_index)
                print(greyRiftEquivalence)
                object_stats[obj]["mainPosition"] = greyRiftEquivalence[int(max_index)]

    f = open(racine_path + "/t_stats.txt", "w")
    f.write(json.dumps(object_stats))
    f.close()