import pygame

# Define colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
TITLE = 'FROGGER'
WIDTH = 660
HEIGHT = 780
FPS = 60
BGCOLOR = BLACK

SPRITESHEET = "graphics-game-sprites.png"

TILESIZE = 60
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# home settings
HOME_LOCATIONS = [1.5, 3.5, 5.5, 7.5, 9.5]

# define lanes
LANE_1 = 2.5
LOG_LANES = [2.5, 4.5, 5.5]
TURTLE_LANES = [3.5]
ROAD_LANES = [7.5, 8.5, 9.5, 10.5]

# car settings
CAR_SPEED = 2

