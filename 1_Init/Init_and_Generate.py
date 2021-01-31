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

import argparse
import numpy as np
from PIL import Image, ImageDraw
import json
import const
import random

# Params default
nbGeneratedMap = 300

if __name__ == "__main__":
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    """
    Command line options
    """

    parser.add_argument(
        "--number",
        "-n",
        type=int,
        default=nbGeneratedMap,
        help="Number of fake map generated. Default is " + str(nbGeneratedMap),
    )

    FLAGS = parser.parse_args()

    # Create 26*26 tile for all champs
    with open(const.CHAMPIONS_LIST_PATH, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        for p in data:
            img = Image.open(const.CHAMPIONS_TILE_PATH + p + ".png").convert("RGB")
            npImage = np.array(img)
            h, w = img.size

            # Create same size alpha layer with circle
            alpha = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0, 0, h, w], 0, 360, fill=255)

            # Convert alpha Image to numpy array
            npAlpha = np.array(alpha)

            # Add alpha layer to RGB
            npImage = np.dstack((npImage, npAlpha))

            # Save with alpha / 26*26 resize
            output = Image.fromarray(npImage)
            output = output.resize((26, 26), 4)
            output.save("res/" + p + ".png")

    # PARAMS

    nbChampionsPerMap = 10
    trainingImagePath = (
        "/content/TrainYourOwnYOLO/Data/Source_Images_Training_Images/vott-csv-export/"
    )
    red = Image.open("./Data/Source_Images/Init_Images/red.png")
    blue = Image.open("./Data/Source_Images/Init_Images/blue.png")
    yuumi_red = Image.open("./Data/Source_Images/Init_Images/yuumi_red.png")
    yuumi_blue = Image.open("./Data/Source_Images/Init_Images/yuumi_blue.png")

    _list = {}

    with open(const.CHAMPIONS_LIST_PATH, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        i = 0
        data_classes = []
        for p in data:
            _list[i] = p
            data_classes.append(p)
            i += 1

        print("Loading champions list done")
        print("Number of champions : " + str(len(_list)))
        # print("Champion aux hasard : "+_list[random.randint(0,len(_list))])

        f = open("./Data/Model_Weights/data_classes.txt", "w")
        f.write("\n".join(data_classes))
        f.close()

    text = []
    redBool = True

    for mapIndex in range(FLAGS.number):
        rift = Image.open("./Data/Source_Images/Init_Images/rift.png")
        randomList = random.sample(list(_list), nbChampionsPerMap)
        row = "map" + str(mapIndex) + ".jpg"
        lastRed = (-1, -1)
        lastBlue = (-1, -1)
        for randomChampIndex in randomList:
            randomChampImage = Image.open("res/" + _list[randomChampIndex] + ".png")
            x = random.randint(10, 226)
            y = random.randint(10, 226)

            if (
                _list[randomChampIndex] != "Yuumi"
                or lastBlue[0] == -1
                or random.random() > 0.4
            ):
                rift.paste(randomChampImage, (x, y), randomChampImage)
                if redBool == True:
                    lastRed = (x, y)
                    rift.paste(red, (x, y), red)
                    redBool = False
                else:
                    lastBlue = (x, y)
                    rift.paste(blue, (x, y), blue)
                    redBool = True
            else:
                if redBool == True:
                    rift.paste(yuumi_red, (lastRed[0] - 3, lastRed[1] - 6), yuumi_red)
                    redBool = False
                    x = lastRed[0]
                    y = lastRed[1]
                else:
                    rift.paste(
                        yuumi_blue, (lastBlue[0] - 3, lastBlue[1] - 6), yuumi_blue
                    )
                    redBool = True
                    x = lastBlue[0]
                    y = lastBlue[1]
            row += (
                " "
                + str(x)
                + ","
                + str(y)
                + ","
                + str(x + 26)
                + ","
                + str(y + 26)
                + ","
                + str(randomChampIndex)
            )

        out = rift.convert("RGB")
        out.save(
            "./Data/Source_Images/Training_Images/map" + str(mapIndex) + ".jpg",
            quality=90,
        )
        text.append(row)

    f = open("./Data/Source_Images/Training_Images/data_train.txt", "w")
    f.write("\n".join(text))
    f.close()
    print("Generated", FLAGS.number, "maps")
