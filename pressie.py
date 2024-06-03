import random

class Pressie:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.pressies = []
        self.x, self.y = -1, -1

    def addPressie(self, pos, gravity):
        #print(f"Adding pressie, TOTAL: {len(self.pressies)}")
        x = self.settings.pressieStartX + pos[0] + random.randint(0, 10)
        y = self.settings.pressieStartY + pos[1] + random.randint(0, 10)
        self.pressies.append([x, y, float(gravity), len(self.pressies)])

    def update(self, delta):
        self.deleteIndex = []
        for i in range(len(self.pressies)):
            self.pressies[i][0] -= (self.settings.res_scale / 4) * delta
            self.pressies[i][2] += self.settings.pressieGravity * delta
            self.pressies[i][1] += self.pressies[i][2] * delta
            if (self.pressies[i][1] > self.settings.screen_height):
                self.deleteIndex.append(i)
            #print(f"pressieX: {self.pressies[i][0]}")

        if (len(self.deleteIndex) > 0):
            for j in range(len(self.deleteIndex)):
                self.deletePressie(j)

    def deletePressie(self, index):
        self.pressies.pop(index)

    def howManyPressies(self):
        return len(self.pressies)

    def draw(self, img):
        for i in range(len(self.pressies)):
            self.screen.blit(img, (self.pressies[i][0], self.pressies[i][1]))

    # Based on center X point of pressie to 12px to left and right of chimneyX
    def checkCollision(self, x, y):
        for i in range(len(self.pressies)):         
            if (self.pressies[i][0] + (2 * self.settings.res_scale) > x - (12 * self.settings.res_scale) and \
                self.pressies[i][0] + (2 * self.settings.res_scale) < x + (12 * self.settings.res_scale)):
                if (self.pressies[i][1] > y and self.pressies[i][1] < y + (12 * self.settings.res_scale)):
                    self.x = self.pressies[i][0]
                    self.y = self.pressies[i][1]
                    return [int(i), (self.x, self.y)]
        return [-1, 0, 0]