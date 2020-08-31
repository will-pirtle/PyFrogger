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
WATER_LANES = [5.5, 4.5, 3.5, 2.5]
ROAD_LANES = [10.5, 9.5, 8.5, 7.5]
LANE_DIRS = {
    2.5: 1,
    3.5: -1,
    4.5: 1,
    5.5: 1,
    7.5: -1,
    8.5: 1,
    9.5: -1,
    10.5: 1,
}

# car settings
CAR_SPEED = {
    7.5: 1.5,
    8.5: 2.5,
    9.5: 1,
    10.5: 1,
}
CARS_PER_LANE = {
    7.5: 2,
    8.5: 1,
    9.5: 2,
    10.5: 2,
}

# platform settings
PLATFORM_SPEED = {
    2.5: 1.5,
    3.5: 2,
    4.5: 2,
    5.5: 1,
}
PLATFORMS_PER_LANE = {
    2.5: 2,
    3.5: 2,
    4.5: 1,
    5.5: 3,
}