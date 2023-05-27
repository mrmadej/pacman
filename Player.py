import threading
import pygame
from Global import *




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
    def time(self):
        timer = threading.Timer(POWERUP_TIME, self.powerUp)
        timer.start()
    def powerUp(self):
        self.powerup = False
    def _get_event(self, key_pressed):
        self.position(key_pressed)
        if key_pressed[pygame.K_LEFT]:
            if self.possible_turns[LEWO] == True:
                self.current_rotation = LEWO
                self.rect.move_ip([-2, 0])
        if key_pressed[pygame.K_RIGHT]:
            if self.possible_turns[PRAWO] == True:
                self.current_rotation = PRAWO
                self.rect.move_ip([2, 0])
        if key_pressed[pygame.K_UP]:
            if self.possible_turns[GORA] == True:
                self.current_rotation = GORA
                self.rect.move_ip([0, -2])
        if key_pressed[pygame.K_DOWN]:
            if self.possible_turns[DOL] == True:
                self.current_rotation = DOL
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
    def position(self, key_pressed):
        self.possible_turns = [False, False, False, False]
        # 0 - prawo
        # 1 - dół
        # 2 - lewo
        # 3 - góra
        CENTER_X = self.rect.x + CENTER_X_PLAYER
        CENTER_Y = self.rect.y + CENTER_Y_PLAYER

        PLUS_MINUS_NUM = 2

        if key_pressed[pygame.K_RIGHT]:
            if level[CENTER_Y // TILE_Y_LEN][(CENTER_X + (TILE_X_LEN // 2) + PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                self.possible_turns[PRAWO] = True
        
        if key_pressed[pygame.K_LEFT]:
            if level[CENTER_Y // TILE_Y_LEN][(CENTER_X - (TILE_X_LEN // 2) - PLUS_MINUS_NUM) // TILE_X_LEN] < 3:
                self.possible_turns[LEWO] = True

        if key_pressed[pygame.K_UP]:
            if level[(CENTER_Y - (TILE_Y_LEN // 2) - PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                self.possible_turns[GORA] = True

        if key_pressed[pygame.K_DOWN]:
            if level[(CENTER_Y + (TILE_Y_LEN // 2) + PLUS_MINUS_NUM) // TILE_Y_LEN][CENTER_X // TILE_X_LEN] < 3:
                self.possible_turns[DOL] = True



    def testing_position(self):
        #print("Piksel_x: " + str(self.rect.x + CENTER_X_PLAYER) + "; Piksel_y: " + str(self.rect.y + CENTER_Y_PLAYER) + "; Level_x: " + str((self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33)) + "; Level_y: " + str((self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30)) + "; Level[x][y]: " + str(level[((self.rect.y + CENTER_Y_PLAYER) // ((HEIGHT - 50) // 33))][((self.rect.x + CENTER_X_PLAYER) // (WIDTH // 30))]) + "\n")
        print("Powerup: " + str(self.powerup))
    def update(self, key_pressed):
        self.testing_position()
        self.eating()
        self._get_event(key_pressed)
        self.animation()
        pygame.draw.circle(screen, 'white', (self.rect.x + CENTER_X_PLAYER, self.rect.y + CENTER_Y_PLAYER), 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)