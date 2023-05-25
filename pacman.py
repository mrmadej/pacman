import pygame, os
from board import *
import math
import logging
import sys

pygame.init()

window_open = True
# wymiary okna
WIDTH = 900
HEIGHT = 950 + 24
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
for i in range (1, 5):
    pacman_images.append(pygame.transform.scale(pygame.image.load(os.path.join(current_dir, f'{i}.png')).convert_alpha(), (45, 45)))

level = boards

color = 'blue'


counter = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y) -> None:
        super().__init__()
        self.image = pacman_images[0]
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.score = 0
        self.powerup = False
        self.lifes = 3

        # Prawo, dół, lewo, góra
        self.possible_turns = [True, True, True, True]
        # 0 - prawo
        # 1 - dół
        # 2 - lewo
        # 3 - góra
        self.current_rotation = PRAWO
        
    def _get_event(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.current_rotation = LEWO
            if self.possible_turns[LEWO] == True:
                self.rect.move_ip([-2, 0])
        if key_pressed[pygame.K_RIGHT]:
            self.current_rotation = PRAWO
            if self.possible_turns[PRAWO] == True:
                self.rect.move_ip([2, 0])
        if key_pressed[pygame.K_UP]:
            self.current_rotation = GORA
            if self.possible_turns[GORA] == True:
                self.rect.move_ip([0, -2])
        if key_pressed[pygame.K_DOWN]:
            self.current_rotation = DOL
            if self.possible_turns[DOL] == True:
                self.rect.move_ip([0, 2])
    
    def eating(self):
        CENTER_X = self.rect.x + CENTER_X_PLAYER
        CENTER_Y = self.rect.y + CENTER_Y_PLAYER
        position = level[CENTER_Y // TILE_Y_LEN][CENTER_X // TILE_X_LEN]
        if position == 1 or position == 2:
            level[CENTER_Y // TILE_Y_LEN][CENTER_X // TILE_X_LEN] = 0
            if position == 1:
                self.score += 10
            elif position == 2:
                self.score += 50
                self.powerup = True
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
    def position(self):
        self.possible_turns = [False, False, False, False]
        # 0 - prawo
        # 1 - dół
        # 2 - lewo
        # 3 - góra
        CENTER_X = self.rect.x + CENTER_X_PLAYER
        CENTER_Y = self.rect.y + CENTER_Y_PLAYER

        # PLUS_MINUS_NUM = 15

        if self.current_rotation == PRAWO:
            if level[CENTER_Y // TILE_Y_LEN][(CENTER_X + (TILE_X_LEN // 2)) // TILE_X_LEN] < 3:
                self.possible_turns[PRAWO] = True
        
        if self.current_rotation == LEWO:
            if level[CENTER_Y // TILE_Y_LEN][(CENTER_X - (TILE_X_LEN // 2)) // TILE_X_LEN] < 3:
                self.possible_turns[LEWO] = True

        if self.current_rotation == GORA:
            if level[(CENTER_Y - (TILE_Y_LEN // 2)) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                self.possible_turns[GORA] = True

        if self.current_rotation == DOL:
            if level[(CENTER_Y + (TILE_Y_LEN // 2)) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                self.possible_turns[DOL] = True


    def testing_position(self):
        print("Piksel_x: " + str(self.rect.x + CENTER_X_PLAYER) + "; Piksel_y: " + str(self.rect.y + CENTER_Y_PLAYER) + "; Level_x: " + str((self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33)) + "; Level_y: " + str((self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30)) + "; Level[x][y]: " + str(level[((self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33))][((self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30))]) + "\n")
    def update(self, key_pressed):
        self.testing_position()
        self.position()
        self.eating()
        self._get_event(key_pressed)
        self.animation()
        pygame.draw.circle(screen, 'white', (self.rect.x + CENTER_X_PLAYER, self.rect.y + CENTER_Y_PLAYER), 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HUD:
    def __init__(self, score: int, lifes: int,) -> None:
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
    
    def draw(self):
        screen.blit(self.text_render, self.text_rect)
    def update(self, score: int, lifes: int):
        self.score = score
        self.lifes = lifes
        self.text_render = self.font.render(("Score: " + str(score)), True, self.font_color, None)

def draw_board():
    num1 = ((HEIGHT - 50) // 33)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            pygame.draw.polygon(screen, 'red', ((j * num2, i * num1), (j * num2, (i+1) * num1), ((j - 1) * num2, (i+1) * num1), ((j - 1) * num2, i * num1)), 2)
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


#konkretyzacja obiektów
player = Player(PLAYER_X, PLAYER_Y)
hud = HUD(0, 3)

screen.fill((0, 0, 0))
is_game_running = False

clock = pygame.time.Clock()

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
                is_game_running = True

    if counter < 19:
        counter += 1
    else:
        counter = 0
    
    screen.fill((0, 0, 0))  # Czyszczenie ekranu
    
    # Rysowanie na ekranie
    screen.blit(background_image, (90.5, 0))  # Wyświetlanie obrazka tła
    screen.blit(button_image, button_rect)  # Wyświetlanie obrazka na przycisku


    if is_game_running:
        # Renderowanie planszy gry

        # Ustawienie koloru tła na czarny
        screen.fill((0, 0, 0))
        # Rysowanie planszy
        draw_board()
        hud.draw()
        player.draw(screen)
        key_pressed = pygame.key.get_pressed()
        player.update(key_pressed)
        

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)


pygame.quit()