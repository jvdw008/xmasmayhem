import pygame
from spritesheet import SpriteSheet

class Sprites:
    def __init__(self, xmas_mayhem_game, file, scale, rows, cols, settings, log):
        # Load the image
        self.sheet = SpriteSheet(file, scale, settings, log)
        self.spriteTiles = self.sheet.load_grid_images(rows, cols)

    def getSprite(self):
        return self.spriteTiles
    
    # Get pixel height from first image in image array of spritesheet
    def get_height(self):
        return self.sheet.get_height(self.spriteTiles[0])

    # Get pixel width from first image in image array of spritesheet
    def get_width(self):
        return self.sheet.get_width(self.spriteTiles[0])