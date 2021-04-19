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
sys.path.append(const_path)

import argparse
import numpy as np
from PIL import Image, ImageDraw
import json
import const
import random

champions_list_path = os.path.join(racine_path, const.CHAMPIONS_LIST_PATH)
champions_tile_path = os.path.join(racine_path, const.CHAMPIONS_TILE_PATH)


if __name__ == "__main__":
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)

    FLAGS = parser.parse_args()

    # Create 26*26 tile for all champs
    with open(const.champions_list_file, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        # Array reciving all champions name for data classes File
        data_classes = []
        for p in data:
            p_file = os.path.join(const.champions_img_path, (p + ".png"))
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
            save_file = os.path.join(const.res_path, (p + ".png"))
            output.save(save_file)

            # add Champions to data Class
            data_classes.append(p)

        f = open(const.data_classes_file, "w")
        f.write("\n".join(data_classes))
        f.close()

        print(
            "Loading champions list done, tiles are generated and data classes file created"
        )
        print("Number of champions : " + str(len(data)))