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
data_path = os.path.join(racine_path,"Data")
res_path = os.path.join(racine_path,"res")
init_images_path = os.path.join(data_path,"Source_Images","Init_Images")
training_images_path = os.path.join(data_path,"Source_Images","Training_Images")
model_weights = os.path.join(data_path,"Model_Weights")


blue_file = os.path.join(init_images_path,"blue.png")
red_file = os.path.join(init_images_path,"red.png")
rift_file = os.path.join(init_images_path,"rift.png")
yuumi_blue_file = os.path.join(init_images_path,"yuumi_blue.png")
yuumi_red_file = os.path.join(init_images_path,"yuumi_red.png")
data_classes_file = os.path.join(model_weights,"data_classes.txt")
data_train_file = os.path.join(training_images_path,"data_train.txt")






sys.path.append(const_path)

import argparse
import numpy as np
from PIL import Image, ImageDraw
import json
import const
import random

champions_list_path = os.path.join(racine_path, const.CHAMPIONS_LIST_PATH)
champions_tile_path = os.path.join(racine_path, const.CHAMPIONS_TILE_PATH)

# Params default
nbGeneratedMap = 10

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
    with open(champions_list_path, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        for p in data:
            p_file = os.path.join(champions_tile_path, (p+".png"))
            img = Image.open(p_file).convert("RGB")
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
            save_file = os.path.join(res_path,(p+".png"))
            output.save(save_file)

    # PARAMS

    nbChampionsPerMap = 10
    red = Image.open(red_file)
    blue = Image.open(blue_file)
    yuumi_red = Image.open(yuumi_red_file)
    yuumi_blue = Image.open(yuumi_blue_file)

    _list = {}

    with open(champions_list_path, "r") as json_file:
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

        f = open(model_weights+"/data_classes.txt", "w")
        f.write("\n".join(data_classes))
        f.close()

    text = []
    redBool = True

    for mapIndex in range(FLAGS.number):
        rift = Image.open(rift_file)
        randomList = random.sample(list(_list), nbChampionsPerMap)
        row = "map" + str(mapIndex) + ".jpg"
        lastRed = (-1, -1)
        lastBlue = (-1, -1)
        for randomChampIndex in randomList:
            random_image_file = os.path.join(res_path,(_list[randomChampIndex] + ".png"))
            randomChampImage = Image.open(random_image_file)
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
        out_file = os.path.join(training_images_path,"map"+str(mapIndex)+".jpg")
        out.save(
            out_file,
            quality=90,
        )
        text.append(row)

    f = open(training_images_path+"/data_train.txt", "w")
    f.write("\n".join(text))
    f.close()
    print("Generated", FLAGS.number, "maps")
