import arcade
from constant import *

class Bullet(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)  
        # Move bullet speed      
        self.change_y = SHIP_BULLET_SPEED
        self.center_x = None
        
        # Load bullet sound
        self.bullet_sound = arcade.load_sound(":resources:sounds/laser3.wav")
        # Play bullet sound
        arcade.play_sound(self.bullet_sound)
