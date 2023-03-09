
# A 2-D Space Invader game in python using pygame module

The project is an example that was built along with a Youtube Video showing to create a space invader game using pygame module in python programming language. The basic structure of the program is as follows:

* First we have imported all the required modules.
* Then load all our assets requiured in this game and stored it in variables.
* We have two parent classes Laser and Ship along with two child classes Player and Enemy ship.
* Then we have our main game loop.
* I have separately created a main menu function for displaying the main menu for the game.
* All the functions for Collision and Shooting are included inside the Ship class since it's a common function for enemy as well as player ship.
* The health bar function for displaying players health is included inside the Player class.
* I have included 10 levels in this game as the level increses the velocity of the Enemy Space Ships will increase.
* Have added some basic sound effects.

## HOW TO INSTALL THIS AND PLAY!

* Make sure that pygame module is installed in your system
1. Download the souce code.
2. Download all the assets.
3. Put all the assets in a folder.
4. Now put that assets folder and the source code in a main folder.
5. Delete all the asset paths in the source code and put the path of that asset of your computer there.
6. Now you are ready to Play and Enjoy the game!.

## Found a Bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issue tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

In my device there was some issues with the #pygame.mixer.init() thats why i have commented the sound effects statements.
* You can uncomment and check, it may work fine in your system.