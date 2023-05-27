import math
import os

WIDTH = 900
HEIGHT = 950 + 24
PRAWO = 0
DOL = 1
LEWO = 2
GORA = 3
POWERUP_TIME = 10
TILE_Y_LEN = ((HEIGHT - 50) // 33)
TILE_X_LEN = (WIDTH // 30)
CENTER_X_PLAYER = 23
CENTER_Y_PLAYER = 24
PLAYER_X = 442
PLAYER_Y = 662
PI = math.pi
# Ustalenie ścieżki do obrazka
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.join(current_dir, 'Pacman_images') 
image_path = os.path.join(current_dir, 'Menu_background.jpg')
pacman_images = []