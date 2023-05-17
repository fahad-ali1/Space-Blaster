import arcade, random
from constant import *

class  Star(arcade.Sprite):
    def __init__(self, image_file_name, scale, width = 1, height = 1):
        super().__init__(image_file_name, scale=scale)  
        # Position the star
        self.center_x = random.randint(0, width)
        self.center_y = random.randint(0, width)
        self.velocity = (0, random.uniform(-2, -1.5))
            
    # reset star once it is past the bottom of screen
    def reset(self, width, height):
        self.center_y = random.randrange(height + 10, height + 100)
        self.center_x = random.randrange(width)
