# xmasmayhem
Xmas game for Windows, Linux and Mac

Version 1.0
Run XmasMayhem.exe (Windows) / XmasMayhem (Linux) to start the game!

Story:
=====
Santa is running late due to some of his reindeer having gotten lost! Help him get these last few gifts delivered before sunrise! You'll find that his sleigh is struggling to stay in the air, so you will constantly need to boost it to stay up. When you want to release a gift, make sure to aim for the middle of the chimneys as best you can. You will also need to be above the chimneys before santa can drop any! Don't forget to shoot those nasties trying to take you out because they drop some very useful goodies such as biscuits (more fuel), candy canes (more bullets) and stars (more energy). 
If you go below the bottom of the screen, it's game over!
If you lose all your energy or fuel, it's game over!

Look at your stats when it's game over and see if you can beat it next time!

The game randomizes each play-through so it'll never be the same boring level and enemy placements.

Play info:
=========
The default controls for both joystick (when plugged in) or keyboard (when joystick not plugged in) is shown on the menu screen. These, along with audio volume, enable/disable music, full screen or game window scaling is all adjustable in the gamefolder/data/config.json file. Some further information is provided in the config file.
Only santa's head has a hitbox, so it should be fairly easy to dodge most bullets!

Talking of default controls, keyboard is:
Shoot - right arrow key
Boost - space key
Drop pressie - left arrow key
Pause game - p key
Go to menu - escape key
Quit game to desktop - F10 key

Joypad is (Playstation 3 pad):
Shoot - Circle
Boost - Triangle
Drop pressie - L1
Pause game - Start
Go to menu - Select
Quit game to desktop - PS button

Configuration: (gamefolder/data/config.json)
=============
- Window size:
You can set the window size by changing "screenSize" to a value between 2 to 6 (small to large). Or you can go fullscreen by setting "fullScreen" to true.

- Keyboard:
If you're trying to see which keyboard buttons you wish to use to play the game, you can enable logging in the config.json file (enable, set "logLevel" to 1). This will then record the button(s) you press. Quit the game then look at the gamefolder/data/log.txt file to see what they are called. 
Use those exact names in the "keyboard" section in config.json and save the file.

- Joypad:
By default, both Linux and Windows joypad controller configurations is set up for a PS3 pad. If you wish to use a joypad controller and/or yours has the buttons all wrong, check out what your OS provides.
In Windows 10 you can open your control panel->devices and printers. Then right-click your controller->Game controller settings. In here choose "Properties" and you will see each button number for the button you press. Change the number you want for an action in the config.json file under the "joypad" section relevant to your OS.
On Linux, you can install jstest-gtk and it will let you also see which button is pressed to a number.

If you're having problems with playing the game on your computer, you can enable logging and set it to logLevel 3. This will record everything, so reload the game after this change and try to replicate your bug/issue. All activities will be recorded to the gamefolder/data/log.txt file. You can zip this up and email it to jaco@blackjet.co.uk and I will try pinpoint the issue and hopefully get it fixed!

Apologies:
=========
The music isn't great, sorry, but I ran out of time. Nor are the sound effects really.

Credits:
=======
Graphics, music, sounds and code by Jaco van der Walt.
Thanks to the playtesters.

This game was made by Sensei of Blackjet in 2022. Check out blackjet.co.uk for more games.

