import arcade, random
from constant import *

class Rock(arcade.Sprite):
    def __init__(self, image_file_name, scale, width = 1, height = 1):
        super().__init__(image_file_name, scale=scale)         
        # Position the rock
        self.center_x = random.randint(50, width - 50)
        self.center_y = random.randint(height+10, height+100)
        self.velocity = (0, random.uniform(-1.8, -0.8)) 