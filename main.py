"""
A space 2D block blasting game with ship upgrades, special game features and 
more!

Images and sounds from https://kenney.nl

TODO: ADd walls/ boundaries, Add menu screen, add scores, each score gives coins based on it and you can 
buy more ships, add rocks and animation for rocks, 


"""
import arcade
import random

# Constants for the screen and title
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN_TITLE = "2D Space Blaster"

# Constants used to scale the sprites
CHARACTER_SCALING = 1

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 15

# Movement speed of bullet
SHIP_BULLET_SPEED = 20
BULLET_SCALING = 1

# Rock Scaling
ROCK_COUNT = 2
ROCK_SCALING = 2
ROCK_FALL_SPEED = 1.5

# Score
SCORE_INCREASE = 1
            
class Rock(arcade.Sprite):
    """Each object is a single rock, ranging from small, medium, to large rocks"""

    def update(self):
        # Move the rock
        self.center_y -= ROCK_FALL_SPEED

        # If rock falls below screen TODO: end game, lose
        if self.top < 0:
            pass
        
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.GAINSBORO)
                
        # The lists that keep track of all sprites. Each sprite will 
        # go into a list.
        self.player_list = None
        self.bullet_list = None
        self.rock_list = None
                
        # This camera is used to display any GUI element (score, etc.)
        self.gui_camera = None
        
        # Players score
        self.player_score = 0
        
        # Game state
        self.game_end = False
        
        # Load sounds
        self.rock_hits = arcade.load_sound(":resources:sounds/explosion2.wav")
                        
        # Tracks keys pressed or not
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
            
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        
        # This camera is used to display any GUI element (score, etc.)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Track score
        self.score = 0

        # Game state
        self.game_end = False

        # Set up the ship
        image_source = ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)   
        
        # Create the rocks TODO: Change to while loop while player is alive so
        # that it keeps creating rocks 
        for i in range(ROCK_COUNT):
            # Create the rock instances
            self.rock_sprite = Rock(
                ":resources:images/space_shooter/meteorGrey_med2.png",
                ROCK_SCALING - random.randint(-1,1),
                )
            
            # Position the rocks
            self.rock_sprite.center_x = random.randrange(SCREEN_WIDTH)
            self.rock_sprite.center_y = random.randint(SCREEN_HEIGHT-50, SCREEN_HEIGHT)
            
            # Add the rocks to the lists
            self.rock_list.append(self.rock_sprite)            


    def shoot(self):
        """Called when space pressed to shoot"""
        # Set up the bullet  
        bullet_source = ":resources:images/space_shooter/laserRed01.png"
        self.bullet_sprite = arcade.Sprite(bullet_source, BULLET_SCALING)
        self.bullet_sprite.change_y = SHIP_BULLET_SPEED
        
        self.bullet_sprite.center_x = self.player_sprite.center_x
        self.bullet_sprite.bottom = self.player_sprite.top
        
        self.bullet_list.append(self.bullet_sprite)

    def on_draw(self):
        """Render to the screen"""

        self.clear()
        # Code to draw the screen goes here, here I draw my sprites
        self.player_list.draw()
        self.bullet_list.draw()
        self.rock_list.draw()
        
        # This will activate the camera in order to draw to GUI
        self.gui_camera.use()

        # Draw score on the screen bottom left corner
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 18)
                
    def on_update(self, delta_time):
        """Movement and game logic, control animations"""   
        if not self.game_end:
             
            # This will update the bullet
            self.bullet_list.update()
            # This will update the player
            self.player_list.update()
            # This will update the rocks
            self.rock_list.update()
            
            # if bullet is shot
            if self.bullet_list:  
                for bullet in self.bullet_list:
                    rock_hit_list = arcade.check_for_collision_with_list(\
                        bullet, self.rock_list)
                    
                    # If bullet hit rock, remove it
                    if len(rock_hit_list) > 0:
                        bullet.remove_from_sprite_lists()

                    # For every rock hit, add to the score and remove the rock
                    for rock in rock_hit_list:
                        rock.remove_from_sprite_lists()
                        self.score += SCORE_INCREASE
                        
                        # play rock explosion sound
                        arcade.play_sound(self.rock_hits)
                        
                    # If the bullet flies from screen remove it (for efficiency)
                    if bullet.bottom > SCREEN_HEIGHT:
                        bullet.remove_from_sprite_lists()
                        
            # If rock flies past bottom of screen or hits you, you lose
            for rock in self.rock_list:
                rock_hit_player = arcade.check_for_collision_with_list(\
                    self.player_sprite, self.rock_list)
                if len(rock_hit_player) > 0 or rock.bottom < 0:
                    # NOTE: END GAME HERE
                    self.game_end = True    

    def update_player_location(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # If gone out of bounds this will bring the ship back
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > SCREEN_WIDTH - 1:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > SCREEN_HEIGHT - 1:
            self.player_sprite.top = SCREEN_HEIGHT

        # Moves the ship by a certain amount
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED   

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
            self.update_player_location()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            self.update_player_location()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
            self.update_player_location()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
            self.update_player_location()
        elif key == arcade.key.SPACE:
            self.shoot() 
            
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.update_player_location()
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            self.update_player_location()
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_location()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_location()
                    
def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()