from arcade.application import Window
from game_screen import *
from constant import *

class HelpView(arcade.View):
    """ Class to show help and instructions of game """
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85,
                         arcade.color.WHITE, font_size=90, anchor_x="center")
        
        arcade.draw_text("HOW TO PLAY:\n1. Shoot straight with" 
                         "space bar\n2. Shoot any where with mouse\n3. Move "
                         "around with WASD keys or arrow keys on keyboard\nNOTE: "
                         "You are unable to spam bullets\n\nOBJECTIVE\n- Destroy "
                         "as many rocks as you can\n- No real objective, just "
                         "shoot rocks and get a high score\n- DO NOT crash "
                         "into rocks\n- DO NOT let rock fly past you\n", SCREEN_WIDTH / 2, 
                         SCREEN_HEIGHT * 0.77, arcade.color.WHITE, font_size=17,multiline=True,
                         anchor_x="center", width = 900)
                
        arcade.draw_text("Click anywhere to go back to main menu", SCREEN_WIDTH / 2, 
                         SCREEN_HEIGHT * 0.1, arcade.color.RED, font_size=30,
                         anchor_x="center")

    def on_mouse_press(self, x, y, _button, _modifiers):
        main_menu = MenuView()
        self.window.show_view(main_menu)
        
class MenuView(arcade.View):
    """ Class that manages the main menu """

    def __init__(self, window: Window = None):
        self.game_music = arcade.load_sound(":resources:music/1918.mp3")
        arcade.play_sound(self.game_music,volume=0.3,looping=True)
        
        super().__init__(window)
        self.play_hover = None
        self.help_hover = None
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
        
        # Change button appearance on hover
        play_font_size = 40 if self.play_hover else 25
        help_font_size = 40 if self.help_hover else 25
        exit_font_size = 40 if self.exit_hover else 25

        arcade.draw_text("PLAY", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.33,
                         arcade.color.WHITE, font_size=play_font_size, anchor_x="center")
        arcade.draw_text("HELP", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.28,
                         arcade.color.WHITE, font_size=help_font_size, anchor_x="center")
        arcade.draw_text("EXIT", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.23,
                         arcade.color.WHITE, font_size=exit_font_size, anchor_x="center")

    def on_mouse_press(self, x, y, _button, _modifiers):
        self.x1 = x
        self.y1 = y
        self.hover = arcade.load_sound(":resources:sounds/coin2.wav")
        
        play_clicked = (self.x1 >= SCREEN_WIDTH/2 + 60 and self.x1 <= SCREEN_WIDTH/2 - 60) \
                    or (self.y1 >= SCREEN_HEIGHT * 0.33 and self.y1 <= SCREEN_HEIGHT * 0.33 + 30)
        
        help_clicked = (self.x1 <= SCREEN_WIDTH/2 + 60 and self.x1 >= SCREEN_WIDTH/2 - 60) \
                    and (self.y1 >= SCREEN_HEIGHT * 0.28 and self.y1 <= SCREEN_HEIGHT * 0.28 + 30)
        
        exit_clicked = (self.x1 <= SCREEN_WIDTH/2 + 60 and self.x1 >= SCREEN_WIDTH/2 - 60) \
                    and (self.y1 >= SCREEN_HEIGHT * 0.23 and self.y1 <= SCREEN_HEIGHT * 0.23 + 30)
        
        # If "play" is clicked launch game
        if play_clicked:
            self.window.game_view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Blaster")
            arcade.play_sound(self.hover, volume=0.03)
            self.window.game_view.setup()
            self.window.show_view(self.window.game_view)
            
        # If "help" clicked then instruction pops up
        if help_clicked:
            arcade.play_sound(self.hover, volume=0.03)
            self.window.help_view = HelpView()
            self.window.show_view(self.window.help_view)
            
        # If "exit" clicked then game closes
        if exit_clicked:
            arcade.exit()
        
    def on_mouse_motion(self, x, y, dx, dy):
        """ When hover over button change appearance """
        self.x2 = x
        self.y2 = y
        
        self.play_hover = (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 - 60) \
                        and (self.y2 >= SCREEN_HEIGHT * 0.33 and self.y2 <= SCREEN_HEIGHT * 0.33 + 30)
        
        self.help_hover = (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 - 60) \
                        and (self.y2 >= SCREEN_HEIGHT * 0.28 and self.y2 <= SCREEN_HEIGHT * 0.28 + 30)
        
        self.exit_hover = (self.x2 <= SCREEN_WIDTH/2 + 60 and self.x2 >= SCREEN_WIDTH/2 - 60) \
                        and (self.y2 >= SCREEN_HEIGHT * 0.23 and self.y2 <= SCREEN_HEIGHT * 0.23 + 30)
