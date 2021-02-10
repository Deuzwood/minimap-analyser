import os
import sys
import math
import random


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

    # PARAMS


    nbChampionsPerMap = 10
    nbChampions = len(_list)
    listTest = [0]*nbChampions
    red = Image.open(red_file)
    blue = Image.open(blue_file)
    yuumi_red = Image.open(yuumi_red_file)
    yuumi_blue = Image.open(yuumi_blue_file)

    text = []
    
    randomIndexList = list(range(nbChampions))
    #random.shuffle(randomIndexList)

    def generateMap(mapIndex,startIndex,redOrBlue):
        rift = Image.open(rift_file)
        row = training_images_path+"/map" + str(mapIndex) + ".jpg"
        for i in range(nbChampionsPerMap):
            if (i+startIndex >= nbChampions):
                break

            random_image_file = os.path.join(res_path,(_list[randomIndexList[startIndex+i]] + ".png"))
            listTest[randomIndexList[startIndex+i]]+=1
            randomChampImage = Image.open(random_image_file)
            
            x = random.randint(10, 226)
            y = random.randint(10, 226)
            rift.paste(randomChampImage, (x, y), randomChampImage)
            if ((i+redOrBlue)%2==0):
                rift.paste(red, (x, y), red)
            else :
                rift.paste(blue, (x, y), blue)
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
                    + str(randomIndexList[startIndex+i])
                )
        out = rift.convert("RGB")
        out_file = os.path.join(training_images_path,"map"+str(mapIndex)+".jpg")
        out.save(
            out_file,
            quality=90,
        )
        text.append(row)

    def generateMapSuperposition(mapIndex,startIndex,redOrBlue,xPos,yPos,xMove,yMove):
        rift = Image.open(rift_file)
        row = training_images_path+"/map" + str(mapIndex) + ".jpg"
        x = xPos
        y = yPos
        for i in range(nbChampionsPerMap):
            if (i+startIndex >= nbChampions):
                break

            random_image_file = os.path.join(res_path,(_list[randomIndexList[startIndex+i]] + ".png"))
            listTest[randomIndexList[startIndex+i]]+=1
            randomChampImage = Image.open(random_image_file)
            
            x += math.floor(random.uniform(0.2,1)*26) * xMove
            y += math.floor(random.uniform(0.2,1)*26) * yMove
            rift.paste(randomChampImage, (x, y), randomChampImage)
            if ((i+redOrBlue)%2==0):
                rift.paste(red, (x, y), red)
            else :
                rift.paste(blue, (x, y), blue)
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
                    + str(randomIndexList[startIndex+i])
                )
        out = rift.convert("RGB")
        out_file = os.path.join(training_images_path,"map"+str(mapIndex)+".jpg")
        out.save(
            out_file,
            quality=90,
        )
        text.append(row)

def generateMaps(nbMaps):
    mapIndex = 0
    while (mapIndex < nbMaps/2):
        random.shuffle(randomIndexList)
        listIndex = 0
        while (listIndex < nbChampions):
            # red
            generateMapSuperposition(mapIndex, listIndex, 0, 10,10,1,1)
            mapIndex += 1
            # blue
            generateMapSuperposition(mapIndex, listIndex, 1, 10, 200, 1, -1)
            mapIndex += 1
            listIndex += nbChampionsPerMap
    while (mapIndex < nbMaps):
        random.shuffle(randomIndexList)
        listIndex = 0
        while (listIndex < nbChampions):
            # red
            generateMap(mapIndex, listIndex, 0)
            mapIndex += 1
            # blue
            generateMap(mapIndex, listIndex, 1)
            mapIndex += 1
            listIndex += nbChampionsPerMap









generateMaps(FLAGS.number)
print(listTest)


f = open(training_images_path+"/data_train.txt", "w")
f.write("\n".join(text))
f.close()