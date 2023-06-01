"""
A 2D space blasting game

Images and sounds from https://kenney.nl and google images
"""
from main_screen import *
from game_screen import *

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Blaster")
    main_menu = MenuView()
    game_music = arcade.load_sound(":resources:music/1918.mp3")
    arcade.play_sound(game_music,volume=0.3,looping=True)
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()