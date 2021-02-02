class Champion:
    def __init__(self, data):
        [xmin, ymin, xmax, ymax, idChamp] = data
        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)

        self.idChampion = int(idChamp)

    def getCenter(self):
        return ((self.xmin + self.xmax) / 2, (self.ymin + self.ymax) / 2)

    def toString(self):
        return (
            str(self.idChampion)
            + "("
            + str(self.xmin)
            + ","
            + str(self.ymin)
            + ") "
            + str(self.getCenter())
        )
