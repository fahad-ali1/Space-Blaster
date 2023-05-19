from arcade.application import Window
from game_screen import *
from constant import *


class MenuView(arcade.View):
    """ Class that manages the 'Main Menu'. """

    def __init__(self, window: Window = None):
        super().__init__(window)
        self.play_hover = None
        self.exit_hover = None

    def on_show(self):
        # set background color
        arcade.set_background_color(arcade.color.BLACK)
        
    def on_draw(self):
        # clear previous screen
        self.clear()
        arcade.start_render()
        
        # draw game name
        arcade.draw_text("Space Blaster", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.75,
                    arcade.color.WHITE, font_size=45, anchor_x="center")
        
        arcade.draw_text("Author: Fahad", SCREEN_WIDTH - 10, SCREEN_HEIGHT * 0.03,
                    arcade.color.WHITE, font_size=10, anchor_x="right")
        arcade.draw_text("Version 1.00", SCREEN_WIDTH - 10, SCREEN_HEIGHT * 0.01,
                    arcade.color.WHITE, font_size=10, anchor_x="right")
        
        # changes button on hover
        if self.play_hover:
            arcade.draw_text("PLAY", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.33,
                            arcade.color.WHITE, font_size=40, anchor_x="center")
        else:
            arcade.draw_text("PLAY", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.33,
                            arcade.color.WHITE, font_size=25, anchor_x="center")
            
        if self.exit_hover:
            arcade.draw_text("EXIT", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.27,
                            arcade.color.WHITE, font_size=40, anchor_x="center")
        else:
            arcade.draw_text("EXIT", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.27,
                            arcade.color.WHITE, font_size=25, anchor_x="center")

    def on_mouse_press(self, x, y, _button, _modifiers):
        self.x1 = x
        self.y1 = y
        
        # If "play" is clicked launch game
        if (self.x1 >= SCREEN_WIDTH/2 + 60 and self.x1 <= SCREEN_WIDTH/2 -60)\
            or (self.y1 >= SCREEN_HEIGHT * 0.33 and self.y1 <= SCREEN_HEIGHT * 0.33 + 30):
            game_view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Blaster")
            game_view.setup()
            self.window.show_view(game_view)
        
        # If "exit" clicked then game closes
        if (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 -60)\
            and (self.y2 >= SCREEN_HEIGHT * 0.27 and self.y2 <= SCREEN_HEIGHT * 0.27 + 30):
            arcade.exit()
        
    def on_mouse_motion(self, x, y, dx, dy):
        """ When hover over button change colours """
        # set values
        self.x2 = x
        self.y2 = y
        self.play_hover = False
        self.exit_hover = False

        # change flags depending on hover
        if (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 -60)\
            and (self.y2 >= SCREEN_HEIGHT * 0.33 and self.y2 <= SCREEN_HEIGHT * 0.33 + 30):
            self.play_hover = True
        if (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 -60)\
            and (self.y2 >= SCREEN_HEIGHT * 0.27 and self.y2 <= SCREEN_HEIGHT * 0.27 + 30):
            self.exit_hover = True