# Display text on screen
from letters import Letter

class Text:
    def __init__(self, letter_spacing, scale):
        self.word_list = []
        self.letter_spacing = letter_spacing
        self.scale = scale

    # Add all the words for the game
    def addWord(self, text = "text", pos = (0, 0), gameState = 0):
        self.word_list.append([text, pos, gameState])

    def displayTextAt(self, alphabet, x, y, text):
        for letter in str(text):
            # Space char
            if (letter == " "):
                x += self.letter_spacing * self.scale
            else:
                for idx, img in enumerate(alphabet.letters):                        
                    # Everything else
                    if (img.name == letter):
                        alphabet.letters[idx].draw((x, y), self.scale)
                        x += self.letter_spacing * self.scale