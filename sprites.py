import pygame
from random import choice

from settings import *


class Spritesheet:
    """A class for the Spritesheet."""

    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        """Grab image out of a larger spritesheet."""
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image


class Player(pygame.sprite.Sprite):
    """Class for our Player(Frogger)."""

    def __init__(self, game):
        """Initilize player and set starting position."""
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # movement flags
        self.facing = 'up'
        self.moving = False

        # animation variables
        self.current_frame = 0
        self.last_update = 0

        # load the initial image of frogger
        self.load_images()
        if self.facing == 'up':
            self.image = self.up_frames[0]
        if self.facing == 'down':
            self.image = self.down_frames[0]
        if self.facing == 'right':
            self.image = self.right_frames[0]
        if self.facing == 'left':
            self.image = self.left_frames[0]
        self.rect = self.image.get_rect()

        # starting position (bottom middle of screen)
        self.x = (5.5) * TILESIZE
        self.y = (11.5) * TILESIZE

        # life counter
        self.lives = 3

    def load_images(self):
        """Function to load all of froggers images."""
        self.down_frames = [pygame.transform.scale(
                                self.game.spritesheet.get_image(1, 30, 52, 36),
                                (45, 31)),
                            pygame.transform.scale(
                                self.game.spritesheet.get_image(54, 28, 57, 36),
                                (49, 31)),
                            pygame.transform.scale(
                                self.game.spritesheet.get_image(113, 19, 56, 51),
                                (51, 46)),
                            pygame.transform.scale(
                                self.game.spritesheet.get_image(285, 20, 56, 51),
                                (51, 46)),
                            ]
        self.up_frames = []
        self.right_frames = []
        self.left_frames = []

        for frame in self.down_frames:
            frame.set_colorkey(BLACK)
            self.up_frames.append(pygame.transform.flip(frame, False, True))
            self.right_frames.append(pygame.transform.rotate(frame, 90))
            self.left_frames.append(pygame.transform.rotate(frame, -90))

    def move(self, direction):
        """Move Frogger one tile down."""
        if direction == 'down':
            self.y += TILESIZE
            self.facing = 'down'
        if direction == 'up':
            self.y -= TILESIZE
            self.facing = 'up'
        if direction == 'right':
            self.x += TILESIZE
            self.facing = 'right'
        if direction == 'left':
            self.x -= TILESIZE
            self.facing = 'left'

    def animate(self):
        """Animate Frogger image."""
        now = pygame.time.get_ticks()

        # check if frogger is moving
        if self.moving:
            if now - self.last_update > 16:
                self.last_update = now
                self.current_frame += 1

                if self.current_frame >= len(self.down_frames):
                    self.current_frame = 0
                    self.moving = False
                
                # change image based on direction of movement
                if self.facing == 'up':
                    self.image = self.up_frames[self.current_frame]
                if self.facing == 'down':
                    self.image = self.down_frames[self.current_frame]
                if self.facing == 'right':
                    self.image = self.right_frames[self.current_frame]
                if self.facing == 'left':
                    self.image = self.left_frames[self.current_frame]
                self.rect = self.image.get_rect()

    def in_bushes(self):
        """Frogger is in the top row of screen (whether in home or not)"""
        if self.rect.y < 1.5 * TILESIZE:
            return True
        else:
            return False
    
    def in_water(self):
        """Frogger is in the water (whether on log of not)"""
        if self.rect.y < 5.5 * TILESIZE and self.rect.y > 1.5 * TILESIZE:
            return True
        else:
            return False

    def reset_pos(self):
        """Return frogger back to starting position."""
        self.image = self.up_frames[0]

        self.x = 5.5 * TILESIZE
        self.y = 11.5 * TILESIZE

    def update(self):
        """Update the player."""
        self.animate()
        self.rect.centerx = self.x
        self.rect.centery = self.y


class Home(pygame.sprite.Sprite):
    """Class to manage scoring zones(homes)."""

    def __init__(self, game, x):
        """Initialize home attributes."""
        self.groups = game.all_sprites, game.homes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # create a transparent square in scoring zones
        self.image = pygame.Surface((TILESIZE / 4, TILESIZE / 4))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = 1.6 * TILESIZE


