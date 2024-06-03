# Explosion class

class Explosion:
    def __init__(self, pos, frameStart):
        self.x = pos[0]
        self.y = pos[1]
        self.frame = frameStart
        
    def update(self, frame):
        if (self.x > -100):
            self.x -= 3
            self.frame = frame

    def getPos(self):
        return [self.x, self.y]
    
    def getFrame(self):
        return self.frame
