import pygame
import os
import math
from board import *

pygame.init()

window_open = True
# wymiary okna
WIDTH = 900
HEIGHT = 950
PI = math.pi

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

level = boards

color = 'blue'

player_x = 450
player_y = 663


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y) -> None:
        super().__init__()
        self.images = []
        for image in pacman_images:
            self.images.append(image)
            self.images.append(pygame.transform.flip(image, True, False))
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def _get_event(self, key_pressed):
        if key_pressed[pygame.K_LEFT]:
            self.rect.move_ip([-1, 0])
        if key_pressed[pygame.K_RIGHT]:
            self.rect.move_ip([1, 0])
        if key_pressed[pygame.K_UP]:
            self.rect.move_ip([0, -1])
        if key_pressed[pygame.K_DOWN]:
            self.rect.move_ip([0, 1])

    def update(self, key_pressed):
        self._get_event(key_pressed)
        # Aktualizacja animacji
        self.frame_index = (self.frame_index + 1) % len(self.images)
        self.image = self.images[self.frame_index]

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


player = Player(WIDTH // 2, HEIGHT // 2)

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