class Car(pygame.sprite.Sprite):
    """Class to manage cars."""

    def __init__(self, game, lane):
        """Initialize car attributes."""
        self.groups = game.all_sprites, game.cars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.lane = lane
        
        # set the image of the car
        self.load_images()
        if self.lane == ROAD_LANES[0]:
            self.image = self.car_imgs['car1']
        elif self.lane == ROAD_LANES[1]:
            self.image = self.truck_img
        elif self.lane == ROAD_LANES[2]:
            self.image = self.car_imgs['car3']
        elif self.lane == ROAD_LANES[3]:
            self.image = self.car_imgs['car2']
        
        # set the direction of the car based on which lane it's in
        self.dir = LANE_DIRS[self.lane]
        
        # flip if moving left
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        # Set start position based on direction
        if self.dir == 1:
            # start left of screen
            self.rect.x = -(self.rect.width)
        else:
            #start right of screen
            self.rect.x = WIDTH     
        self.rect.centery = self.lane * TILESIZE

        # car's speed is multiplied by the dir (+1 for right, -1 for left)
        self.speed = CAR_SPEED[lane] * self.dir

        # store the exact x location
        self.x = float(self.rect.x)

    def load_images(self):
        """Load different types of car images."""
        self.truck_img = pygame.transform.scale(
            self.game.spritesheet.get_image(11, 408, 174, 63), (110, 40))
        self.car_imgs = {
            'car1': pygame.transform.scale(
                self.game.spritesheet.get_image(13, 485, 125, 65), (77, 40)),
            'car2': pygame.transform.scale(
                self.game.spritesheet.get_image(157, 485, 132, 67), (79, 40)),
            'car3': pygame.transform.scale(
                self.game.spritesheet.get_image(306, 484, 132, 67), (79, 40)),
            }

    def update(self):
        """Update car."""
        # if car exits the screen, return it to original position
        if self.dir == 1 and self.rect.left > WIDTH:
            self.x = -(self.rect.width)
        if self.dir == -1 and self.rect.right < 0:
            self.x = WIDTH
        
        # move the car by adding speed to its positions
        self.x += self.speed
        self.rect.x = self.x


class Platform(pygame.sprite.Sprite):
    """Class to manage logs."""
    
    def __init__(self, game, lane):
        """Initialize log attributes."""
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.lane = lane

        # set animation counters
        self.current_frame = 0
        self.last_update = 0
        
        # set the image of the platform
        self.load_images()
        # water lane 3 will be turtle lane later
        if self.lane == WATER_LANES[2]:
            self.image = self.turtle_frames[0]
        elif self.lane == WATER_LANES[0] or self.lane == WATER_LANES[3]:
            self.image = self.log_imgs['sm']
        elif self.lane == WATER_LANES[1]:
            self.image = self.log_imgs['md']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        # set direction based on lane
        self.dir = LANE_DIRS[self.lane]
        
        # Set start position based on direction
        if self.dir == 1:
            # start left of screen
            self.rect.x = -self.rect.width
        else:
            #start right of screen
            self.rect.x = WIDTH     
        self.rect.centery = self.lane * TILESIZE

        # platform speed is multiplied by the dir (+1 for right, -1 for left)
        self.speed = PLATFORM_SPEED[lane] * self.dir

        # store the exact x location
        self.x = float(self.rect.x)

    def load_images(self):
        """Load images for different types of logs."""
        # list of log imgs
        self.log_imgs = {
            'sm': pygame.transform.scale(
                self.game.spritesheet.get_image(388, 258, 183, 58), (126, 40)),
            'md': pygame.transform.scale(
                self.game.spritesheet.get_image(15, 328, 270, 58), (186, 40)),
            }
        # list of turtle imgs
        self.turtle_frames = [
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load("images/turtles1.png"), (174, 47)), 
                    True, False),
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load("images/turtles2.png"), (174, 50)),
                    True, False),
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load("images/turtles3.png"), (174, 55)),
                    True, False),
            ]
    
    def animate(self):
        """Animate turtle images."""
        now = pygame.time.get_ticks()

        if now - self.last_update > 240:
            self.last_update = now
            self.current_frame += 1

            if self.current_frame >= len(self.turtle_frames):
                self.current_frame = 0
            
            self.image = self.turtle_frames[self.current_frame]
            self.rect = self.image.get_rect()

    def update(self):
        """Update log."""
        # animate turtles
        if self.lane == WATER_LANES[2]:
            self.animate()

        # if platform exits the screen, return it to original position
        if self.dir == 1 and self.rect.left > WIDTH:
            self.x = -(self.rect.width)
        if self.dir == -1 and self.rect.right < 0:
            self.x = WIDTH
        
        # move the platform by adding speed to its positions
        self.x += self.speed
        self.rect.x = self.x
        self.rect.centery = self.lane * TILESIZE