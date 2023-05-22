import pygame, os
from board import *
import math

pygame.init()

window_open = True
# wymiary okna
WIDTH = 900
HEIGHT = 950
PI = math.pi
PLAYER_X = 450
PLAYER_Y = 663
CENTER_X_PLAYER = 23
CENTER_Y_PLAYER = 24
PRAWO = 0
DOL = 1
LEWO = 2
GORA = 3


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
        # Prawo, dół, lewo, góra
        self.possible_turns = [False, False, False, False]
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
        CENTER_Y = self.rect.y - CENTER_Y_PLAYER
        TILE_Y_LEN = ((HEIGHT - 50) // 32)
        TILE_X_LEN = (WIDTH // 30)
        PLUS_MINUS_NUM = 15
        if CENTER_X // 30 < 29:
            if self.current_rotation == PRAWO:
                if level[CENTER_Y // TILE_Y_LEN][(CENTER_X - PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                    self.possible_turns[PRAWO] = True
            
            if self.current_rotation == LEWO:
                if level[CENTER_Y // TILE_Y_LEN][(CENTER_X + PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                    self.possible_turns[LEWO] = True
            
            if self.current_rotation == GORA:
                if level[(CENTER_Y + PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                    self.possible_turns[GORA] = True
            
            if self.current_rotation == DOL:
                if level[(CENTER_Y - PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                    self.possible_turns[DOL] = True


            if self.current_rotation == GORA or self.current_rotation == DOL:
                if 12 <= CENTER_X % TILE_X_LEN <= 18:
                    if level[(CENTER_Y + PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                        self.possible_turns[DOL] = True
                    if level[(CENTER_Y - PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                        self.possible_turns[GORA] = True
                if 12 <= CENTER_Y % TILE_Y_LEN <= 18:
                    if level[CENTER_Y // TILE_Y_LEN][(CENTER_X - TILE_X_LEN) // TILE_X_LEN] < 3:
                        self.possible_turns[LEWO] = True
                    if level[CENTER_Y // TILE_Y_LEN][(CENTER_X + TILE_X_LEN) // TILE_X_LEN] < 3:
                        self.possible_turns[PRAWO] = True
            
            if self.current_rotation == PRAWO or self.current_rotation == LEWO:
                if 12 <= CENTER_Y % TILE_X_LEN <= 18:
                    if level[(CENTER_Y + TILE_Y_LEN) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                        self.possible_turns[DOL] = True
                    if level[(CENTER_Y - TILE_Y_LEN) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                        self.possible_turns[GORA] = True
                if 12 <= CENTER_Y % TILE_Y_LEN <= 18:
                    if level[CENTER_Y // TILE_Y_LEN][(CENTER_X - PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                        self.possible_turns[LEWO] = True
                    if level[CENTER_Y // TILE_Y_LEN][(CENTER_X + PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                        self.possible_turns[PRAWO] = True
        else:
            self.possible_turns[PRAWO] = True
            self.possible_turns[LEWO] = True

    def update(self, key_pressed):
        self.position()
        self._get_event(key_pressed)
        self.animation()
        # pygame.draw.circle(screen, 'white', (self.rect.x + CENTER_X_PLAYER, self.rect.y + CENTER_Y_PLAYER), 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
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


player = Player(PLAYER_X, PLAYER_Y)

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
        player.draw(screen)
        key_pressed = pygame.key.get_pressed()
        player.update(key_pressed)
        

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)


pygame.quit()