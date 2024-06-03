# Class used to load Letters class objects 
from spritesheet import SpriteSheet
from letters import Letter

class Alphabet:
    def __init__(self, xmas_mayhem_game, settings, fontFile, log):
        self.xmas_mayhem_game = xmas_mayhem_game
        self.log = log
        self.letters = []
        self.letter_names = []
        self.settings = settings
        self.fontFile = self.settings.font_file
        if (len(fontFile) > 0):
            self.fontFile = fontFile
        # Load font image
        letters_ss = SpriteSheet(self.fontFile, self.settings.res_scale, self.settings, self.log)
        letter_images = letters_ss.load_grid_images(1, 44)
        self.letter_names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", \
        "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ":", ",", "@", "!", "?", \
        "<", ">", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        letter_num = 0

        for image in letter_images:
            letterObj = Letter(self.xmas_mayhem_game)
            letterObj.image = image
            letterObj.name = self.letter_names[letter_num]
            self.letters.append(letterObj)
            letter_num += 1

        """
        # To grab an individual image, use below:
        # x, y, w, h
        # Create "a"
        a_rect = (0, 0, 8, 8)
        a_rect_image = letters_ss.image_at(a_rect)

        a_letter = Letter(self.xmas_mayhem_game, a_rect_image)
        a_name = "a"

        self.letters.append(a_letter)
        """

