#!/usr/bin/python3
from PIL import Image
import json
import random
import math

def isPosValid(x,y,a,b,c,d):
    digit = (x<0) or (x>255) or (y<0) or (y>255) or (x<a and y<b) or (x<b and y<a) or (x>c and y>d) or (x>d and y>c) 
    return not digit

#PARAMS
nbGeneratedMap = 10
nbChampionsPerMap = 10
trainingImagePath = '/content/TrainYourOwnYOLO/Data/Source_Images_Training_Images/vott-csv-export/'
nbChampions = 0
text = []
red = Image.open('./rift/red.png')
blue = Image.open('./rift/blue.png')
mapIndex = 0
_list = []
_listBis = []

with open('dataDragon/10.23.1/data/fr_FR/champion.json', 'r') as json_file:
    data = json.load(json_file)
    data = data['data']
    
    data_classes = []
    for p in data:
        print(p)
        _list.append(p)
        _listBis.append(p)
        data_classes.append(p)   
    
    print("Loading champions list done")
    nbChampions = len(_list)
    print("Nombre de champions : "+str(nbChampions))
    print(_list)

    f = open("Training_Gen/data_classes.txt", "w")
    f.write('\n'.join(data_classes))
    f.close()

for i in range(10):
    while (nbChampions >= nbChampionsPerMap):
        row = "map"+str(mapIndex)+".jpg"
        rift = Image.open('./rift/rift.png')
        x = random.randint(37,192)
        y = random.randint(37,192)
        for numChamp in range(nbChampionsPerMap):
            randomChampIndex = random.randint(0,nbChampions-1)
            randomChampImage = Image.open('res/'+_listBis[randomChampIndex]+'.png')
            while True:
                tmpX = x + math.floor(random.uniform(-1,1)*26)
                tmpY = y + math.floor(random.uniform(-1,1)*26)
                centerX = tmpX + 13
                centerY = tmpY + 13
                if isPosValid(centerX,centerY,10,173,245,80):
                    break
            x = tmpX
            y = tmpY
            rift.paste(randomChampImage, (x,  y), randomChampImage)
            if (numChamp%2 == 0):
                    rift.paste(red,(x,y),red)
            else:
                    rift.paste(blue,(x,y),blue)
            row+=' '+str(x)+','+str(y)+','+str(x+26)+','+str(y+26)+","+str(_list.index(_listBis[randomChampIndex]))
            _listBis[randomChampIndex], _listBis[nbChampions-1] = _listBis[nbChampions-1], _listBis[randomChampIndex]
            nbChampions = nbChampions-1
        out = rift.convert('RGB')
        out.save("./generatedImages/map"+str(mapIndex)+".jpg", quality=90)
        text.append(row)
        mapIndex = mapIndex+1
    nbChampions = len(_list)

for i in range(10):
    while (nbChampions >= nbChampionsPerMap):
        row = "map"+str(mapIndex)+".jpg"
        rift = Image.open('./rift/rift.png')
        for numChamp in range(nbChampionsPerMap):
            randomChampIndex = random.randint(0,nbChampions-1)
            randomChampImage = Image.open('res/'+_listBis[randomChampIndex]+'.png')
            
            while True:
                x = random.randint(-13,242)
                y = random.randint(-13,242)
                centerX = x + 13
                centerY = y + 13
                if isPosValid(centerX,centerY,10,173,245,80):
                    break
            rift.paste(randomChampImage, (x,  y), randomChampImage)
            if (numChamp%2 == 0):
                rift.paste(red,(x,y),red)
            else:
                rift.paste(blue,(x,y),blue)

            row+=' '+str(x)+','+str(y)+','+str(x+26)+','+str(y+26)+","+str(_list.index(_listBis[randomChampIndex]))
            numChamp = numChamp+1
            _listBis[randomChampIndex], _listBis[nbChampions-1] = _listBis[nbChampions-1], _listBis[randomChampIndex]
            nbChampions = nbChampions-1
            
        out = rift.convert('RGB')
        out.save("./generatedImages/map"+str(mapIndex)+".jpg", quality=90)
        text.append(row)
        mapIndex = mapIndex+1
    nbChampions = len(_list)



f = open("./data_train.txt", "w")
f.write("\n".join(text))
f.close()
    
