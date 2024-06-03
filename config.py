# Class to load game settings from a file

import pygame, os, json, platform
from settings import Settings

class Config:
    def __init__(self, settings):
        self.settings = settings
        self.file = os.path.join(os.getcwd(), "data", self.settings.config_file)
        self.os = platform.system()

        # Use below to get the "friendly" name of a keycode identifier
        #print(pygame.key.name(pygame.K_ESCAPE))

        try:
            with open(self.file) as f:
                self.data = json.load(f)
                # Get keyboard config
                self.settings.key_fire                  = pygame.key.key_code(self.data["keyboard"]["shoot"])
                self.settings.key_drop                  = pygame.key.key_code(self.data["keyboard"]["dropPressie"])
                self.settings.key_boost                 = pygame.key.key_code(self.data["keyboard"]["boost"])
                self.settings.key_pause                 = pygame.key.key_code(self.data["keyboard"]["pause"])
                self.settings.key_menu                  = pygame.key.key_code(self.data["keyboard"]["menu"])
                self.settings.key_quit                  = pygame.key.key_code(self.data["keyboard"]["quit"])
                
                # Get joypad config using OS mappings
                # Button code mappings
                self.settings.joypad_fire               = self.data["joypad"][self.os.lower()]["shoot"][0]
                self.settings.joypad_pressie            = self.data["joypad"][self.os.lower()]["dropPressie"][0]
                self.settings.joypad_boost              = self.data["joypad"][self.os.lower()]["boost"][0]
                self.settings.joypad_pause              = self.data["joypad"][self.os.lower()]["pause"][0]
                self.settings.joypad_menu               = self.data["joypad"][self.os.lower()]["menu"][0]
                self.settings.joypad_quit               = self.data["joypad"][self.os.lower()]["quit"][0]

                # Name mappings for joypad
                self.settings.joypad_fire_name          = self.data["joypad"][self.os.lower()]["shoot"][1]
                self.settings.joypad_pressie_name       = self.data["joypad"][self.os.lower()]["dropPressie"][1]
                self.settings.joypad_boost_name         = self.data["joypad"][self.os.lower()]["boost"][1]
                self.settings.joypad_pause_name         = self.data["joypad"][self.os.lower()]["pause"][1]
                self.settings.joypad_menu_name          = self.data["joypad"][self.os.lower()]["menu"][1]
                self.settings.joypad_quit_name          = self.data["joypad"][self.os.lower()]["quit"][1]

                # Screen res
                if (self.data["screenSize"]["scale"] > 1 and self.data["screenSize"]["scale"] <= 6):
                    self.settings.res_scale             = self.data["screenSize"]["scale"]

                    # Fullscreen?
                    if (self.data["fullScreen"]):
                        self.settings.is_fullscreen = True
                        self.settings.res_scale = 4

                    self.settings.screen_width          = self.settings.game_width * self.settings.res_scale
                    self.settings.screen_height         = self.settings.game_height * self.settings.res_scale
                    self.settings.text_spacing          = 10 * self.settings.res_scale
                    
                    # Adjust fps based on screen size
                    if (self.settings.res_scale == 1):
                        self.settings.fps = 30
                        self.settings.playerDefaultBoost = 7

                    elif (self.settings.res_scale ==2):
                        self.settings.fps = 40
                        self.settings.playerDefaultBoost = 10    # done

                    elif (self.settings.res_scale ==3):
                        self.settings.fps = 50
                        self.settings.playerDefaultBoost = 12   # done

                    elif (self.settings.res_scale ==4):
                        self.settings.fps = 60
                        self.settings.playerDefaultBoost = 13   # done

                    elif (self.settings.res_scale ==5):
                        self.settings.fps = 70
                        self.settings.playerDefaultBoost = 15   # done

                    else:
                        self.settings.fps = 80
                        self.settings.playerDefaultBoost = 16   # done

                # Logging to file
                if (self.data["logging"]):
                    self.settings.logging_enabled       = True
                    self.settings.log_setting           = self.data["logLevel"]
                    if (self.settings.log_setting == 1):
                        self.settings.log_size = 10
                    elif (self.settings.log_setting == 2):
                        self.settings.log_size = 100
                    else:
                        self.settings.log_size = 1000

                else:
                    self.settings.logging_enabled       = False

                # More overrides
                self.settings.bulletStartX              = 100 * self.settings.res_scale
                self.settings.bulletStartY              = 13 * self.settings.res_scale
                self.settings.pressieStartX             = 20 * self.settings.res_scale
                self.settings.pressieStartY             = 20 * self.settings.res_scale
                self.settings.playerX                   = 5 * self.settings.res_scale
                self.settings.playerY                   = 62 * self.settings.res_scale
                self.settings.bulletSpeed               = 2.5 * self.settings.res_scale
                self.settings.bulletGravity             = self.settings.gravityExpo * (self.settings.res_scale / 2)
                self.settings.pressieGravity            = self.settings.gravityExpo * self.settings.res_scale

                # Audio voluume and mapping to sounds
                self.settings.volume                    = self.data["volume"]
                
                self.settings.snd_shoot.set_volume(self.settings.volume)
                self.settings.snd_pressie.set_volume(self.settings.volume)
                self.settings.snd_enemyHit.set_volume(self.settings.volume)
                self.settings.snd_enemyShoot.set_volume(self.settings.volume)
                self.settings.snd_playerHit.set_volume(self.settings.volume)
                self.settings.snd_menuSound.set_volume(self.settings.volume)
                self.settings.snd_gameOver.set_volume(self.settings.volume)
                self.settings.snd_collect.set_volume(self.settings.volume)

                self.settings.musicEnabled              = self.data["music"]

        except IOError:
            if (self.settings.log_setting == 2):
                print(f"Unable to load file: {self.file}")
            return
