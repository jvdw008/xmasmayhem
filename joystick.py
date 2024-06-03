# Joystick code
import pygame

class Joy:
    def __init__(self):
        self.joystickName = ""
        self.joyCount = pygame.joystick.get_count()
        if (self.joyCount > 0):
            self.joy = pygame.joystick.Joystick(0)
            self.joy.init()
            self.joystick = self.joy
            self.joystickName = self.joy.get_name()

    def deviceAdded(self, eventId):
        self.joy = pygame.joystick.Joystick(eventId)
        self.joystick = self.joy
        self.joystickName = self.joy.get_name()

    def deviceRemoved(self):
        if (self.joystick):
            del self.joystick

    def getCount(self):
        return self.joyCount

    def getName(self):
        return self.joystickName

    def displayJoysticks(self, joy):
        print(joy)

    def displayHats(self):
        hats = self.joy.get_numhats()
        if (hats > 0):
            for i in range(hats):
                hat = self.joy.get_hat(i)
                print(f"Hat {i} value: {str(hat)}")

    def displayButtons(self):
        pass

    def rumble(self, length=100):
        self.joy.rumble(1, 1, length)