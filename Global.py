import math
import os
import pygame
import random
import copy

pygame.mixer.init()
pygame.init()

# Board dimensions
NUM_ROWS = 33
NUM_COLS = 30

# Step of player and ghosts
STEP = 2

# Margin for HUD panel
MARGIN = 50

# Window Dimensions in Pixels
WIDTH = 900
HEIGHT = 924 + MARGIN  # 900 + 50 + 24

PI = math.pi

# opening window
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pacman")

# Center of pacman and ghosts images
# Add this to current position to know coordinates of the center
CENTER_X_PLAYER = 23
CENTER_Y_PLAYER = 24

# starting posiion of player
PLAYER_X = 442
PLAYER_Y = 662

# Directions
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

# Dimensions of one tile
TILE_Y_LEN = ((HEIGHT - MARGIN) // 33)
TILE_X_LEN = (WIDTH // 30)

# During this time Pacman can eat ghosts
POWERUP_TIME = 10

# Eaten ghost must go to this position and then enter the cage
# This position is in front of the cage
EATEN_MODE_TARGET_X = 14 * TILE_X_LEN + TILE_X_LEN // 2
EATEN_MODE_TARGET_Y = 12 * TILE_Y_LEN + TILE_Y_LEN // 2

# Modes of ghosts
CHASE_MODE = 0
SCATTER_MODE = 1
FRIGHTEN_MODE = 2
EATEN_MODE = 3
EXIT_CAGE = 4

# Ghosts id
BLINKY = 0
INKY = 1
PINKY = 2
CLYDE = 3

# Modes of game, tells program what to display
STARTING_PANEL = 0
RUNNING_GAME = 1
ENDING_PANEL = 2

# Path to the current directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Font and color
FONT = os.path.join(CURRENT_DIR, 'font\OptimusPrinceps.ttf')
FONT_COLOR = (79, 0, 1)
COLOR_BOARD = 'blue'

# Soundtrack
START_SOUND = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound\start.wav'))
EATING_SOUND = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound\eating.wav'))
PACMAN_DEATH_SOUND = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound\pacman_death.wav'))
PACMAN_EATGHOST_SOUND = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound\pacman_eatghost.wav'))
PACMAN_WIN_SOUND = pygame.mixer.Sound(os.path.join(CURRENT_DIR, 'sound\pacman_win.wav'))

# Ghost images
IMAGE_GHOST_BLUE = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, 'images\\blue.png')).convert_alpha(),
                                          (45, 45))
IMAGE_GHOST_RED = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, 'images\\red.png')).convert_alpha(),
                                         (45, 45))
IMAGE_GHOST_PINK = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, 'images\pink.png')).convert_alpha(),
                                          (45, 45))
IMAGE_GHOST_ORANGE = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, 'images\orange.png')).convert_alpha(),
                                            (45, 45))

IMAGE_GHOST_DEAD = pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, 'images\dead.png')).convert_alpha(),
                                          (45, 45))
IMAGE_GHOST_POWERUP = pygame.transform.scale(
    pygame.image.load(os.path.join(CURRENT_DIR, 'images\powerup.png')).convert_alpha(), (45, 45))

# Starting panel image
STARTING_IMAGE = pygame.image.load(os.path.join(CURRENT_DIR, 'images\Menu_background.jpg')).convert()

# Images of pacman
# Used for animation
pacman_images = []
for i in range(1, 5):
    pacman_images.append(
        pygame.transform.scale(pygame.image.load(os.path.join(CURRENT_DIR, f'images\{i}.png')).convert_alpha(), (45, 45)))