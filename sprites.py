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
        self.moving = False
        self.facing_up = True
        self.facing_down = False
        self.facing_right = False
        self.facing_left = False

        # animation variables
        self.current_frame = 0
        self.last_update = 0

        # load the initial image of frogger
        self.load_images()
        self.image = self.up_frames[0]
        self.rect = self.image.get_rect()

        # starting position (bottom middle of screen)
        self.x = 5
        self.y = 11

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
                                self.game.spritesheet.get_image(173, 9, 53, 64),
                                (49, 59)),
                            pygame.transform.scale(
                                self.game.spritesheet.get_image(230, 2, 54, 73),
                                (50, 68)),
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

    def move_left(self):
        """Move Frogger one tile left"""
        self.x += -1

        # frogger faces left
        self.facing_up = False
        self.facing_down = False
        self.facing_right = False
        self.facing_left = True

    def move_right(self):
        """Move Frogger one tile right."""
        self.x += 1

        # frogger facing right
        self.facing_up = False
        self.facing_down = False
        self.facing_right = True
        self.facing_left = False

    def move_up(self):
        """Move Frogger one tile up."""
        self.y += -1

        # frogger facing up
        self.facing_up = True
        self.facing_down = False
        self.facing_right = False
        self.facing_left = False

    def move_down(self):
        """Move Frogger one tile down."""
        self.y += 1
        
        # frogger facing down
        self.facing_up = False
        self.facing_down = True
        self.facing_right = False
        self.facing_left = False

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
                if self.facing_up:
                    self.image = self.up_frames[self.current_frame]
                if self.facing_down:
                    self.image = self.down_frames[self.current_frame]
                if self.facing_right:
                    self.image = self.right_frames[self.current_frame]
                if self.facing_left:
                    self.image = self.left_frames[self.current_frame]
                self.rect = self.image.get_rect()
        else:
            # keep image facing direction of last movement
            if self.facing_down:
                self.image = self.down_frames[0]
            if self.facing_up:
                self.image = self.up_frames[0]
            if self.facing_right:
                self.image = self.right_frames[0]
            if self.facing_left:
                self.image = self.left_frames[0]
            self.rect = self.image.get_rect()

    def in_bushes(self):
        """Frogger is in the top row of screen (whether in home or not)"""
        if self.rect.y < 1.5 * TILESIZE:
            return True
        else:
            return False

    def reset_pos(self):
        """Return frogger back to starting position."""
        self.image = self.up_frames[0]

        self.x = 5
        self.y = 11

    def update(self):
        """Update the player."""
        self.animate()

        self.rect.centerx = self.x * TILESIZE + 0.5 * TILESIZE
        self.rect.centery = self.y * TILESIZE + 0.5 * TILESIZE


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
        # set the direction of the car based on which lane it's in
        self.dir = LANE_DIRS[self.lane]

        # set the image of the car
        self.image = pygame.transform.scale(
            self.game.spritesheet.get_image(13, 485, 125, 65), (77, 40))
        # flip if moving left
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        # Set start position based on direction
        #   if moving right start left of screen
        #   if moving left start right of screen
        if self.dir == 1:
            self.rect.centerx = -1 * TILESIZE
        else:
            self.rect.centerx = (WIDTH + 1) * TILESIZE      
        self.rect.centery = self.lane * TILESIZE

        # car's speed is multiplied by the dir (+1 for right, -1 for left)
        self.speed = CAR_SPEED[lane] * self.dir

    def update(self):
        """Update car."""
        # move the car by adding speed to its positions
        self.rect.x += self.speed

        # if car exits the screen, return it to original position
        if self.dir == 1 and self.rect.left > WIDTH:
            self.rect.centerx = -1 * TILESIZE
        if self.dir == -1 and self.rect.right < 0:
            self.rect.centerx = WIDTH + TILESIZE


class Log(pygame.sprite.Sprite):
    """Class to manage logs."""
    
    def __init__(self, game):
        """Initialize log attributes."""
        self.groups = game.all_sprites, game.logs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.type = 'md'

        self.load_images()
        self.image = self.log_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.rect.centerx = 0 - self.rect.width / 2
        self.rect.centery = LOG_LANES[0]

    def load_images(self):
        """Load images for different types of logs."""
        self.sm_img = pygame.transform.scale(
            self.game.spritesheet.get_image(388, 258, 183, 58), (164, 52))
        self.md_img = pygame.transform.scale(
            self.game.spritesheet.get_image(15, 328, 270, 58), (242, 52))
        self.log_imgs = {'sm': self.sm_img, 'md': self.md_img}

    def update(self):
        """Update log."""
        self.rect.x += 2
        if self.rect.left > WIDTH:
            self.rect.centerx = 0 - self.rect.width / 2
