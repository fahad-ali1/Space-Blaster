import arcade
import random
import math

from constant import *
from star import *
from bullet import *
from ship import *
from rock import *
from main_screen import *


class GameOverView(arcade.View):
    """ Class that manages game over view """
    
    def __init__(self, window: Window = None):
        super().__init__(window)
        
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        # Draw game over screen
        arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT * 0.5,\
            arcade.color.WHITE, font_size=60, anchor_x="center")
        arcade.draw_text("Click anywhere to restart", SCREEN_WIDTH/2, \
            SCREEN_HEIGHT * 0.5 - 60, arcade.color.WHITE, font_size=25,\
                anchor_x="center") 
        arcade.draw_text(f"Total score = {self.window.total_score}", SCREEN_WIDTH/2, \
            SCREEN_HEIGHT * 0.5 - 120, arcade.color.WHITE, font_size=25,\
                anchor_x="center") 
        
    def on_mouse_press(self, x, y, _button, _modifiers):
        game_view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT, "Space Blaster")
        game_view.setup()
        self.window.show_view(game_view)

class GameView(arcade.View):
    """ Main application class """

    def __init__(self, width, height, title, window: Window = None):

        # Call the parent class and set up the window
        super().__init__(window)
        
        arcade.set_background_color(arcade.color.BLACK)

        # The lists that keep track of all sprites. Each sprite will 
        # go into a list.
        self.player_list = None
        self.bullet_list = None
        self.mouse_bullet_list = None
        self.rock_list = None
        self.star_list = None
        
        self.width = width
        self.height = height
                
        # This camera is used to display any GUI element (score, etc.)
        self.gui_camera = None
        
        # Players score
        self.player_score = 0
        self.window.total_score = 0
                                
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
        self.mouse_bullet_list = arcade.SpriteList()
        self.rock_list = arcade.SpriteList()
        self.star_list = arcade.SpriteList()
        
        # This camera is used to display any GUI element (score, etc.)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Set up the ship
        player_ship_image = ":resources:images/space_shooter/playerShip1_blue.png"
        self.player_sprite = Ship(player_ship_image,
                                  SHIP_SCALING,
                                  self.width,
                                  self.height,
                                  )
        self.player_list.append(self.player_sprite)   
        
        # make rock appear every second
        arcade.schedule(self.add_rock, 0.8)
        
        # call star function
        self.add_star()
    
    def draw_score(self):
        score_text = f"Score: {self.player_score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 20)
    
    def hit_list (self, sprite_list):
        for bullet in sprite_list:
            rock_hit_list = arcade.check_for_collision_with_list(\
                bullet, self.rock_list)

            # If bullet hit rock, remove it
            if len(rock_hit_list) > 0:
                bullet.remove_from_sprite_lists()
 
            # For every rock hit, add to the score and also remove it
            self.remove_rock(rock_hit_list) 
              
            # If the bullet flies from screen remove it
            if bullet.bottom > self.width or bullet.top < 0 \
                or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()
                
    def shoot(self):
        """Called when space pressed to shoot"""
        # Set up the bullet, only allow maximum so that spam cannot occur
        bullet_image = ":resources:images/space_shooter/laserRed01.png"
        if len(self.bullet_list) < MAX_180_BULLETS:
            self.bullet_sprite = Bullet(bullet_image, BULLET_SCALING)
            
            self.bullet_sprite.center_x = self.player_sprite.center_x
            self.bullet_sprite.bottom = self.player_sprite.top

            self.bullet_list.append(self.bullet_sprite)

    def on_shoot(self):
        self.hit_list(self.bullet_list) 
        self.hit_list(self.mouse_bullet_list)

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
            self.player_score += SCORE_INCREASE
            self.window.total_score += SCORE_INCREASE
            
            # play rock explosion sound
            explosion_select = random.randint(0,1)
            explosion_sounds = [":resources:sounds/explosion1.wav",
                                ":resources:sounds/explosion2.wav",
                                ]
            self.rock_hit_sound = arcade.load_sound(explosion_sounds[explosion_select])
            arcade.play_sound(self.rock_hit_sound, volume=0.15)

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
                star.reset(self.width, self.width)

    def on_draw(self):
        """Render to the screen"""

        # Clear previous screen
        self.clear()
        
        # Code to draw the screen goes here, here I draw my sprites
        self.star_list.draw()
        self.rock_list.draw()
        self.bullet_list.draw()
        self.mouse_bullet_list.draw()
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
        self.mouse_bullet_list.update()
        self.player_list.update()

        # Check if a bullet is shot
        if self.bullet_list or self.mouse_bullet_list:
            self.on_shoot()

        # Check for collision between player and rocks or if rock goes off the screen
        for rock in self.rock_list:
            rock_player_collision = arcade.check_for_collision(rock, self.player_sprite)
            if rock_player_collision or rock.bottom < 0:
                # Show the game over view
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)

        # Move star to the top of the screen if it goes off the bottom
        self.recycle_star()

        # Update the player's location
        self.update_player_location()
        
    def update_player_location(self):
        """Move player ship. Code copied from 
        https://api.arcade.academy/en/latest/examples/sprite_move_keyboard_accel.html"""
        # Calculate speed based on the keys pressed
        if self.player_sprite.change_x > PLAYER_SHIP_DRAG:
            self.player_sprite.change_x -= PLAYER_SHIP_DRAG
        elif self.player_sprite.change_x < -PLAYER_SHIP_DRAG:
            self.player_sprite.change_x += PLAYER_SHIP_DRAG
        else:
            self.player_sprite.change_x = 0

        if self.player_sprite.change_y > PLAYER_SHIP_DRAG:
            self.player_sprite.change_y -= PLAYER_SHIP_DRAG
        elif self.player_sprite.change_y < -PLAYER_SHIP_DRAG:
            self.player_sprite.change_y += PLAYER_SHIP_DRAG
        else:
            self.player_sprite.change_y = 0
            
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y += PLAYER_ACCEL
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y += -PLAYER_ACCEL
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x += -PLAYER_ACCEL
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x += PLAYER_ACCEL

        if self.player_sprite.change_x > PLAYER_SHIP_MAX_SPEED:
            self.player_sprite.change_x = PLAYER_SHIP_MAX_SPEED
        elif self.player_sprite.change_x < -PLAYER_SHIP_MAX_SPEED:
            self.player_sprite.change_x = -PLAYER_SHIP_MAX_SPEED
        if self.player_sprite.change_y > PLAYER_SHIP_MAX_SPEED:
            self.player_sprite.change_y = PLAYER_SHIP_MAX_SPEED
        elif self.player_sprite.change_y < -PLAYER_SHIP_MAX_SPEED:
            self.player_sprite.change_y = -PLAYER_SHIP_MAX_SPEED

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. Code referenced from
        https://api.arcade.academy/en/latest/examples/sprite_bullets_aimed.html#sprite-bullets-aimed
        """
        if len (self.mouse_bullet_list) < MAX_MOUSE_BULLETS:
            bullet = Bullet(":resources:images/space_shooter/laserBlue01.png", BULLET_SCALING)
            # Create a bullet and position it at player ship
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get the mouse the destination location for the bullet
            dest_x = x
            dest_y = y

            # Do math to calculate how to get the bullet to the destination and 
            # calculate the angle
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it goes head on
            bullet.angle = math.degrees(angle)

            # Take the angle and send it by the speed
            bullet.change_x = math.cos(angle) * SHIP_BULLET_SPEED
            bullet.change_y = math.sin(angle) * SHIP_BULLET_SPEED

            self.mouse_bullet_list.append(bullet)
            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Reference from 
        https://api.arcade.academy/en/latest/examples/sprite_move_keyboard_better.html"""


        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.shoot() 
            
    def on_key_release(self, key, modifiers):
        """Called whenever a key is released. Reference from 
        https://api.arcade.academy/en/latest/examples/sprite_move_keyboard_better.html"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False