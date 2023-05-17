import arcade, random
from constant import *
from star import *
from bullet import *
from ship import *
from rock import *

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):

        # Call the parent class and set up the window
        super().__init__(width, height, title, resizable=True)
        
        arcade.set_background_color(arcade.color.BLACK)
        
        self.width = width
        self.height = height

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
        self.player_sprite = Ship(player_ship_image, CHARACTER_SCALING)
        self.player_list.append(self.player_sprite)   
                
        # call star function
        self.add_star()
        
        # make rock appear every second
        arcade.schedule(self.add_rock, 0.8)
        
    def on_resize(self, width, height):
        """ This method is  called when the window is resized. """

        super().on_resize(width, height)
    
    def draw_score(self):
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 20)
            
    def shoot(self):
        """Called when space pressed to shoot"""
        # Set up the bullet  
        bullet_image = ":resources:images/space_shooter/laserRed01.png"
        self.bullet_sprite = Bullet(bullet_image, BULLET_SCALING)
        
        self.bullet_sprite.center_x = self.player_sprite.center_x
        self.bullet_sprite.bottom = self.player_sprite.top

        self.bullet_list.append(self.bullet_sprite)

    def on_shoot(self):
        for bullet in self.bullet_list:
            rock_hit_list = arcade.check_for_collision_with_list(\
                bullet, self.rock_list)
            
            # If bullet hit rock, remove it
            if len(rock_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every rock hit, add to the score and also remove it
            self.remove_rock(rock_hit_list)
                                    
            # If the bullet flies from screen remove it
            if bullet.bottom > self.height:
                bullet.remove_from_sprite_lists()


    def add_rock(self, deltatime: float):
        # Create the rock
        image_num = random.randrange(5)
        image_list = [":resources:images/space_shooter/meteorGrey_med1.png",
                      ":resources:images/space_shooter/meteorGrey_med2.png",
                      ":resources:images/space_shooter/meteorGrey_big1.png",
                      ":resources:images/space_shooter/meteorGrey_big2.png",
                      ":resources:images/space_shooter/meteorGrey_big3.png",
                      ]
        self.rock_sprite = Rock(
            image_list[image_num],
            ROCK_SCALING,
            self.width,
            self.height
            )
        
        # Add the rock to the list
        self.rock_list.append(self.rock_sprite)    

    def remove_rock(self, rock_hit_list):
        for rock in rock_hit_list:
            rock.remove_from_sprite_lists()
            self.score += SCORE_INCREASE
            
            # play rock explosion sound
            explosion_select = random.randint(0,1)
            explosion_sounds = [":resources:sounds/explosion1.wav",
                                ":resources:sounds/explosion2.wav",
                                ]
            self.rock_hit_sound = arcade.load_sound(explosion_sounds[explosion_select])
            arcade.play_sound(self.rock_hit_sound)

    def add_star(self):
        # create 50 stars that will be recycled back to top of screen
        for i in range(50):
            self.star_sprite = Star(
                "images/shining-star.png",
                STAR_SCALING,
                self.width,
                self.height,
                )
            # Add the star to the list
            self.star_list.append(self.star_sprite)

    def recycle_star(self):
        for star in self.star_list:
            # Remove star when it is past the screen
            if star.bottom < 0:
                print(self.width, self.height)
                star.reset(self.width, self.width)

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
        self.draw_score()
                
    def on_update(self, delta_time):
        """Movement and game logic, control animations"""             
        # Update the lists
        self.star_list.update()
        self.rock_list.update()
        self.bullet_list.update()
        self.player_list.update()
                    
        # if bullet is shot
        if self.bullet_list:  
            self.on_shoot()
        
        # move star to top of screen
        self.recycle_star()
        
    def update_player_location(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        # If gone out of bounds this will bring the ship back
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > self.width - 1:
            self.player_sprite.right = self.width
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > self.height - 1:
            self.player_sprite.top = self.height

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