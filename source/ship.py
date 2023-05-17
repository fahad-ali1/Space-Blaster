import arcade
from constant import *

class Ship(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)  
        # Set ship coordinate
        self.center_x = 600
        self.center_y = 50
