import arcade
# Constants for the screen and title
width, height = arcade.window_commands.get_display_size()
SCREEN_WIDTH = width-200
SCREEN_HEIGHT = height-200
SCREEN_TITLE = "Space Blaster"

# Constants used to scale the sprites
SHIP_SCALING = 1

# Movement speed of player, in pixels per frame
PLAYER_SHIP_MAX_SPEED = 15
PLAYER_ACCEL = 0.1
PLAYER_SHIP_DRAG = 0.02

# Movement speed of bullet
SHIP_BULLET_SPEED = 20
BULLET_SCALING = 1
MAX_180_BULLETS = 2
MAX_MOUSE_BULLETS = 2

# Rock Scaling
ROCK_SCALING = 1

# Star Scaling
STAR_SCALING = 0.025

# Score
SCORE_INCREASE = 1