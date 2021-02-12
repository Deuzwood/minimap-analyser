from __future__ import absolute_import, division, print_function, unicode_literals
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
data_path = os.path.join(racine_path, "0_Light", "Data")
training_images_path = os.path.join(data_path, "Training")
res_path = os.path.join(racine_path, "0_Light", "res")
init_images_path = os.path.join(racine_path, "Data", "Source_Images", "Init_Images")

blue_file = os.path.join(init_images_path, "blue.png")
red_file = os.path.join(init_images_path, "red.png")
rift_file = os.path.join(init_images_path, "rift.png")

data_classes_file = os.path.join(data_path, "data_classes.txt")
data_train_file = os.path.join(data_path, "data_train.txt")


sys.path.append(const_path)

import argparse
import numpy as np
from PIL import Image, ImageDraw
import json
import const
import cv2
import random
import tensorflow as tf

# from tensorflow.keras import datasets, layers, models
from tensorflow import keras
import time

champions_list_path = os.path.join(racine_path, const.CHAMPIONS_LIST_PATH)
champions_tile_path = os.path.join(racine_path, const.CHAMPIONS_TILE_PATH)

# Params default
nbGeneratedTile = 100
nbChampions = 2
train = False

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
        default=nbGeneratedTile,
        help="Number of fake map generated. Default is " + str(nbGeneratedTile),
    )

    parser.add_argument(
        "--champions",
        "-c",
        type=int,
        default=nbChampions,
        help="Number of champions trained generated. Default is " + str(nbChampions),
    )

    parser.add_argument(
        "--train",
        "-t",
        type=bool,
        default=train,
        help="Number of champions trained generated. Default is " + str(train),
    )

    FLAGS = parser.parse_args()

    # Create 26*26 tile for all champs
    with open(champions_list_path, "r") as json_file:
        data = json.load(json_file)
        data = data["data"]
        for p in data:
            p_file = os.path.join(champions_tile_path, (p + ".png"))
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
            save_file = os.path.join(res_path, (p + ".png"))
            output.save(save_file)

    # PARAMS
    red = Image.open(red_file)
    blue = Image.open(blue_file)

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

        f = open(data_classes_file, "w")
        f.write("\n".join(data_classes))
        f.close()

    text = []

    train_images = []
    train_labels = []
    test_images = []
    test_labels = []

    for index in range(FLAGS.champions):
        for i in range(FLAGS.number):
            # print(index, _list[index])
            rift = Image.open(rift_file)

            randomChampImage = Image.open(res_path + ("/" + _list[index] + ".png"))
            x = random.randint(10, 226)
            y = random.randint(10, 226)
            rift.paste(randomChampImage, (x, y), randomChampImage)
            rift.paste(red, (x, y), red)
            rift = rift.crop((x, y, x + 26, y + 26))

            row = (
                " "
                + str(x)
                + ","
                + str(y)
                + ","
                + str(x + 26)
                + ","
                + str(y + 26)
                + ","
                + str(index)
            )

            out = rift.convert("RGB")
            out_file = os.path.join(
                training_images_path, "tile_" + str(index) + "_" + str(i) + ".jpg"
            )
            out.save(
                out_file,
                quality=90,
            )
            text.append(row)

            # Then create file

            img = cv2.imread(out_file)
            img = cv2.resize(img, (24, 24))
            r_max = int(1 / 0.1)
            r = random.randint(1, r_max)
            if r == 1:
                test_images.append(img)
                test_labels.append(index)
            else:
                train_images.append(img)
                train_labels.append(index)

    f = open(training_images_path + "/data_train.txt", "w")
    f.write("\n".join(text))
    f.close()

# Generate crop image from minimap


# create data_classe and data_train

train_images = np.array(train_images)
train_labels = np.array(train_labels)
test_images = np.array(test_images)
test_labels = np.array(test_labels)

np.save(training_images_path + "train_images", train_images)
np.save(training_images_path + "train_labels", train_labels)
np.save(training_images_path + "test_images", test_images)
np.save(training_images_path + "test_labels", test_labels)

