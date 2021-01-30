class Champion:

    def __init__(self,id, confidence, xmin, ymin, xmax, ymax):
        self.data = []
        self.id = id
        self.confidence = confidence
        self.center = self.getCenter(xmin, ymin, xmax, ymax)

    def getCenter(self, xmin, ymin, xmax, ymax):
        return ( (xmin+xmax)/2, (ymin+ymax)/2 )
