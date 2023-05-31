"""
A space 2D block blasasasasting game with ship upgrades, special game features and 
more!

Images and sounds from https://kenney.nl and google images
"""
from main_screen import *
from game_screen import *

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Blaster : Main Menu")
    main_menu = MenuView()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()