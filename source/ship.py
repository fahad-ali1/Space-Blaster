import arcade
from constant import *

class Ship(arcade.Sprite):
    """Some code referenced from:
    https://api.arcade.academy/en/latest/examples/sprite_move_keyboard_better.html"""
    def __init__(self, image_file_name, scale, width = 1, height = 1):
        super().__init__(image_file_name, scale=scale)         
        self.screen_width = width
        self.screen_height = height
        
        self.center_x = width//2
        self.center_y = 50
        
    def update(self):
        """moves player"""
        # move player
        self.center_x += self.change_x 
        self.center_y += self.change_y

        # Cannot go out of bounds
        if self.bottom < -30:
            self.bottom = -30
        elif self.top > self.screen_height + 30:
            self.top = self.screen_height + 30
            
        if self.left < -30:
            self.left = -30
        elif self.right > self.screen_width + 30:
            self.right = self.screen_width + 30
            
        super().update()