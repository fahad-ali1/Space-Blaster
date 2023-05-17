"""
A space 2D block blasting game with ship upgrades, special game features and 
more!

Images and sounds from https://kenney.nl and google images

TODO:  Add menu screen, each score gives coins based on it and you can 
buy more ships
"""

from game_screen import *

def main():
    """Main function"""
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()