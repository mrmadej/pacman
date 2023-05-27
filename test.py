import pygame, os
from board import *
import math
import logging
import sys
import threading
from Player import *
from Global import *

pygame.init()

window_open = True
# wymiary okna










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

for i in range (1, 5):
    pacman_images.append(pygame.transform.scale(pygame.image.load(os.path.join(current_dir, f'{i}.png')).convert_alpha(), (45, 45)))

level = boards

color = 'blue'


counter = 0



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
        # życia
        self.image = pacman_images[0]
        self.lifes_rect = self.image.get_rect()
        self.lifes_rect.x = WIDTH - 30 - CENTER_X_PLAYER
        self.lifes_rect.y = self.text_rect.y - CENTER_Y_PLAYER
    
    def draw(self, screen):
        screen.blit(self.text_render, self.text_rect)
        for i in range(self.lifes):
            screen.blit(self.image, (self.lifes_rect.x - i * 60, self.lifes_rect.y))
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
        hud.draw(screen)
        player.draw(screen)
        key_pressed = pygame.key.get_pressed()
        player.update(key_pressed)
        

    # Aktualizacja ekranu
    pygame.display.flip()
    clock.tick(60)


pygame.quit()