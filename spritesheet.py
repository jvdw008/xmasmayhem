import os, pygame
from os.path import dirname

class SpriteSheet:
    # Load the spritesheet
    def __init__(self, file, scale, settings, log):
        self.settings = settings
        self.log = log
        
        try:
            if (self.settings.log_setting == 3):
                self.log.write(f"Attempting to load spritesheet image: {file}")
            self.sheet = pygame.image.load(os.path.join(os.getcwd(), "data", file)).convert_alpha()
            self.rect = self.sheet.get_rect()
            self.x_scale = self.rect.width * scale
            self.y_scale = self.rect.height * scale
            self.sheet = pygame.transform.scale(self.sheet, (self.x_scale, self.y_scale))

        except IOError:
            if (self.settings.log_setting == 3):
                self.log.write(f"Unable to load spritesheet image: {file}")
            return

    # Loads image from x, y, x + offset, y + offset.
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image = pygame.transform.scale(image, (self.x_scale, self.y_scale))
        image.blit(self.sheet, (0, 0), rect)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects):
        return [self.image_at(rect) for rect in rects]

    # Load a whole strip of images, and return them as a list
    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
        return self.images_at(tups, colorkey)

    # Load grid of images and return as list
    def load_grid_images(self, num_rows, num_cols):
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        x_sprite_size = sheet_width / num_cols
        y_sprite_size = sheet_height / num_rows
        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                x = col_num * x_sprite_size
                y = row_num * y_sprite_size
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects)
        return grid_images

    def get_height(self, image):
        return image.get_rect().height

    def get_width(self, image):
        return image.get_rect().width