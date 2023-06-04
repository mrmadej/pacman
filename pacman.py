import pygame, os
from board import *
import math
import logging
import sys
import threading
import random

pygame.init()

window_open = True
# wymiary okna
NUM_ROWS = 33
NUM_COLS = 30
STEP = 2
MARGIN = 50
WIDTH = 900
HEIGHT = 924 + MARGIN  # 900 + 50 + 24


PI = math.pi
CENTER_X_PLAYER = 23
CENTER_Y_PLAYER = 24
PLAYER_X = 442
PLAYER_Y = 662
PRAWO = 0
DOL = 1
LEWO = 2
GORA = 3
TILE_Y_LEN = ((HEIGHT - 50) // 33)
TILE_X_LEN = (WIDTH // 30)
POWERUP_TIME = 10
EATEN_MODE_TARGET_X = 14 * TILE_X_LEN + TILE_X_LEN // 2
EATEN_MODE_TARGET_Y = 12 * TILE_Y_LEN + TILE_Y_LEN // 2
CHASE_MODE = 0
SCATTER_MODE = 1
FRIGHTEN_MODE = 2
EATEN_MODE = 3
EXIT_CAGE = 4
BLINKY = 0
INKY = 1
PINKY = 2
CLYDE = 3


# Ustalenie ścieżki do obrazka
current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.join(current_dir, 'Pacman_images')
image_path = os.path.join(current_dir, 'Menu_background.jpg')

# otwieranie okienka
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# To się wyświetla na górze jako nazwa programu
pygame.display.set_caption("Pacman")

# podkłada grafikę do tła i przycisku
background_image = pygame.image.load(image_path).convert()
image_path = os.path.join(current_dir, 'Start_button.png')
button_image = pygame.image.load(image_path).convert()

# Ustalenie pozycji przycisku
button_x = 281.5
button_y = 500
button_width = 337
button_height = 130

# Utworzenie przycisku
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# obrazki pacmana załadowane do tablicy
# z tego będą animacje
pacman_images = []
for i in range(1, 5):
    pacman_images.append(
        pygame.transform.scale(pygame.image.load(os.path.join(current_dir, f'{i}.png')).convert_alpha(), (45, 45)))



color = 'blue'

counter = 0


class Collision:
    def __init__(self) -> None:
        # Prawo, dół, lewo, góra
        self.rect = None
        self.possible_turns = [False, False, False, False]
        self.PLUS_MINUS_NUM = 2

    def position(self):
        self.possible_turns = [False, False, False, False]
        # 0 - prawo
        # 1 - dół
        # 2 - lewo
        # 3 - góra

        # center_x , center_y coordinates of center of element
        center_x = self.rect.x + CENTER_X_PLAYER
        center_y = self.rect.y + CENTER_Y_PLAYER

        # try to calculate square coordinates
        square_x = center_x // TILE_X_LEN
        square_y = center_y // TILE_Y_LEN

        x_offset = center_x % TILE_X_LEN
        y_offset = center_y % TILE_Y_LEN

        print("Square: " + str(square_x) + " " + str(square_y))

        if level.board[square_y][(square_x + 1) % NUM_COLS] < 3 or x_offset < (TILE_X_LEN // 2):
            self.possible_turns[PRAWO] = True

        if level.board[square_y][(square_x - 1)% NUM_COLS] < 3 or x_offset > (TILE_X_LEN // 2):
            self.possible_turns[LEWO] = True

        if level.board[square_y - 1][square_x % NUM_COLS] < 3 or y_offset > (TILE_Y_LEN // 2):
            self.possible_turns[GORA] = True

        if level.board[(square_y + 1) % NUM_ROWS][square_x % NUM_COLS] < 3 or y_offset < (TILE_Y_LEN // 2):
            self.possible_turns[DOL] = True


class Player(Collision):
    def __init__(self, player_x: int, player_y: int, image: pygame.Surface) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.score = 0
        self.powerup = False
        self.lifes = 3
        self.current_rotation = PRAWO
        self.start_x = player_x
        self.start_y = player_y

    def time(self):
        timer = threading.Timer(POWERUP_TIME, self.powerUp)
        timer.start()
        print ("Timer started player")

    def powerUp(self):
        self.powerup = False
        print ("Timer expired player")

    def _get_event(self, key_pressed):

        self.position()
        # need fit to grid horizontal if running up or down or vertical if running left or right
        center_x = self.rect.x + CENTER_X_PLAYER
        center_y = self.rect.y + CENTER_Y_PLAYER
        x_offset = center_x % TILE_X_LEN
        y_offset = center_y % TILE_Y_LEN
        move_x = - (x_offset - TILE_X_LEN // 2)
        move_y = - (y_offset - TILE_Y_LEN // 2)

        if key_pressed[pygame.K_LEFT]:
            if self.possible_turns[LEWO]:
                self.current_rotation = LEWO
                if center_x > STEP:
                    self.rect.move_ip([-STEP, move_y])
                else:
                    self.rect.move_ip([WIDTH - STEP, move_y])
        if key_pressed[pygame.K_RIGHT]:
            if self.possible_turns[PRAWO]:
                self.current_rotation = PRAWO
                if center_x < WIDTH - STEP:
                    self.rect.move_ip([STEP, move_y])
                else:
                    self.rect.move_ip([-WIDTH, move_y])
        if key_pressed[pygame.K_UP]:
            if self.possible_turns[GORA]:
                self.current_rotation = GORA
                if center_y > STEP:
                    self.rect.move_ip([move_x, -STEP])
                else:
                    self.rect.move_ip([move_x, HEIGHT - MARGIN - STEP - 1])
        if key_pressed[pygame.K_DOWN]:
            if self.possible_turns[DOL]:
                self.current_rotation = DOL
                if center_y < HEIGHT - MARGIN - STEP:
                    self.rect.move_ip([move_x, STEP])
                else:
                    self.rect.move_ip([move_x, -HEIGHT + MARGIN])

    def eating(self):
        CENTER_X = self.rect.x + CENTER_X_PLAYER
        CENTER_Y = self.rect.y + CENTER_Y_PLAYER
        position = level.board[CENTER_Y // TILE_Y_LEN][CENTER_X // TILE_X_LEN]
        if position == 1 or position == 2:
            level.board[CENTER_Y // TILE_Y_LEN][CENTER_X // TILE_X_LEN] = 0
            if position == 1:
                self.score += 10
            elif position == 2:
                self.score += 50
                self.powerup = True
                self.time()
        hud.update(self.score, self.lifes)

    def animation(self):
        if self.current_rotation == PRAWO:
            self.image = pacman_images[counter // 5]
        elif self.current_rotation == DOL:
            self.image = pygame.transform.rotate(pacman_images[counter // 5], -90)
        elif self.current_rotation == LEWO:
            self.image = pygame.transform.rotate(pacman_images[counter // 5], 180)
        elif self.current_rotation == GORA:
            self.image = pygame.transform.rotate(pacman_images[counter // 5], 90)

    def testing_position(self):
        print("Piksel_x: " + str(self.rect.x + CENTER_X_PLAYER) + "; Piksel_y: " + str(
            self.rect.y + CENTER_Y_PLAYER) + "; Level_x: " + str(
            (self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33)) + "; Level_y: " + str(
            (self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30)) + "; Level[x][y]: " + str(
            level.board[((self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33))][
                ((self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30))]) + "\n")
        # print("Powerup: " + str(self.powerup))

    def update(self, key_pressed):
        # self.testing_position()
        self.eating()
        self._get_event(key_pressed)
        self.animation()
        pygame.draw.circle(screen, 'white', (self.rect.x + CENTER_X_PLAYER, self.rect.y + CENTER_Y_PLAYER), 2)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)


class HUD:
    def __init__(self, score: int, lifes: int, ) -> None:
        self.score = score
        self.lifes = lifes
        # Ustawienia tekstu
        self.font_size = 32
        self.font_color = (255, 255, 255)  # Biały kolor tekstu
        self.font = pygame.font.Font(None, self.font_size)
        self.text_render = self.font.render(("Score: " + str(score)), True, self.font_color, None)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.x = 30
        self.text_rect.y = 934
        # życia
        self.image = pacman_images[0]
        self.lifes_rect = self.image.get_rect()
        self.lifes_rect.x = WIDTH - 30 - CENTER_X_PLAYER
        self.lifes_rect.y = self.text_rect.y - CENTER_Y_PLAYER

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text_render, self.text_rect)
        for i in range(self.lifes):
            screen.blit(self.image, (self.lifes_rect.x - i * 60, self.lifes_rect.y))

    def update(self, score: int, lifes: int):
        self.score = score
        self.lifes = lifes
        self.text_render = self.font.render(("Score: " + str(score)), True, self.font_color, None)


class Ghost(Collision):
    def __init__(self, image: pygame.Surface, x: int, y: int, scatter_target_x: int, scatter_target_y: int, name: int, points: int) -> None:
        super().__init__()
        self.image = image
        self.ghost_name = name
        self.image_storage = image
        self.rect = self.image.get_rect()
        self.start_x = x
        self.start_y = y
        self.rect.x = x
        self.rect.y = y
        self.scatter_target_x = scatter_target_x
        self.scatter_target_y = scatter_target_y
        self.last_move = 0
        # prawo, dół, lewo, góra
        self.directionImportance = [0, 1, 2, 3]
        self.frighten_mode_first = True
        self.eaten = True
        self.current_mode = -1
        self.timer = None
        self.entered_scatter_mode = False
        self.points = points
    
    def killing_pacman(self):
        ghost_center_x = (self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN
        ghost_center_y = (self.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN
        pacman_center_x = (player.rect.x + CENTER_X_PLAYER) // TILE_X_LEN
        pacman_center_y = (player.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN
        if ghost_center_x == pacman_center_x and ghost_center_y == pacman_center_y and self.current_mode != FRIGHTEN_MODE:
            player.lifes -= 1
            level.start()

    def is_in_cage(self) -> bool:
        x = (self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN >= 12 and (self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN <= 17
        y = (self.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN >= 13 and (self.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN <= 16
        cage = x and y
        front_cage_x = (self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN >= 14 and (self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN <= 15
        front_cage_y = (self.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN == 12
        front_cage = front_cage_x and front_cage_y
        return cage or front_cage

    def start_timer(self, duration, callback):
        print ("Timer start ghost")
        self.stop_timer()  # Zatrzymujemy poprzedni timer, jeśli istnieje
        self.timer = threading.Timer(duration, lambda: self.timer_callback(mode = callback))
        #self.timer = threading.Timer(duration, self.change_mode(callback))
        self.timer.start()
    
    def stop_timer(self):        
        if self.timer and self.timer.is_alive():
            print ("Timer stop ghost")
            self.timer.cancel()

    def timer_callback(self,mode):
        print("Timer ghost expired"+str(mode)+"\n")
        self.current_mode=mode

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self, direction: int):
        self.last_move = direction

        # need fit to grid horizontal if running up or down or vertical if running left or right
        center_x = self.rect.x + CENTER_X_PLAYER
        center_y = self.rect.y + CENTER_Y_PLAYER
        x_offset = center_x % TILE_X_LEN
        y_offset = center_y % TILE_Y_LEN
        move_x = - (x_offset - TILE_X_LEN // 2)
        move_y = - (y_offset - TILE_Y_LEN // 2)

        if direction == PRAWO:
            if center_x < WIDTH - STEP:
                self.rect.move_ip([STEP, move_y])
            else:
                self.rect.move_ip([-WIDTH, move_y])            
        if direction == LEWO:
            if center_x > STEP:
                self.rect.move_ip([-STEP, move_y])
            else:
                self.rect.move_ip([WIDTH - STEP, move_y])            
        if direction == GORA:
            if center_y > STEP:
                self.rect.move_ip([move_x, -STEP])
            else:
                self.rect.move_ip([move_x, HEIGHT - MARGIN - STEP - 1])            
        if direction == DOL:
            if center_y < HEIGHT - MARGIN - STEP:
                self.rect.move_ip([move_x, STEP])
            else:
                self.rect.move_ip([move_x, -HEIGHT + MARGIN])


    def change_mode(self, mode = None):        
        if mode is not None:
            self.current_mode = mode

        if self.current_mode != FRIGHTEN_MODE and self.current_mode != EATEN_MODE and player.powerup == True and not self.is_in_cage():
            self.image = IMAGE_GHOST_POWERUP
            self.frighten_mode_first = True
            self.current_mode = FRIGHTEN_MODE
            self.start_timer(POWERUP_TIME, SCATTER_MODE)

        if self.current_mode == CHASE_MODE:
            self.chase_mode()
        elif self.current_mode == SCATTER_MODE:
            self.scatter_mode()
        elif self.current_mode == FRIGHTEN_MODE:
            self.frighten_mode()
        elif self.current_mode == EATEN_MODE:
            self.eaten_mode()
        elif self.current_mode == EXIT_CAGE:        
            self.exit_cage()

    def chase_mode(self):
        self.image = self.image_storage
        if self.timer and not self.timer.is_alive():
            duration = random.randint(5, 15)
            self.start_timer(duration, SCATTER_MODE)
        palyer_center_x = player.rect.x + CENTER_X_PLAYER
        palyer_center_y = player.rect.y + CENTER_Y_PLAYER
        if self.ghost_name == BLINKY:
            self.move(self.calculate_distance(palyer_center_x, palyer_center_y))
        elif self.ghost_name == INKY:
            self.move(self.calculate_distance(pinky.rect.x + CENTER_X_PLAYER, pinky.rect.y + CENTER_Y_PLAYER))
        elif self.ghost_name == PINKY:
            direction = player.current_rotation
            if direction == PRAWO:
                self.move(self.calculate_distance(palyer_center_x + 2 * TILE_X_LEN, palyer_center_y))
            elif direction == LEWO:
                self.move(self.calculate_distance(palyer_center_x - 2 * TILE_X_LEN, palyer_center_y))    
            elif direction == GORA:
                self.move(self.calculate_distance(palyer_center_x, palyer_center_y - 2 * TILE_Y_LEN))
            elif direction == DOL:
                self.move(self.calculate_distance(palyer_center_x, palyer_center_y + 2 * TILE_Y_LEN))
        elif self.ghost_name == CLYDE:
            warunek = abs(((self.rect.x + CENTER_X_PLAYER) // TILE_X_LEN) + ((self.rect.y + CENTER_Y_PLAYER) // TILE_Y_LEN) - palyer_center_x // TILE_X_LEN - palyer_center_y // TILE_Y_LEN)
            if  warunek > 8:
                self.move(self.calculate_distance(palyer_center_x, palyer_center_y))
            else:
                self.move(self.calculate_distance(self.scatter_target_x, self.scatter_target_y))
    def scatter_mode(self):
        self.image = self.image_storage
        if self.timer and not self.timer.is_alive():
            duration = random.randint(5, 15)
            self.start_timer(duration, CHASE_MODE)
        self.move(self.calculate_distance(self.scatter_target_x, self.scatter_target_y))
    def exit_cage(self):
        if self.rect.x + CENTER_X_PLAYER == EATEN_MODE_TARGET_X and self.rect.y + CENTER_Y_PLAYER == EATEN_MODE_TARGET_Y:
            self.eaten = False
            self.current_mode = CHASE_MODE
            duration = random.randint(5, 15)
            self.start_timer(duration, SCATTER_MODE)
        else:
            self.move(self.calculate_distance(EATEN_MODE_TARGET_X, EATEN_MODE_TARGET_Y))
    def eaten_mode(self): # POPRAWIC
        self.stop_timer()
        if self.eaten == False:
            self.eaten = True
            self.image = IMAGE_GHOST_DEAD
            self.frighten_mode_first = False
            #testing
        if self.rect.x + CENTER_X_PLAYER == self.start_x + CENTER_X_PLAYER and self.rect.y + CENTER_Y_PLAYER == self.start_y + CENTER_Y_PLAYER:
            self.last_move = -1
            self.image = self.image_storage
            self.current_mode = EXIT_CAGE
            #self.change_mode()
        else:
            # 375, 434
            self.move(self.calculate_distance(self.start_x + CENTER_X_PLAYER, self.start_y + CENTER_Y_PLAYER))
        

    def frighten_mode(self):
        # self.rect.x + CENTER_X_PLAYER == player.rect.x + CENTER_X_PLAYER and self.rect.y + CENTER_Y_PLAYER == player.rect.y + CENTER_Y_PLAYER

        ghost_center_x = self.rect.x + CENTER_X_PLAYER
        ghost_center_y = self.rect.y + CENTER_Y_PLAYER
        
        pacman_center_x = player.rect.x + CENTER_X_PLAYER
        pacman_center_y = player.rect.y + CENTER_Y_PLAYER


        if (ghost_center_x // TILE_X_LEN == pacman_center_x // TILE_X_LEN) and (ghost_center_y // TILE_Y_LEN == pacman_center_y // TILE_Y_LEN):
            print("Kolizja z duchem")
            self.stop_timer()
            self.current_mode = EATEN_MODE
            player.score += self.points
            # self.eaten = True
        if self.frighten_mode_first:
            self.frighten_mode_first = False
            if self.last_move == 1:
                self.last_move = 3
            else:
                self.last_move = (self.last_move + 2) % 4
        i = 0
        for n in range(len(self.possible_turns)):
            if self.possible_turns[n]:
                if (n - self.last_move) % 4 == 2:
                    self.possible_turns[n] = False
        next_direction = self.last_move
        if self.center_check():
            next_direction = random.randint(0, 3)
            while self.possible_turns[next_direction] == False:
                next_direction = random.randint(0, 3)
        self.move(next_direction)


    def calculate_distance(self, target_x, target_y):

        ghost_center_x = self.rect.x + CENTER_X_PLAYER
        ghost_center_y = self.rect.y + CENTER_Y_PLAYER
                

        if self.eaten == True:
            if level.board[(ghost_center_y // TILE_Y_LEN) + 1][(ghost_center_x // TILE_X_LEN)] == 9:
                self.possible_turns[DOL] = True
            if level.board[(ghost_center_y // TILE_Y_LEN) - 1][(ghost_center_x // TILE_X_LEN)] == 9:
                self.possible_turns[GORA] = True
        next_direction = self.last_move
        distance = dict()
        last_distance = -1
        i = 0
        if self.center_check():
            for direction in self.possible_turns:
                if direction:
                    # sprawdzanie czy stąd nie przyszedł
                    if (i - self.last_move) % 4 != 2:
                        move_x = 0
                        move_y = 0
                        # 0 - prawo
                        # 1 - dół
                        # 2 - lewo
                        # 3 - góra
                        match i:
                            case 0:
                                move_x = 2
                            case 1:
                                move_y = 2
                            case 2:
                                move_x = -2
                            case 3:
                                move_y = -2
                        distance[i] = math.sqrt(abs(target_x - self.rect.x - move_x) ** 2 + abs(
                            target_y - self.rect.y - move_y) ** 2)
                i += 1
            for direction, dist in distance.items():
                if last_distance == -1:
                    last_distance = dist
                    next_direction = direction
                else:
                    if last_distance > dist:
                        last_distance = dist
                        next_direction = direction
                    elif last_distance == dist:
                        if self.directionImportance[next_direction] < direction:
                            last_distance = dist
                            next_direction = direction
        return next_direction
    


    def update(self):
        self.position()
        #self.scatter_mode()
        #self.frighten_mode()
        #self.eaten_mode()
        #self.chase_mode()
        self.killing_pacman()
        self.change_mode()

    def center_check(self) -> bool:

        return (self.rect.x + CENTER_X_PLAYER) % TILE_X_LEN == TILE_X_LEN // 2  and (self.rect.y + CENTER_Y_PLAYER) % TILE_Y_LEN == TILE_Y_LEN // 2


class Level:
    def __init__(self, board, characters) -> None:
        self.board = board
        # [player, clyde, blinky, inky, pinky]
        self.characters = characters
        self.is_game_running = False
    def draw_board(self):
        num1 = ((HEIGHT - 50) // 33)
        num2 = (WIDTH // 30)
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.polygon(screen, 'red', (
                    (j * num2, i * num1), (j * num2, (i + 1) * num1), ((j - 1) * num2, (i + 1) * num1),
                    ((j - 1) * num2, i * num1)), 2)
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                if self.board[i][j] == 3:
                    pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                    (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                if self.board[i][j] == 4:
                    pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                if self.board[i][j] == 5:
                    pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                    0, PI / 2, 3)
                if self.board[i][j] == 6:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
                if self.board[i][j] == 7:
                    pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == 8:
                    pygame.draw.arc(screen, color,
                                    [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                    (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
    def start(self):
        i = 0
        for character in self.characters:
            character.rect.x = character.start_x
            character.rect.y = character.start_y
            if i == 0:
                pass
            else:
                character.current_mode = -1
                character.start_timer(5 * i, EXIT_CAGE)
            i += 1
    
    def win(self):
        warunek1 = not any(1 in row for row in self.board)
        warunek2 = not any(2 in row for row in self.board)
        if warunek1 and warunek2:
            self.is_game_running = False


image_ghost_blue = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'blue.png')).convert_alpha(), (45, 45))
image_ghost_red = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'red.png')).convert_alpha(), (45, 45))
image_ghost_pink = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'pink.png')).convert_alpha(), (45, 45))
image_ghost_orange = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'orange.png')).convert_alpha(), (45, 45))
IMAGE_GHOST_DEAD = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'dead.png')).convert_alpha(), (45, 45))
IMAGE_GHOST_POWERUP = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, 'powerup.png')).convert_alpha(), (45, 45))

# konkretyzacja obiektów
player = Player(PLAYER_X, PLAYER_Y, pacman_images[0])
hud = HUD(0, 3)
blinky = Ghost(image_ghost_blue, 472, 410, 0, 0, BLINKY, 100)
inky = Ghost(image_ghost_orange,  412, 410, WIDTH, 0, INKY, 200)
pinky = Ghost(image_ghost_pink, 352, 410, WIDTH, HEIGHT, PINKY, 300)
clyde = Ghost(image_ghost_red, 412, 326, 0, HEIGHT, CLYDE, 400)
level = Level(boards, [player, clyde, blinky, inky, pinky])


screen.fill((0, 0, 0))


clock = pygame.time.Clock()

level.start()
while window_open:
    # wyłączanie gry
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        elif event.type == pygame.QUIT:
            window_open = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                level.is_game_running = True

    if counter < 19:
        counter += 1
    else:
        counter = 0

    screen.fill((0, 0, 0))  # Czyszczenie ekranu

    # Rysowanie na ekranie
    screen.blit(background_image, (90.5, 0))  # Wyświetlanie obrazka tła
    screen.blit(button_image, button_rect)  # Wyświetlanie obrazka na przycisku

    if level.is_game_running:
        # Renderowanie planszy gry
        level.win()
        # Ustawienie koloru tła na czarny
        screen.fill((0, 0, 0))
        # Rysowanie planszy
        level.draw_board()
        hud.draw(screen)
        player.draw(screen)
        blinky.draw(screen)
        pinky.draw(screen)
        inky.draw(screen)
        clyde.draw(screen)
        key_pressed = pygame.key.get_pressed()
        player.update(key_pressed)
        blinky.update()
        pinky.update()
        inky.update()
        clyde.update()

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)

pygame.quit()