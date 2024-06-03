# Class to show stars when player gets pressie into chimney
class Sparkles:
    def __init__(self, settings, pressiePos, log):
        self.settings = settings
        self.log = log
        self.startX = pressiePos[0]
        self.startY = pressiePos[1]
        self.boost = -(2.5 * self.settings.res_scale)
        self.left, self.right = 5, 5
        self.stars = []
        self.stars.append([self.startX, self.startY, -5, -2, self.boost / 2])
        self.stars.append([self.startX, self.startY, -2, -2, self.boost])
        self.stars.append([self.startX, self.startY, 2, -2, self.boost])
        self.stars.append([self.startX, self.startY, 5, -2, self.boost / 2])
        if (self.settings.log_setting == 3):
            self.log.write(f"Star sparkles created at position {self.startX, self.startY}")

    def update(self, delta):
        if (len(self.stars) > 0):
            for i in range(len(self.stars)):
                # Reduce boost
                self.stars[i][4] += 1
                # Add the boost to the upward movement to fake gravity
                self.stars[i][1] += self.stars[i][4] * delta
                # Adjust X pos
                self.stars[i][0] += self.stars[i][2] * delta
                # Adjust Y pos
                self.stars[i][1] += self.stars[i][3] * delta
                # Remove if out of screen
                if (self.stars[i][1] > self.settings.screen_height):
                    self.stars.pop(i)
                    break
                if (self.stars[i][0] < 0):
                    self.stars.pop(i)
                    break
            return True
        return False

    def draw(self, screen, img):
        for i in range(len(self.stars)):
            screen.blit(img, (self.stars[i][0], self.stars[i][1]))