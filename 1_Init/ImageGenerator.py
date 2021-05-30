import argparse
import json
import math
import os
import random
import sys

from PIL import Image

import path

const = path.get_const_dir()
sys.path.append(const)

import const


class ImageGenerator:
    def __init__(self):
        self.nbMapsToGenerate = 10
        self.mapIndex = 0

        self.yuumiProba = 200

        self.nbChampionsPerMap = 10
        self.nbChampions = 0
        self.championIndex = 0
        self.championSize = 26

        self.imageSize = 256
        self.minLimit = self.championSize / 2
        self.maxLimit = self.imageSize - 3 * self.championSize / 2

        self.data_train = []

        self.redImage = Image.open(const.red_file)
        self.blueImage = Image.open(const.blue_file)
        self.yuumi_red = Image.open(const.yuumi_red_file)
        self.yuumi_blue = Image.open(const.yuumi_blue_file)

        self.championsList = []
        self.championsListBis = []

        with open(const.champions_list_file, "r") as json_file:
            data = json.load(json_file)
            data = data["data"]
            data_classes = []
            for p in data:
                print(p)
                self.championsList.append(p)
                self.championsListBis.append(p)
                data_classes.append(p)

            print("Loading champions list done")
            self.nbChampions = len(self.championsList)
            print("Nombre de champions : " + str(self.nbChampions))
            print(self.championsList)
            f = open(const.data_classes_file, "w")
            f.write("\n".join(data_classes))
            f.close()
            self.randomIndexList = list(range(self.nbChampions))
            self.listTest = [0] * self.nbChampions

    # random.shuffle(randomIndexList)

    # def randomXY(limit):
    def update(self):
        if self.championIndex >= self.nbChampions:
            self.championIndex = 0
            random.shuffle(self.randomIndexList)

    def getRandomChampionIndex(self, i):
        return self.randomIndexList[self.championIndex + i]

    def getRandomChampion(self, i):
        return self.championsList[self.getRandomChampionIndex(i)]

    def championToString(self, i, x, y):
        return (
            " "
            + str(x)
            + ","
            + str(y)
            + ","
            + str(x + self.championSize)
            + ","
            + str(y + self.championSize)
            + ","
            + str(self.getRandomChampionIndex(i))
        )

    def yuumiToString(self, x, y):
        return (
            " "
            + str(x)
            + ","
            + str(y)
            + ","
            + str(x + 36)
            + ","
            + str(y + 36)
            + ","
            + str(self.championsList.index("Yuumi"))
        )

    def getValidRandomPosition(self):
        return random.randint(self.minLimit, self.maxLimit), random.randint(
            self.minLimit, self.maxLimit
        )

    def isPositionValid(self, x, y):
        return (
            x >= self.minLimit
            and x <= self.maxLimit
            and y >= self.minLimit
            and y <= self.maxLimit
        )

    def generateMap(self, redOrBlue):
        rift = Image.open(const.rift_file)
        mapName = "map" + str(self.mapIndex) + ".jpg"
        row = os.path.join(const.training_images_path, mapName)
        for i in range(self.nbChampionsPerMap):
            if self.championIndex + i >= self.nbChampions:
                break

            randomChampion = self.getRandomChampion(i)
            self.listTest[self.championsList.index(randomChampion)] += 1
            randomChampionFile = os.path.join(
                const.res_path, (randomChampion + ".png"))
            randomChampionImage = Image.open(randomChampionFile)

            x, y = self.getValidRandomPosition()

            rift.paste(randomChampionImage, (x, y), randomChampionImage)

            if random.randint(0, self.yuumiProba) == 0:
                x -= 1
                y -= 5
                if (i + redOrBlue) % 2 == 0:
                    rift.paste(self.yuumi_red, (x, y), self.yuumi_red)
                else:
                    rift.paste(self.yuumi_blue, (x, y), self.yuumi_blue)
                row += self.yuumiToString(x, y)
            else:
                if (i + redOrBlue) % 2 == 0:
                    rift.paste(self.redImage, (x, y), self.redImage)
                else:
                    rift.paste(self.blueImage, (x, y), self.blueImage)

            row += self.championToString(i, x, y)
        out = rift.convert("RGB")
        out_file = os.path.join(const.training_images_path, mapName)
        out.save(
            out_file,
            quality=90,
        )
        self.data_train.append(row)
        self.mapIndex += 1

    def getSensDeplacementXY(self, x, y):
        tmpX = x + self.championSize / 2
        tmpY = y + self.championSize / 2
        if tmpX < self.imageSize / 2 and tmpY < self.imageSize / 2:
            return 1, 1
        if tmpX < self.imageSize / 2 and tmpY >= self.imageSize / 2:
            return 1, -1
        if tmpX >= self.imageSize / 2 and tmpY < self.imageSize / 2:
            return -1, 1
        return -1, -1

    def getNewPosition(self, x, y, sensX, sensY, min, max):
        nbTry = 0
        while nbTry < 100:
            angle = random.uniform(0, 1) * (math.pi / 2)
            deplacement = random.randint(min, max)
            newX = math.floor(x + sensX * math.cos(angle) * deplacement)
            newY = math.floor(y + sensY * math.sin(angle) * deplacement)
            if self.isPositionValid(newX, newY):
                return newX, newY
            nbTry += 1
        print(str(self.mapIndex))
        return self.getValidRandomPosition()

    def generateMapSuperposition(self, redOrBlue):
        rift = Image.open(const.rift_file)
        mapName = "map" + str(self.mapIndex) + ".jpg"
        row = os.path.join(const.training_images_path, mapName)
        x, y = self.getValidRandomPosition()
        sensX, sensY = self.getSensDeplacementXY(x, y)
        for i in range(self.nbChampionsPerMap):
            if self.championIndex + i >= self.nbChampions:
                break

            randomChampion = self.getRandomChampion(i)
            self.listTest[self.championsList.index(randomChampion)] += 1
            randomChampionFile = os.path.join(
                const.res_path, (randomChampion + ".png"))
            randomChampionImage = Image.open(randomChampionFile)

            rift.paste(randomChampionImage, (x, y), randomChampionImage)

            if random.randint(0, self.yuumiProba) == 0:
                x -= 1
                y -= 5
                if (i + redOrBlue) % 2 == 0:
                    rift.paste(self.yuumi_red, (x, y), self.yuumi_red)
                else:
                    rift.paste(self.yuumi_blue, (x, y), self.yuumi_blue)
                row += self.yuumiToString(x, y)
            else:
                if (i + redOrBlue) % 2 == 0:
                    rift.paste(self.redImage, (x, y), self.redImage)
                else:
                    rift.paste(self.blueImage, (x, y), self.blueImage)

            row += self.championToString(i, x, y)

            x, y = self.getNewPosition(
                x, y, sensX, sensY, 5, self.championSize-5)

        out = rift.convert("RGB")
        out_file = os.path.join(const.training_images_path, mapName)
        out.save(
            out_file,
            quality=90,
        )
        self.data_train.append(row)
        self.mapIndex += 1

    def updateChampions(self):
        self.championIndex += self.nbChampionsPerMap
        if self.championIndex >= self.nbChampions:
            self.championIndex = 0
            random.shuffle(self.randomIndexList)

    def updateDataTrain(self):
        f = open(const.data_train_file, "w")
        f.write("\n".join(self.data_train))
        f.close()

    def generateMaps(self, nbMaps, superposition):
        while self.mapIndex < nbMaps:
            # redAndBlue
            self.generateMap(0)
            self.generateMap(1)
            if(superposition):
                self.generateMapSuperposition(0)
                self.generateMapSuperposition(1)
            self.updateChampions()
        self.updateDataTrain()
        print(self.listTest)


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
        default=64,
        help="Number of fake map generated. Default is " + str(64),
    )
    
    parser.add_argument('--no_superposition', dest='superposition', action='store_false')
    parser.set_defaults(superposition=True)

    FLAGS = parser.parse_args()
    print(FLAGS)
    factory = ImageGenerator()
    factory.generateMaps(FLAGS.number, FLAGS.superposition)
