import pygame, os

class Settings:

    def __init__(self):
        self.version                    = 1.0
        self.logging_enabled            = False
        self.log_size                   = 1000
        self.log_setting                = 0
        self.debug                      = 0
        self.release                    = 1
        self.build                      = self.release          # Change to RELEASE when building .exe (use "BuildLinuxExe.sh" or "BuildWindowsExe.bat")

        self.game_width                 = 320                   # Pixel width
        self.game_height                = 180                   # Pixel height
        self.res_scale                  = 4                     # Scale of "low res" screen
        self.font_scale                 = 0.5                   # Scale of font graphics
        self.text_spacing               = 10 * self.res_scale
        self.screen_width               = self.game_width * self.res_scale
        self.screen_height              = self.game_height * self.res_scale
        '''
        # Get list of display modes - Find the first mode and use it, or if fail, use tmp values above
        displayArr = pygame.display.list_modes()
        self.screen_width = displayArr[0][0]
        self.screen_height = displayArr[0][1]
        if (displayArr != -1):
            self.fake_width                 = self.screen_width / self.res_scale
            self.fake_height                = self.screen_height / self.res_scale
        else:
            self.fake_width                 = self.screen_width_tmp / self.res_scale
            self.fake_height                = self.screen_height_tmp / self.res_scale
        '''
        self.is_fullscreen              = False
        # https://riptutorial.com/pygame/topic/6442/creating-a-window-in-pygame---pygame-display-set-mode--

        # Files
        self.config_file                = "config.json"
        self.font_file                  = "font.png"
        self.font_white_file            = "font-white.png"
        self.level01_file               = "level01.png"
        self.bg01_file                  = "bg01.png"
        self.fg01_file                  = "fg01.png"
        self.fg02_file                  = "fg02.png"
        self.bar_bg_file                = "bar-bg.png"
        self.weather_level01_file       = "weather01.png"
        self.house01File                = "house01.png"
        self.log_file                   = "log.txt"
        self.playerFile                 = "santa.png"
        self.playerFlashFile            = "santa-flash.png"
        self.bullet_file                = "bullet.png"
        self.small_sprites_file         = "sprites.png"
        self.snowman_file               = "snowman.png"
        self.grinch_file                = "grinch.png"
        self.splash_file                = "splash.png"
        self.explosion_file             = "puff.png"

        self.volume                     = 1.0
        self.musicEnabled               = True
        self.snd_shoot                  = pygame.mixer.Sound(self.getPath("shoot.wav"))
        self.snd_pressie                = pygame.mixer.Sound(self.getPath("pressie.wav"))
        self.snd_enemyHit               = pygame.mixer.Sound(self.getPath("enemyhit.wav"))
        self.snd_enemyShoot             = pygame.mixer.Sound(self.getPath("enemyshoot.wav"))
        self.snd_playerHit              = pygame.mixer.Sound(self.getPath("playerhit.wav"))
        self.snd_menuSound              = pygame.mixer.Sound(self.getPath("menu.wav"))
        self.snd_gameOver               = pygame.mixer.Sound(self.getPath("gameover.wav"))
        self.snd_collect                = pygame.mixer.Sound(self.getPath("collect.wav"))

        self.music_menu                 = self.getPath("xmasMenu.wav")
        self.music_game                 = self.getPath("xmasGame.wav")
        self.music_state                = False

        # Vars and Constants
        self.BULLET                     = 0             # Spritesheet position of each image
        self.SNOWBALL                   = 1
        self.STAR                       = 2
        self.BISCUIT                    = 3
        self.PRESSIE                    = 4
        self.COAL                       = 5
        self.AMMO                       = 6
        self.ENERGY                     = 7
        self.FUEL                       = 8
        self.SHIELD                     = 9

        self.houseY                     = self.screen_height
        self.house01SpriteParams        = [0, 1, 1]     # start frame, no of frames, anim speed in ms
        self.houseCols                  = 5             # How many houses in the image
        self.houseQty                   = 1000          # how many houses per level
        self.houseQtyMax                = self.houseQty # Default
        self.snowmanSpriteParams        = [0, 10, 2, 50]    # start frame, no of frames, anim speed in ms, pause before loop restarts
        self.grinchSpriteParams         = [0, 10, 2, 40]    # start frame, no of frames, anim speed in ms, pause before loop restarts
        self.explosionSpriteParams      = [0, 10, 4, 0]
        self.enemyLeftX                 = 40 * self.res_scale  # This is the left-most an enemy will be to shoot and to be updated
        self.enemyHealth                = 100
        self.playerSpriteParams         = [0, 20, 3, 0]    # start frame, no of frames, anim speed in ms
        self.playerX                    = 5 * self.res_scale
        self.playerY                    = 62 * self.res_scale
        self.playerDefaultBoost         = 10          # Amount of upward boost player gets
        self.playerBoost                = self.playerDefaultBoost
        self.defaultGravity             = 0.5           # Initial gravity amount
        self.gravity                    = self.defaultGravity
        self.gravityExpo                = 0.05         # Amount added to gravity to speed up the drop
        self.bulletGravity              = self.gravityExpo * (self.res_scale / 2)
        self.pressieGravity             = self.gravityExpo * self.res_scale
        self.playerBoostState           = False         # True when player hits boost
        self.playerPressieState         = False         # True when player drops pressie
        self.backgroundSpeed            = 1
        self.windSpeed                  = 2
        self.defaultPressieTimer        = 40            # Time between prev and next pressie
        self.pressieTimer               = self.defaultPressieTimer
        self.invulnerabilityTimerMax    = 10            # Set the timer for how fast the flashing occurs
        self.invulnerabilityTimer       = self.invulnerabilityTimerMax
        self.flashCounterMax            = 10             # Sets how many times the player flashes
        self.flashCounter               = self.flashCounterMax
        self.playerHit                  = False         # Player has been hit state
        self.enemyBulletSpeed           = 3             # Speed of enemy bullets
        self.bulletTimerMax             = 30            # Time between enemy bullets
        self.bulletSpeed                = 2.5 * self.res_scale
        self.defaultBulletTimer         = 40           # Time between prev and next bullets
        self.bulletTimer                = self.defaultBulletTimer
        self.bulletStartX               = 100 * self.res_scale
        self.bulletStartY               = 13 * self.res_scale
        self.pressieStartX              = 20 * self.res_scale
        self.pressieStartY              = 20 * self.res_scale

        self.ammoQty                    = 100
        self.energyQty                  = 100
        self.fuelQty                    = 100

        self.fps                        = 60            # Frames per second.
        self.delta                      = 0
        self.getTicksLastFrame          = 0

        # Keyboard controls
        self.key_menu                   = pygame.K_ESCAPE
        self.key_quit                   = pygame.K_F10
        self.key_togglescreen           = pygame.K_f
        self.key_boost                  = pygame.K_SPACE
        self.key_drop                   = pygame.K_RETURN
        self.key_fire                   = pygame.K_LCTRL
        self.key_logger                 = pygame.K_KP_ENTER
        self.key_pause                  = pygame.K_p

        self.state_menu                 = 0
        self.state_game                 = 1
        self.state_pause                = 2
        self.state_gameover             = 3
        self.state_info                 = 4

        # Colour constants - RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).
        self.fill_colour                = (0, 42, 70)   # Game bg
        self.red                        = (230, 0, 0)       # in-game toolbars
        self.yellow                     = (230, 230, 0)
        self.green                      = (0, 230, 0)
        self.fullScreen                 = False

        # Menu texts
        self.score                      = 0
        self.highscore                  = 0
        self.gifts_delivered            = 0
        self.bullets_shot               = 0
        self.enemies_killed             = 0
        self.distance_travelled         = 0

    def getPath(self, file):
        return os.path.join(os.getcwd(), "./data", file)