#!/usr/bin/python3
from PIL import Image
import json
import random
_list = []
_listBis = []

def isPosValid(x,y,a,b,c,d):
    digit = (x<a and y<b) or (x<b and y<a) or (x>c and y>d) or (x>d and y>c)
    return not digit

#PARAMS
nbGeneratedMap = 100
nbChampionsPerMap = 10
nbChampions = 0

with open('./dragontail-10.23.1/10.23.1/data/fr_FR/champion.json', 'r') as json_file:
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

    f = open("./Data/Model_Weights/data_classes.txt", "w")
    f.write('\n'.join(data_classes))
    f.close()

text = []

red = Image.open('./Data/Source_Images/Init_Images/red.png')
blue = Image.open('./Data/Source_Images/Init_Images/blue.png')
mapIndex = 0

for i in range(int(nbGeneratedMap/len(_list)/10)):
    while (nbChampions >= nbChampionsPerMap):
        row = "map"+str(mapIndex)+".jpg"
        rift = Image.open('./Data/Source_Images/Init_Images/rift.png')
        for numChamp in range(nbChampionsPerMap):
            randomChampIndex = random.randint(0,nbChampions-1)
            randomChampImage = Image.open('res/'+_listBis[randomChampIndex]+'.png')
            while True:
                x = random.randint(-13,242)
                y = random.randint(-13,242)
                if isPosValid(x,y,10,173,245,80):
                    rift.paste(randomChampImage, (x,  y), randomChampImage)
                    if (numChamp%2 == 0):
                        rift.paste(red,(x,y),red)
                    else:
                        rift.paste(blue,(x,y),blue)
                    row+=' '+str(x)+','+str(y)+','+str(x+26)+','+str(y+26)+","+str(_list.index(_listBis[randomChampIndex]))
                    numChamp = numChamp+1
                    break
            _listBis[randomChampIndex], _listBis[nbChampions-1] = _listBis[nbChampions-1], _listBis[randomChampIndex]
            nbChampions = nbChampions-1
        out = rift.convert('RGB')
        out.save("./Data/Source_Images/Training_Images/map"+str(mapIndex)+".jpg", quality=90)
        text.append(row)
        mapIndex = mapIndex+1
    nbChampions = len(_list)

f = open("./Data/Source_Images/Training_Images/data_train.txt", "w")
f.write("\n".join(text))
f.close()