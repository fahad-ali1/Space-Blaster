"""
A space 2D block blasting game with ship upgrades, special game features and 
more!

Images and sounds from https://kenney.nl and google images

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
ROCK_SCALING = 1

# Star Scaling
STAR_SCALING = 0.025

# Score
SCORE_INCREASE = 1
                    
class  Star(arcade.Sprite):
    # reset star once it is past the bottom of screen
    def reset(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 10, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)
    
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.BLACK)
                
        # The lists that keep track of all sprites. Each sprite will 
        # go into a list.
        self.player_list = None
        self.bullet_list = None
        self.rock_list = None
        self.star_list = None
                
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
        self.star_list = arcade.SpriteList()
        
        # This camera is used to display any GUI element (score, etc.)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Track score
        self.score = 0

        # Set up the ship
        player_ship_image = ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite = arcade.Sprite(player_ship_image, CHARACTER_SCALING)
        self.player_sprite.center_x = 600
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)   
                
        # call star function
        self.add_star()
        
        # make rock appear every second
        arcade.schedule(self.add_rock, 0.8)
                
    def shoot(self):
        """Called when space pressed to shoot"""
        # Set up the bullet  
        bullet_image = ":resources:images/space_shooter/laserRed01.png"
        self.bullet_sprite = arcade.Sprite(bullet_image, BULLET_SCALING)
        self.bullet_sprite.change_y = SHIP_BULLET_SPEED
        
        self.bullet_sprite.center_x = self.player_sprite.center_x
        self.bullet_sprite.bottom = self.player_sprite.top

        self.bullet_list.append(self.bullet_sprite)

    def add_rock(self, deltatime: float):
        # Create the rock
        image_num = random.randrange(5)
        image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                      ":resources:images/space_shooter/meteorGrey_med2.png",
                      ":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ]
        self.rock_sprite = arcade.Sprite(
            image_list[image_num],
            ROCK_SCALING,
            )
        
        # Position the rock
        self.rock_sprite.center_x = random.randint(50, SCREEN_WIDTH - 50)
        self.rock_sprite.center_y = random.randint(SCREEN_HEIGHT+10, SCREEN_HEIGHT+100)
        self.rock_sprite.velocity = (0, random.uniform(-2.2, -0.5)) 
        
        # Add the rock to the list
        self.rock_list.append(self.rock_sprite)    

    def add_star(self):
        for i in range(50):
            self.star_sprite = Star(
                "images/shining-star.png",
                STAR_SCALING,
                )
            # Position the star
            self.star_sprite.center_x = random.randint(0, SCREEN_WIDTH)
            self.star_sprite.center_y = random.randint(0, SCREEN_WIDTH)
            self.star_sprite.velocity = (0, random.uniform(-2.5, -1))
            
            # Add the star to the list
            self.star_list.append(self.star_sprite)

    def on_draw(self):
        """Render to the screen"""

        # Clear previous screen
        self.clear()
        
        # Code to draw the screen goes here, here I draw my sprites
        self.star_list.draw()
        self.rock_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        
        # This will activate the camera in order to draw to GUI
        self.gui_camera.use()

        # Draw score on the screen bottom left corner
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 20)
                
    def on_update(self, delta_time):
        """Movement and game logic, control animations"""             
        # Update the lists
        self.star_list.update()
        self.rock_list.update()
        self.bullet_list.update()
        self.player_list.update()
        
        # if bullet is shot
        if self.bullet_list:  
            for bullet in self.bullet_list:
                rock_hit_list = arcade.check_for_collision_with_list(\
                    bullet, self.rock_list)
                
                # If bullet hit rock, remove it
                if len(rock_hit_list) > 0:
                    bullet.remove_from_sprite_lists()

                # For every rock hit, add to the score and also remove it
                for rock in rock_hit_list:
                    rock.remove_from_sprite_lists()
                    self.score += SCORE_INCREASE
                    
                    # play rock explosion sound
                    arcade.play_sound(self.rock_hits)
                                        
                # If the bullet flies from screen remove it
                if bullet.bottom > SCREEN_HEIGHT:
                    bullet.remove_from_sprite_lists()
        
        for star in self.star_list:
            # Remove star when it is past the screen
            if star.bottom < 0:
                star.reset()
        
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