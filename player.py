

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getPos(self):
        return self.x, self.y

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def updatePosition(self, gravity):
        self.y += gravity

    def updateBoost(self, boost):
        if (self.y > 0):
            self.y -= boost