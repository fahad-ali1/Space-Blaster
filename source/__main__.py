"""
A space 2D block blasting game with ship upgrades, special game features and 
more!

Images and sounds from https://kenney.nl and google images

TODO in future: each score gives coins based on it and you can buy more ships, 
add menu music, add menu scrolling stars, add menu button hover feedback sound
and click sounds, add upgrade section, add instruction

NOTE: refactor + clean up all code and files
"""
from main_screen import *
from game_screen import *

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Main Menu")
    main_menu = MenuView()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()