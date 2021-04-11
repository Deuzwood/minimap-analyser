import os
import sys

def get_parent_dir(n=1):
    """returns the n-th parent dicrectory of the current
    working directory"""
    current_path = os.path.dirname(os.path.abspath(__file__))
    for _ in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

# --------------------
# Constant file
# --------------------

# League of Legends Version
LATEST_VERSION = "11.2.1"
dragontail = "dragontail-" + LATEST_VERSION

# GENERAL PATHS
racine_path = get_parent_dir(1)
const_path = os.path.join(racine_path, "Const")
data_path = os.path.join(racine_path,"Data")
res_path = os.path.join(racine_path,"res")
init_images_path = os.path.join(data_path,"Source_Images","Init_Images")
training_images_path = os.path.join(data_path,"Source_Images","Training_Images")
minimap_images_path = os.path.join(data_path,"Source_Images","Minimap")
model_weights_path = os.path.join(data_path,"Model_Weights")
champions_img_path = os.path.join(racine_path,dragontail,LATEST_VERSION,"img","champion")


# FILES
blue_file = os.path.join(init_images_path,"blue.png")
red_file = os.path.join(init_images_path,"red.png")
rift_file = os.path.join(init_images_path,"rift.png")
yuumi_blue_file = os.path.join(init_images_path,"yuumi_blue.png")
yuumi_red_file = os.path.join(init_images_path,"yuumi_red.png")
yuumi_file = os.path.join(init_images_path,"yuumi.png")
data_classes_file = os.path.join(model_weights_path,"data_classes.txt")
data_train_file = os.path.join(training_images_path,"data_train.txt")
champions_list_file = os.path.join(racine_path,dragontail,LATEST_VERSION,"data","fr_FR","champion.json")




# CDN
CDN_DOWNLOAD_LINK = (
    "https://ddragon.leagueoflegends.com/cdn/dragontail-" + LATEST_VERSION + ".tgz"
)

# List path from Data Dragon
CHAMPIONS_LIST_PATH = (
    os.path.join(dragontail,LATEST_VERSION,"data","fr_FR","champion.json")
)

# Tile Path
CHAMPIONS_TILE_PATH = (
    os.path.join(dragontail,LATEST_VERSION,"img","champion")
)


# red = #de2f2f
# blue = #1580b6

# Picker from yummi on minimap
# blue = #3769cc
# red = #ae302b