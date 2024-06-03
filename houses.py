import random

class Houses:
    def __init__(self, screen, settings, houseImages, houseHeight, houseWidth):
        self.screen = screen
        self.settings = settings
        self.images = houseImages
        self.houseWidth = (houseWidth / self.settings.res_scale) / self.settings.houseCols
        self.houseHeight = houseHeight
        self.setLevel()

    def setLevel(self):
        self.settings.houseQty = self.settings.houseQtyMax
        self.house = []
        startX = self.settings.screen_width
        startY = self.settings.screen_height - self.houseHeight
        previousHouseNumber = 0

        for i in range(self.settings.houseQty):
            enemyPlacement = False
            houseNumber = random.randint(0, self.settings.houseCols - 1)
            if (houseNumber == previousHouseNumber):
                houseNumber = random.randint(0, self.settings.houseCols - 1)
            previousHouseNumber = houseNumber
            isEnemyPlaced = random.randint(0, 100)
            if (isEnemyPlaced > 60):
                enemyPlacement = True
            # x start pos, image number
            nextX = random.randint(38 * self.settings.res_scale, 150 * self.settings.res_scale)
            startX += self.houseWidth + nextX
            # print(f"startX: {startX} - enemyPlacement: {enemyPlacement}")
            self.house.append([startX, startY + random.randint(0, 10), houseNumber, enemyPlacement])

    # Get X pos of houses with enemies on and return as array
    def getEnemyPositions(self):
        enemyPositions = []
        for i in range(len(self.house)):
            if (self.house[i][3] == True):
                enemyPositions.append(self.house[i][0] + (self.houseWidth * self.settings.res_scale))
        return enemyPositions

    def getChimneyPositions(self):
        chimneyPosition = -1
        for i in range(len(self.house)):
            if (self.house[i][0] > -(self.houseWidth * self.settings.res_scale)):
                chimneyPosition = self.house[i][0] + (self.houseWidth * self.settings.res_scale) / 2
                #print(f"getChimneyPositions: {chimneyPosition}")
                break
        return chimneyPosition

    def update(self):
        self.deleteIndex = []
        for i in range(len(self.house)):
            self.house[i][0] -= self.settings.backgroundSpeed * 3
            if (self.house[i][0] < -self.settings.screen_width):
                self.deleteIndex.append(i)

        if (len(self.deleteIndex) > 0):
            for j in range(len(self.deleteIndex)):
                self.house.pop(j)
                self.settings.houseQty -= 1

    def draw(self):
        for i in range(len(self.house)):
            if (self.house[i][0] > -500 and self.house[i][0] < self.settings.screen_width):
                self.screen.blit(self.images[self.house[i][2]], (self.house[i][0], self.house[i][1]))
