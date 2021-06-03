csv_file = open("data_train_deepLeague4096.csv", "w")
txt_file = open("data_train_deepLeague4096.txt","r")
csv_file.write("image,xmin,xmax,ymin,ymax,label\n")

line = txt_file.readline()
while line :
    line = line.replace("\n","").split(" ")
    image = line.pop(0)
    for object in line :
        csv_file.write(image+","+object+"\n")
    line = txt_file.readline()

csv_file.close()