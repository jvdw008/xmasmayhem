import os, pygame, sys, random
from pygame.locals import *
from joystick import Joy
from log import Log
from settings import Settings
from config import Config
from alphabet import Alphabet
from text import Text
from background import Background
from bars import Bars
from houses import Houses
from weather import Weather
from animation import Animation
from sprites import Sprites
from player import Player
from bullet import Bullet
from pressie import Pressie
from enemy import Enemy
from sparkels import Sparkles
from explosions import Explosion
from magicDust import MagicDust
from drops import Drops

clock = pygame.time.Clock()
# =======================================================================
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_reserved(1)    # For music
        pygame.joystick.init()
        self.joystick = Joy()   # Set up joystick(s)
        self.keys = pygame.key.get_pressed()
        pygame.key.set_repeat()

        # Set up settings
        self.settings = Settings()
        self.gameState = self.settings.state_menu

        # Load config from text file to overwrite settings above where needed (for controls)
        self.config = Config(self.settings)
        
        # Set up logging - level, size
        self.logger = Log(self.settings)
        
        # Create game screen/window
        if (self.settings.is_fullscreen):
            flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE
        else:
            flags = 0
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), flags)
        
        pygame.display.set_caption("Xmas Mayhem " + str(self.settings.version))
        self.fullPath = os.path.realpath("./")
        
        # Load and instantiate the alphabet spritesheet
        self.alphabet = Alphabet(self, self.settings, "", self.logger)
        self.alphabetWhite = Alphabet(self, self.settings, self.settings.font_white_file, self.logger)
        
        # Set up the in-game words
        self.text = Text(self.settings.text_spacing, self.settings.font_scale)

        # Load Backgrounds
        self.bg = Background(self, self.settings, self.logger)

        # Load level graphics - file, scale, rows, cols, log
        self.houseSprites = Sprites(self, self.settings.house01File, self.settings.res_scale, 1, self.settings.houseCols, self.settings, self.logger)
        self.houses = Houses(self.screen, self.settings, self.houseSprites.getSprite(), self.houseSprites.get_height(), self.houseSprites.get_width())

        # Load Weather system - TODO: implement snow
        self.weather = Weather(self.settings, self.screen, self.logger)

        # Set up game sprites - file, scale, rows, cols, log
        self.playerSprite = Sprites(self, self.settings.playerFile, self.settings.res_scale, 1, 21, self.settings, self.logger)
        self.playerSpriteFlash = Sprites(self, self.settings.playerFlashFile, self.settings.res_scale, 1, 21, self.settings, self.logger)
        # Then add it to animation class - sprite image list, sprite params, loop, log
        self.playerAnimation = Animation(self.settings, self.screen, self.playerSprite.getSprite(), self.settings.playerSpriteParams, True, self.logger)
        self.playerAnimationFlash = Animation(self.settings, self.screen, self.playerSpriteFlash.getSprite(), self.settings.playerSpriteParams, True, self.logger)
        self.player = Player(self.settings.playerX, self.settings.playerY)

        # Enemies:
        self.enemiesArray = self.houses.getEnemyPositions()
        # Snowman
        self.snowmanSprite = Sprites(self, self.settings.snowman_file, self.settings.res_scale, 1, 10, self.settings, self.logger)
        # Snowman animation
        self.snowmanAnimation = Animation(self.settings, self.screen, self.snowmanSprite.getSprite(), self.settings.snowmanSpriteParams, True, self.logger)
        # Grinch
        self.grinchSprite = Sprites(self, self.settings.grinch_file, self.settings.res_scale, 1, 10, self.settings, self.logger)
        # Grinch animation
        self.grinchAnimation = Animation(self.settings, self.screen, self.grinchSprite.getSprite(), self.settings.grinchSpriteParams, True, self.logger)

        self.enemies = Enemy(self.settings, self.logger)
        for i in range(len(self.enemiesArray)):
            self.enemies.addEnemy(self.enemiesArray[i], random.randint(0, 1))

        # Spritesheet small images
        self.smallSpritesImages = Sprites(self, self.settings.small_sprites_file, self.settings.res_scale, 1, 10, self.settings, self.logger)
        self.smallSprites = self.smallSpritesImages.getSprite()

        # Game bar backgrond
        self.barBg = Bars(self, self.settings, self.logger)

        # Player bullet system
        self.playerBullets = Bullet(self.screen, self.settings, self.logger)

        # Pressie system
        self.pressies = Pressie(self.screen, self.settings)

        # Sparkels
        self.sparkles = False
        self.sparklesExist = False

        # Magic dust under santa's sleigh
        self.dust = MagicDust(self.settings, self.screen, self.player.getPos(), self.playerSprite.get_height() / 2, int(self.playerSprite.get_width() / self.settings.playerSpriteParams[1]))

        # Explosions
        self.explosionSprite = Sprites(self, self.settings.explosion_file, self.settings.res_scale, 1, 10, self.settings, self.logger)
        self.explosionAnimation = Animation(self.settings, self.screen, self.explosionSprite.getSprite(), self.settings.explosionSpriteParams, False, self.logger)
        self.explosionsArray = []

        # Drops
        self.dropsArray = []

        # Hide OS mouse cursor
        pygame.mouse.set_visible(False)

    # Allow fullscreen mode - still needs work to revert to non-fullscreen
    '''
    def toggle_fullscreen(self):
        self.screen = pygame.display.get_surface()
        bits = self.screen.get_bitsize()
        
        if (not self.settings.is_fullscreen):
            
            flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.HWSURFACE
            self.screen = pygame.display.set_mode((width, height), flags, bits)
            self.settings.is_fullscreen = False
        else:
            flags = pygame.RESIZABLE
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), flags)
            self.settings.is_fullscreen = True

        pygame.key.set_mods(0)  # HACK: work-a-round for a SDL bug??
        return self.screen
    '''
    #######################################################################
    # Reset map/level/score etc for new game
    #######################################################################
    def resetStats(self):
        if (self.settings.score > self.settings.highscore):
            self.settings.highscore = self.settings.score
        self.settings.score = 0
        self.settings.gifts_delivered            = 0
        self.settings.bullets_shot               = 0
        self.settings.enemies_killed             = 0
        self.settings.distance_travelled         = 0
        self.settings.ammoQty = 100
        self.settings.fuelQty = 100
        self.settings.energyQty = 100
        self.settings.gravity = self.settings.defaultGravity
        self.sparkles = False
        self.sparklesExist = False
        self.houses.setLevel()
        self.player.setPos((self.settings.playerX, self.settings.playerY))
        self.playerBullets = Bullet(self.screen, self.settings, self.logger)
        self.enemiesArray = self.houses.getEnemyPositions()
        self.enemies = Enemy(self.settings, self.logger)
        for i in range(len(self.enemiesArray)):
            self.enemies.addEnemy(self.enemiesArray[i], random.randint(0, 1))
        self.explosionsArray = []
        self.dropsArray = []

    #######################################################################
    # Update states
    #######################################################################
    def update(self):
        # Get/set delta time
        t = pygame.time.get_ticks()
        self.settings.delta = (t - self.settings.getTicksLastFrame) / 10
        self.settings.getTicksLastFrame = t

        if self.gameState == self.settings.state_game:
            # Measure distance travelled
            self.settings.distance_travelled += 1

            self.bg.update()
            self.houses.update()

            # Is level complete?
            if (self.settings.houseQty <= 0):
                self.settings.fuelQty = 0
                self.gameState = self.settings.state_gameover
                pygame.mixer.Sound.play(self.settings.snd_gameOver)

            self.playerBullets.update(self.settings.delta)
            if (self.settings.bulletTimer != self.settings.bulletTimerMax):
                self.settings.bulletTimer -= 1
            if (self.settings.bulletTimer <= 0):
                self.settings.bulletTimer = self.settings.bulletTimerMax

            self.enemies.update(self.player.getPos(), self.settings.fuelQty)
            self.enemies.updateBullets()
            self.enemyPosArray = self.enemies.getPos()

            grinchUpdated, snowmanUpdated = False, False
            for i in range(len(self.enemyPosArray)):
                # Check bullet collision from playerr bullets to enemy
                if (self.playerBullets.checkCollision(self.enemyPosArray[i][0], self.enemyPosArray[i][1])):
                    self.explosionsArray.append(Explosion((self.enemyPosArray[i][0], self.enemyPosArray[i][1]), 0))
                    pygame.mixer.Sound.play(self.settings.snd_enemyHit)

                    # Check if enemy dropped something
                    self.enemyDrop = random.randint(0, 100)
                    if (self.enemyDrop > 50):
                        self.enemyDropImage = random.randint(0, 1000)
                        if (self.enemyDropImage < 300):
                            self.enemyDropImage = 0
                        elif (self.enemyDropImage >=300 and self.enemyDropImage < 800):
                            self.enemyDropImage = 3
                        else:
                            self.enemyDropImage = 9

                        self.enemyDrop = self.dropsArray.append(Drops(self.screen, (self.enemyPosArray[i][0], self.enemyPosArray[i][1]), self.smallSprites[self.enemyDropImage], self.enemyDropImage, self.settings, self.logger))

                    self.enemies.deleteEnemy(i)
                    self.settings.score += 50
                    self.settings.enemies_killed += 1

                # Update relevant animation, if needed
                if (self.enemyPosArray[i][0] > self.settings.enemyLeftX):   # Is enemy far enough to the right?
                    if (self.enemyPosArray[i][2] == 0):                     # Is this a snowman?
                        if (snowmanUpdated == False):
                            self.snowmanAnimation.update()                  # Update snowman animation
                            snowmanUpdated = True
                    else:
                        if (grinchUpdated == False):
                            self.grinchAnimation.update()                   # Else update grinch animation
                            grinchUpdated = True

            # Update Enemy Drops
            self.deleteDropsArray = []
            for i in range(len(self.dropsArray)):
                imgIndex = self.dropsArray[i].update()
                dropX = int(self.dropsArray[i].getPos()[0])
                dropY = int(self.dropsArray[i].getPos()[1])
                # Drop it if out of screen
                if (dropX < -10 or dropY < -10):
                    self.deleteDropsArray.append(i)

                # Check if player collected it
                playerX1 = self.player.getPos()[0]
                playerX2 = self.player.getPos()[0] + self.playerSprite.get_width() / self.settings.playerSpriteParams[1] + 5
                playerY1 = self.player.getPos()[1]
                playerY2 = self.player.getPos()[1] + self.playerSprite.get_height() * 0.5
                if (playerX1 < dropX and playerX2 > dropX):
                    if (playerY1 < dropY and playerY2 > dropY):
                        self.deleteDropsArray.append(i)
                        self.settings.score += 50
                        pygame.mixer.Sound.play(self.settings.snd_collect)
                        # Check what to top up
                        # Ammo
                        if (imgIndex == 0):
                            self.settings.ammoQty += 10
                            if (self.settings.ammoQty > 100):
                                self.settings.ammoQty = 100

                        # Energy
                        elif (imgIndex == 9):
                            self.settings.energyQty += 10
                            if (self.settings.energyQty > 100):
                                self.settings.energyQty = 100

                        # Fuel
                        elif (imgIndex == 3):
                            self.settings.fuelQty += 10
                            if (self.settings.fuelQty > 100):
                                self.settings.fuelQty = 100

            # Delete straggler drops
            if (len(self.deleteDropsArray)):
                for i in range(len(self.deleteDropsArray)):
                    for j in range(len(self.dropsArray)):
                        if (j == i):
                            self.dropsArray.pop(j)


            # Check pressies hit chimneys
            self.chimneyPos = self.houses.getChimneyPositions()
            hit = self.pressies.checkCollision(self.chimneyPos, self.settings.screen_height - self.houses.houseHeight)
            if (hit[0] != -1):
                self.settings.score += 100
                self.pressies.deletePressie(hit[0])
                pygame.mixer.Sound.play(self.settings.snd_pressie)
                self.settings.gifts_delivered += 1

                # Show sparkles at pressie Pos
                self.sparkles = Sparkles(self.settings, hit[1], self.logger)
                self.sparklesExist = True

            # Sparkels
            if (self.sparklesExist):
                self.sparklesComplete = self.sparkles.update(self.settings.delta)
                if (self.sparklesComplete == False):
                    del self.sparkles
                    self.sparklesExist = False
                    self.sparklesComplete = True

            # Magic dust
            self.dust.update(self.player.getPos())

            #############################################
            # Check enemy bullet collision hitting player
            if (self.settings.playerHit == False):   # Make sure it only gets hit at the start
                if (self.enemies.checkBulletCollisions(self.player.getPos())):
                    self.settings.playerHit = True
                    self.settings.energyQty -= 10
                    pygame.mixer.Sound.play(self.settings.snd_playerHit)

                    # Rumble joypad for 1 second
                    if (self.joystick.getCount() > 0):
                        self.joystick.rumble()

                    # Game-over
                    if (self.settings.energyQty <= 0):
                        self.settings.fuelQty = 0
                        self.gameState = self.settings.state_gameover
                        pygame.mixer.Sound.play(self.settings.snd_gameOver)

            # Update invulnerability for player
            if (self.settings.playerHit):
                self.settings.invulnerabilityTimer -= 1
                if (self.settings.invulnerabilityTimer <= 0):
                    self.settings.flashCounter -= 1
                    # Flashing over, player now vulnerable again
                    if (self.settings.flashCounter <= 0):
                        self.settings.flashCounter = self.settings.flashCounterMax
                        self.settings.playerHit = False
                    self.settings.invulnerabilityTimer = self.settings.invulnerabilityTimerMax

            # Explosions
            self.deleteExplosions = []
            for i in range(len(self.explosionsArray)):
                # Update X pos
                self.explosionsArray[i].update(self.explosionAnimation.getFrame())
                # Check if animation is done
                self.explosionAnimation.update()
                if (self.explosionAnimation.getFrame() == self.settings.explosionSpriteParams[1]):
                    self.explosionAnimation.resetFrame()
                    self.deleteExplosions.append(i)

            for i in range(len(self.explosionsArray)):
                for j in range(len(self.deleteExplosions)):
                    if (self.deleteExplosions[j] == i):
                        self.explosionsArray.pop(i)

            self.weather.update(self.settings.delta)

            # Player updates
            if (self.settings.playerBoostState):
                if (self.settings.playerBoost >= 0):
                    self.settings.playerBoost -= 1
                    self.player.updateBoost(self.settings.playerBoost)
                else:
                    # Reset
                    self.settings.playerBoost = self.settings.playerDefaultBoost
                    self.settings.playerBoostState = False
                    self.settings.gravity = self.settings.defaultGravity
            else:
                self.settings.gravity += self.settings.gravityExpo
                self.player.updatePosition(self.settings.gravity)

            self.playerAnimationFlash.update()
            self.playerAnimation.update()

            # Has player crashed?
            if (self.player.getPos()[1] > self.settings.screen_height):
                self.gameState = self.settings.state_gameover
                pygame.mixer.Sound.play(self.settings.snd_gameOver)
                if (self.joystick.getCount() > 0):
                        self.joystick.rumble(200)

            # Pressie updates
            self.pressies.update(self.settings.delta)

        elif self.gameState == self.settings.state_menu:
            self.bg.showSplash()
        return

    #######################################################################
    # Render surfaces and objects
    #######################################################################
    def render(self):        
        # Draw level and sprites
        if self.gameState == self.settings.state_game:
            self.bg.draw()
            self.houses.draw()
            #pygame.draw.rect(self.screen, (230, 0, 0), pygame.Rect(self.houseX, self.settings.screen_height - self.houses.houseHeight, self.houseX + (self.houses.houseWidth / 2), self.settings.screen_height))
            for i in range(len(self.enemyPosArray)):
                if (self.enemyPosArray[i][2] == 0):
                    self.snowmanAnimation.draw((self.enemyPosArray[i][0], self.enemyPosArray[i][1]))
                else:
                    self.grinchAnimation.draw((self.enemyPosArray[i][0], self.enemyPosArray[i][1]))

            # Dust
            self.dust.draw()

            # Player
            if (self.settings.playerHit):
                if (self.settings.flashCounter % 2 == 0):
                    self.playerAnimationFlash.draw(self.player.getPos())
                else:
                    self.playerAnimation.draw(self.player.getPos())
            else:
                self.playerAnimation.draw(self.player.getPos())

            # Snow
            self.weather.draw()

            # Bullets
            self.playerBullets.draw(self.smallSprites[self.settings.BULLET])

            # Enemy bullets
            self.enemies.drawBullet(self.screen, self.smallSprites)

            # Enemy drops
            for i in range(len(self.dropsArray)):
                self.dropsArray[i].draw()

            # Pressies
            self.pressies.draw(self.smallSprites[self.settings.PRESSIE])

            # Sparkels
            if (self.sparklesExist):
                self.sparkles.draw(self.screen, self.smallSprites[self.settings.STAR])

            # Explosions
            for i in range(len(self.explosionsArray)):
                explosionFrame = self.explosionAnimation.getFrame()
                if (self.explosionsArray[i].getFrame() < self.settings.explosionSpriteParams[1]):
                    self.explosionAnimation.draw((self.explosionsArray[i].getPos()))

            # Draw Rects for ammo, energy and fuel
            # Bg first
            self.barBg.draw()

            # Ammo
            if (self.settings.ammoQty >= 80):
                ammoBarColour = self.settings.green
            elif (self.settings.ammoQty > 40 and self.settings.ammoQty < 80):
                ammoBarColour = self.settings.yellow
            else:
                ammoBarColour = self.settings.red

            ammoScale = self.settings.ammoQty / 100
            pygame.draw.rect(self.screen, ammoBarColour, pygame.Rect(51 * self.settings.res_scale, 7 * self.settings.res_scale, 25 * self.settings.res_scale * ammoScale, 5 * self.settings.res_scale))

            # Energy
            if (self.settings.energyQty >= 80):
                energyBarColour = self.settings.green
            elif (self.settings.energyQty > 40 and self.settings.energyQty < 80):
                energyBarColour = self.settings.yellow
            else:
                energyBarColour = self.settings.red
            energyScale = self.settings.energyQty / 100
            pygame.draw.rect(self.screen, energyBarColour, pygame.Rect(131 * self.settings.res_scale, 7 * self.settings.res_scale, 25 * self.settings.res_scale * energyScale, 5 * self.settings.res_scale))

            # Fuel
            if (self.settings.fuelQty >= 80):
                fuelBarColour = self.settings.green
            elif (self.settings.fuelQty > 40 and self.settings.fuelQty < 80):
                fuelBarColour = self.settings.yellow
            else:
                fuelBarColour = self.settings.red
            fuelScale = self.settings.fuelQty / 100
            pygame.draw.rect(self.screen, fuelBarColour, pygame.Rect(207 * self.settings.res_scale, 7 * self.settings.res_scale, 25 * self.settings.res_scale * fuelScale, 5 * self.settings.res_scale))

            # Score - graphics, x, y, text
            self.text.displayTextAt(self.alphabetWhite, 270 * self.settings.res_scale, 10, self.settings.score)
            # Ammo
            self.screen.blit(self.smallSprites[self.settings.AMMO], (10 * self.settings.res_scale, 10))
            self.text.displayTextAt(self.alphabetWhite, 30 * self.settings.res_scale, 7 * self.settings.res_scale, self.settings.ammoQty)
            # Energy
            self.screen.blit(self.smallSprites[self.settings.ENERGY], (90 * self.settings.res_scale, 10))
            self.text.displayTextAt(self.alphabetWhite, 110 * self.settings.res_scale, 7 * self.settings.res_scale, self.settings.energyQty)
            # Fuel
            self.screen.blit(self.smallSprites[self.settings.FUEL], (170 * self.settings.res_scale, 10))
            self.text.displayTextAt(self.alphabetWhite, 190 * self.settings.res_scale, 7 * self.settings.res_scale, self.settings.fuelQty)

        elif self.gameState == self.settings.state_menu:
            
            # Display correct keyboard/joypad named controls based on config/settings
            self.text.displayTextAt(self.alphabet, 90 * self.settings.res_scale, 6 * self.settings.res_scale, \
                    "copyright by blackjet in 2022")
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 40 * self.settings.res_scale, "to start game, press <" + pygame.key.name(self.settings.key_boost) + ">")
            if (self.joystick.getCount() > 0):
                self.text.displayTextAt(self.alphabet, 110 * self.settings.res_scale, 46 * self.settings.res_scale, " or joypad <" + self.settings.joypad_boost_name + ">")
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 58 * self.settings.res_scale, \
                    "- in-game controls -")

            if (self.joystick.getCount() > 0):
                self.text.displayTextAt(self.alphabetWhite, 50 * self.settings.res_scale, 170 * self.settings.res_scale, "joypad detected: " + self.joystick.getName().lower())
            
            self.text.displayTextAt(self.alphabetWhite, 40 * self.settings.res_scale, 70 * self.settings.res_scale, "shoot:")
            self.text.displayTextAt(self.alphabetWhite, 40 * self.settings.res_scale, 76 * self.settings.res_scale, "boost:")
            self.text.displayTextAt(self.alphabetWhite, 5 * self.settings.res_scale, 82 * self.settings.res_scale, "drop pressie:")
            self.text.displayTextAt(self.alphabetWhite, 45 * self.settings.res_scale, 88 * self.settings.res_scale, "menu:")
            self.text.displayTextAt(self.alphabetWhite, 40 * self.settings.res_scale, 94 * self.settings.res_scale, "pause:")
            self.text.displayTextAt(self.alphabetWhite, 45 * self.settings.res_scale, 100 * self.settings.res_scale, "quit:")
            # Keyboard
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 70 * self.settings.res_scale, pygame.key.name(self.settings.key_fire) + " key")
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 76 * self.settings.res_scale, pygame.key.name(self.settings.key_boost) + " key")
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 82 * self.settings.res_scale, pygame.key.name(self.settings.key_drop) + " key")
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 88 * self.settings.res_scale, pygame.key.name(self.settings.key_menu) + " key")
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 94 * self.settings.res_scale, pygame.key.name(self.settings.key_pause) + " key")
            self.text.displayTextAt(self.alphabetWhite, 72 * self.settings.res_scale, 100 * self.settings.res_scale, pygame.key.name(self.settings.key_quit) + " key")
            # Joypad
            if (self.joystick.getCount() > 0):
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 70 * self.settings.res_scale, "or joypad <" + self.settings.joypad_fire_name + ">")
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 76 * self.settings.res_scale, "or joypad <" + self.settings.joypad_boost_name + ">")
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 82 * self.settings.res_scale, "or joypad <" + self.settings.joypad_pressie_name + ">")
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 88 * self.settings.res_scale, "or joypad <" + self.settings.joypad_menu_name + ">")
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 94 * self.settings.res_scale, "or joypad <" + self.settings.joypad_pause_name + ">")
                self.text.displayTextAt(self.alphabetWhite, 124 * self.settings.res_scale, 100 * self.settings.res_scale, "or joypad <" + self.settings.joypad_quit_name + ">")

        elif self.gameState == self.settings.state_pause:
            if (self.joystick.getCount() > 0):
                self.text.displayTextAt(self.alphabet, 80 * self.settings.res_scale, 70 * self.settings.res_scale, \
                    "<" + pygame.key.name(self.settings.key_fire) + "> or joypad <" + self.settings.joypad_fire_name + "> to unpause")
            else:
                self.text.displayTextAt(self.alphabet, 120 * self.settings.res_scale, 70 * self.settings.res_scale, \
                    "<" + pygame.key.name(self.settings.key_fire) + "> to unpause")

        elif self.gameState == self.settings.state_gameover:
            if (self.joystick.getCount() > 0):
                self.text.displayTextAt(self.alphabet, 80 * self.settings.res_scale, 120 * self.settings.res_scale, \
                    "<" + pygame.key.name(self.settings.key_menu) + "> or joypad <" + self.settings.joypad_menu_name + "> for menu")
            else:
                self.text.displayTextAt(self.alphabet, 120 * self.settings.res_scale, 120 * self.settings.res_scale, \
                    "<" + pygame.key.name(self.settings.key_menu) + "> for menu")

            self.text.displayTextAt(self.alphabet, 140 * self.settings.res_scale, 40 * self.settings.res_scale, "game over")

            # Show game stats
            self.text.displayTextAt(self.alphabet, 130 * self.settings.res_scale, 52 * self.settings.res_scale, "highscore: " + str(self.settings.highscore))
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 70 * self.settings.res_scale, "your score: " + str(self.settings.score))
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 76 * self.settings.res_scale, "gifts delivered: " + str(self.settings.gifts_delivered))
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 82 * self.settings.res_scale, "candy canes shot: " + str(self.settings.bullets_shot))
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 88 * self.settings.res_scale, "enemies neutralised: " + str(self.settings.enemies_killed))
            self.text.displayTextAt(self.alphabet, 100 * self.settings.res_scale, 94 * self.settings.res_scale, "distance travelled: " + str(self.settings.distance_travelled / 100) + " meters")

        elif self.gameState == self.settings.state_info:
            # Now show instructions
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 10 * self.settings.res_scale, "santa is running late due to losing some reindeer!")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 20 * self.settings.res_scale, "help him get these last few gifts delivered before dawn")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 30 * self.settings.res_scale, "arrives!")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 50 * self.settings.res_scale, "santas sleigh keeps losing power, so you have to keep")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 60 * self.settings.res_scale, "boosting it to stay afloat!")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 80 * self.settings.res_scale, "aim to drop the gifts into the chimney! make sure you")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 90 * self.settings.res_scale, "fly above the chimneys or the gifts wont release!")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 100 * self.settings.res_scale, "shoot those naughty creatures so they drop some goodies")
            self.text.displayTextAt(self.alphabetWhite, 20 * self.settings.res_scale, 110 * self.settings.res_scale, "for you to collect!")
            self.text.displayTextAt(self.alphabetWhite, 75 * self.settings.res_scale, 130 * self.settings.res_scale, "-biscuits top up your magic fuel-")
            self.text.displayTextAt(self.alphabetWhite, 90 * self.settings.res_scale, 140 * self.settings.res_scale, "-candies top up your ammo-")
            self.text.displayTextAt(self.alphabetWhite, 75 * self.settings.res_scale, 150 * self.settings.res_scale, "-stars top up your energy levels-")
            self.text.displayTextAt(self.alphabetWhite, 100 * self.settings.res_scale, 170 * self.settings.res_scale, "<press fire when ready>")
        
        return

    def resetJoypad(self):
        self.joypadBoostPressed = False
        self.joypadPressiePressed = False
        self.joypadBulletPressed = False
        self.joypadPausePressed = False
        self.joypadMenuPressed = False
        self.joypadQuitPressed = False

    #######################################################################
    # Run the game
    #######################################################################
    def run(self):
        run = True

        while run:
            # Set framerate to 60 fps
            clock.tick(self.settings.fps)
            self.resetJoypad()

            for event in pygame.event.get():
                # if event.type == pygame.VIDEORESIZE:
                #    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if (event.type == pygame.QUIT):
                    run = False

                if (event.type == pygame.KEYDOWN):
                    # self.keys = pygame.key.get_pressed()
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"key pressed: {pygame.key.name(event.key)}")

                if (event.type == pygame.JOYBUTTONDOWN):
                    getJoyButton = event.button
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Joypad button {getJoyButton} pressed on {self.joystick.getName()}")

                    if (getJoyButton == self.settings.joypad_pause):
                        self.joypadPausePressed = True

                    if (getJoyButton == self.settings.joypad_menu):
                        self.joypadMenuPressed = True

                    if (getJoyButton == self.settings.joypad_quit):
                        self.joypadQuitPressed = True
                    
                    if (getJoyButton == self.settings.joypad_boost):
                        self.joypadBoostPressed = True

                    if (getJoyButton == self.settings.joypad_pressie):
                        self.joypadPressiePressed = True

                    if (getJoyButton == self.settings.joypad_fire):
                        self.joypadBulletPressed = True

                # Joypad dpad hat position. All or nothing for direction
                if (self.joystick.getCount() > 0):
                    self.joystick.displayHats()
                    
            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                self.joystick.deviceAdded(event.device_index)

            if event.type == pygame.JOYDEVICEREMOVED:
                self.joystick.deviceRemoved()

            self.keys = pygame.key.get_pressed()
            self.screen = pygame.display.get_surface()
            self.screen.fill(self.settings.fill_colour)

            ###############################################
            if self.gameState == self.settings.state_game:
                if (self.settings.music_state == False):
                    if (self.settings.musicEnabled):
                        pygame.mixer.music.load(self.settings.music_game)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(abs(self.settings.volume - 0.2))
                        self.settings.music_state = True

                # Quit to menu
                if (self.keys[self.settings.key_menu] or self.joypadMenuPressed):
                    if (self.settings.music_state):
                        if (self.settings.musicEnabled):
                            pygame.mixer.music.stop()
                            self.settings.music_state = False

                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_menu)} - state: {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.resetStats()
                    self.gameState = self.settings.state_menu

                # Pause
                if (self.keys[self.settings.key_pause] or self.joypadPausePressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_pause)} - state: {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.gameState = self.settings.state_pause

                # Boost
                if (self.keys[self.settings.key_boost] or self.joypadBoostPressed):
                    if (self.settings.playerBoostState == False):
                        # If fuelQty = 0 then game over
                        if (self.settings.fuelQty > 0):
                            self.settings.playerBoostState = True
                            self.settings.fuelQty -= 1

                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_boost)} - state: {self.gameState}")

                # Drop pressie
                if (self.settings.pressieTimer >= 0 and self.pressies.howManyPressies() > 0):
                    self.settings.pressieTimer -= 1
                else:
                    self.settings.pressieTimer = self.settings.defaultPressieTimer

                if (self.settings.fuelQty > 0):
                    if (self.keys[self.settings.key_drop] or self.joypadPressiePressed):
                        playerPos = self.player.getPos()

                        # Check if player high enough to drop pressie
                        if (playerPos[1] < (self.settings.screen_height / 2) - (20 * self.settings.res_scale)):
                            if (self.settings.pressieTimer == self.settings.defaultPressieTimer):
                                self.pressies.addPressie(playerPos, self.settings.defaultGravity)
                            
                        if (self.settings.log_setting > 0):
                            self.logger.write(f"Pressed {pygame.key.name(self.settings.key_drop)} - state: {self.gameState}")

                # Shoot
                if (self.settings.fuelQty > 0):
                    if (self.joypadBulletPressed or self.keys[self.settings.key_fire]):
                        if (self.settings.ammoQty > 0 and self.settings.bulletTimer == self.settings.bulletTimerMax):
                            self.playerBullets.addBullet(self.player.getPos(), self.settings.defaultGravity)
                            self.settings.bulletTimer -= 1
                            self.settings.ammoQty -= 1
                            self.settings.bullets_shot += 1
                            pygame.mixer.Sound.play(self.settings.snd_shoot)
                                
                        if (self.settings.log_setting > 0):
                            self.logger.write(f"Pressed {pygame.key.name(self.settings.key_fire)} - state: {self.gameState}")

            elif self.gameState == self.settings.state_menu:

                # Set menu music to play
                if (self.settings.music_state == False):
                    if (self.settings.musicEnabled):
                        pygame.mixer.music.load(self.settings.music_menu)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(abs(self.settings.volume - 0.2))
                        self.settings.music_state = True

                # Quit game back to OS
                if (self.keys[self.settings.key_quit] or self.joypadQuitPressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_quit)} to quit")
                    run = False
                
                # Start game!
                if (self.keys[self.settings.key_boost] or self.joypadBoostPressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_fire)} to go to info - state {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.gameState = self.settings.state_info

            elif self.gameState == self.settings.state_pause:
                # unPause
                if (self.keys[self.settings.key_fire] or self.joypadBulletPressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_fire)} to unpause - state: {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.gameState = self.settings.state_game

            elif self.gameState == self.settings.state_gameover:
                if (self.settings.music_state):
                    if (self.settings.musicEnabled):
                        pygame.mixer.music.stop()
                        self.settings.music_state = False

                # Quit to menu
                if (self.keys[self.settings.key_menu] or self.joypadMenuPressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_boost)} to go to menu - state: {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.resetStats()
                    self.gameState = self.settings.state_menu

            elif self.gameState == self.settings.state_info:
                # Music setup
                if (self.settings.music_state):
                    if (self.settings.musicEnabled):
                        pygame.mixer.music.stop()
                        self.settings.music_state = False

                if (self.keys[self.settings.key_fire] or self.joypadBulletPressed):
                    if (self.settings.log_setting > 0):
                        self.logger.write(f"Pressed {pygame.key.name(self.settings.key_fire)} to go to game - state: {self.gameState}")
                    pygame.mixer.Sound.play(self.settings.snd_menuSound)
                    self.gameState = self.settings.state_game

            # Display stuff
            self.update()
            self.render()
            pygame.display.flip()

        pygame.mouse.set_visible(True)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    xmas_mayhem_game = Game()
    xmas_mayhem_game.run()