print("Train images size: " + str(train_images.shape))
print("Train labels size: " + str(train_labels.shape))


### Train set
if FLAGS.train is not False:
    # Define a checkpoint path and a checkpoint saving callback
    checkpoint_path = "checkpoints/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path, save_weights_only=True, verbose=1
    )

    # Load the training sets and testing sets created earlier
    train_images = np.load(training_images_path + "train_images.npy")
    train_labels = np.load(training_images_path + "train_labels.npy")
    test_images = np.load(training_images_path + "test_images.npy")
    test_labels = np.load(training_images_path + "test_labels.npy")

    # Make sure that the training set and testing set are not empty
    assert not np.any(np.isnan(train_images))
    assert not np.any(np.isnan(test_images))

    # Normalize pixel values to be between 0 and 1
    train_images, test_images = train_images / 255.0, test_images / 255.0

    # Define the model
    model = keras.models.Sequential()
    model.add(
        keras.layers.Conv2D(16, (3, 3), activation="relu", input_shape=(24, 24, 3))
    )
    model.add(
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")
    )
    model.add(keras.layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(
        keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding="valid")
    )

    model.add(keras.layers.Flatten())
    model.add(
        keras.layers.Dense(
            12,
            kernel_regularizer=keras.regularizers.l2(0.001),
            activation="relu",
            input_shape=train_images.shape[2:],
        )
    )
    model.add(keras.layers.Dense(FLAGS.champions, activation="softmax"))

    # Print a summary of the model
    model.summary()

    # Compile the model
    model.compile(
        optimizer="Adadelta",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    history = model.fit(train_images, train_labels, epochs=100, callbacks=[cp_callback])

    test_loss, test_acc = model.evaluate(test_images, test_labels)

    print("Test Accuracy：" + str(test_acc * 100) + "%")
    # model.save('model/my_model.h5')
    model.save("my_model.h5")


# Load the tensorflow model and restore it
lol_model = tf.keras.models.load_model("my_model.h5")
lol_model.summary()
lol_model.load_weights("checkpoints/cp.ckpt")


# The path for all the images of the video we are analyzing
image_path = data_path + "/map/"

# image = Image.open(image_path + "map6.jpg").convert("RGB")
image = cv2.imread(image_path + "map6.jpg")

# img = np.array(img)
# print(img.shape)


def predict(image_list):
    image_np = np.stack(
        image_list,
        axis=0,
    )
    prediction = lol_model.predict(image_np)
    output = [np.argmax(prediction[n]) for n in range(prediction.shape[0])]
    return output, prediction


# prediction = lol_model.predict(img)
# output = [np.argmax(prediction[n]) for n in range(prediction.shape[0])]
radius = 12  # the radius for all the circles to crop out

cropped_list = []  # The list of all champions in an image
coord_list = []  # The list of all the coordinate of the champions

b, g, r = cv2.split(image)
inranger = cv2.inRange(r, 120, 255)
inrangeg = cv2.inRange(g, 120, 255)
inrangeb = cv2.inRange(b, 120, 255)

induction = inranger - inrangeg - inrangeb

circles = cv2.HoughCircles(
    induction,
    cv2.HOUGH_GRADIENT,
    1,
    10,
    param1=30,
    param2=15,
    minRadius=5,
    maxRadius=30,
)

# If there are champions detected
if circles is not None:
    for n in range(circles.shape[1]):
        x = int(circles[0][n][0])
        y = int(circles[0][n][1])
        try:
            crop_image = image[y - radius : y + radius, x - radius : x + radius].copy()
            cropped_list.append(crop_image)
            coord_list.append((x, y))
            # bg_image[10+n*30:10+n*30+24,300:324] = crop_image
        except:
            pass

    cropped_imagees = np.array(cropped_list)
    champ_prediction, confidence = predict(cropped_imagees)
    print(champ_prediction, confidence)

    for n in range(circles.shape[1]):
        x = int(circles[0][n][0])
        y = int(circles[0][n][1])