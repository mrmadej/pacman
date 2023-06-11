from Global import *
from Button import Button
from Player import Player
from Ghost import Ghost
from typing import List

class Level:
    def __init__(self, board, color, starting_image: pygame.Surface) -> None:
        self.board = copy.deepcopy(board)
        self.board_cp = copy.deepcopy(board)
        # [player, clyde, blinky, inky, pinky]
        self.ghosts = None
        self.player = None
        # self.is_game_running
        # 0 start panel
        # 1 running game
        # 2 ending panel
        self.is_game_running = STARTING_PANEL
        self.first_start = True
        self.color = color
        self.starting_image = starting_image
        # text
        # win/lose
        self.font_size = 100
        self.font_color = (79, 0, 1)  # Biały kolor tekstu
        self.font = pygame.font.Font(FONT, self.font_size)
        self.text_render = self.font.render("Default", True, self.font_color, None)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = (WIDTH // 2, HEIGHT // 2)

        # score

        self.font_size_score = 50
        self.font_score = pygame.font.Font(FONT, self.font_size_score)
        self.text_render_score = None
        self.text_rect_score = None

        self.restart_button = Button(WIDTH // 2, (HEIGHT // 2) + 100, "RESTART", self.restart)
        self.start_button = Button(WIDTH // 2, (HEIGHT // 2) + 100, "START", self.start)
    
    def player_init(self, player: Player):
        self.player = player
        self.text_render_score = self.font.render(("Score: " + str(self.player.score)), True, self.font_color,
                                                  None)
        self.text_rect_score = self.text_render_score.get_rect()
        self.text_rect_score.center = (WIDTH // 2, HEIGHT // 2)
    
    def ghosts_init(self, ghosts: List[Ghost]):
        self.ghosts = ghosts
    
    def starting_panel(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))  # Czyszczenie ekranu
            # Rysowanie na ekranie
        screen.blit(self.starting_image, (90.5, 0))  # Wyświetlanie obrazka tła
            # screen.blit(button_image, button_rect)  # Wyświetlanie obrazka na przycisku
        self.start_button.draw(screen)

    def restart(self):
        self.board = copy.deepcopy(self.board_cp)
        self.player.score = 0
        self.player.lifes = 3
        self.is_game_running = RUNNING_GAME
        self.ending_timers()
        self.start()

    def draw_board(self, screen: pygame.Surface):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (j * TILE_X_LEN + (0.5 * TILE_X_LEN), i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), 4)
                if self.board[i][j] == 2:
                    pygame.draw.circle(screen, 'white', (j * TILE_X_LEN + (0.5 * TILE_X_LEN), i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), 10)
                if self.board[i][j] == 3:
                    pygame.draw.line(screen, self.color, (j * TILE_X_LEN + (0.5 * TILE_X_LEN), i * TILE_Y_LEN),
                                     (j * TILE_X_LEN + (0.5 * TILE_X_LEN), i * TILE_Y_LEN + TILE_Y_LEN), 3)
                if self.board[i][j] == 4:
                    pygame.draw.line(screen, self.color, (j * TILE_X_LEN, i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)),
                                     (j * TILE_X_LEN + TILE_X_LEN, i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), 3)
                if self.board[i][j] == 5:
                    pygame.draw.arc(screen, self.color,
                                    [(j * TILE_X_LEN - (TILE_X_LEN * 0.4)) - 2, (i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), TILE_X_LEN, TILE_Y_LEN],
                                    0, PI / 2, 3)
                if self.board[i][j] == 6:
                    pygame.draw.arc(screen, self.color,
                                    [(j * TILE_X_LEN + (TILE_X_LEN * 0.5)), (i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), TILE_X_LEN, TILE_Y_LEN], PI / 2, PI, 3)
                if self.board[i][j] == 7:
                    pygame.draw.arc(screen, self.color, [(j * TILE_X_LEN + (TILE_X_LEN * 0.5)), (i * TILE_Y_LEN - (0.4 * TILE_Y_LEN)), TILE_X_LEN, TILE_Y_LEN],
                                    PI,
                                    3 * PI / 2, 3)
                if self.board[i][j] == 8:
                    pygame.draw.arc(screen, self.color,
                                    [(j * TILE_X_LEN - (TILE_X_LEN * 0.4)) - 2, (i * TILE_Y_LEN - (0.4 * TILE_Y_LEN)), TILE_X_LEN, TILE_Y_LEN], 3 * PI / 2,
                                    2 * PI, 3)
                if self.board[i][j] == 9:
                    pygame.draw.line(screen, 'white', (j * TILE_X_LEN, i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)),
                                     (j * TILE_X_LEN + TILE_X_LEN, i * TILE_Y_LEN + (0.5 * TILE_Y_LEN)), 3)

    def start(self):
        self.is_game_running = RUNNING_GAME
        
        # reseting player
        self.player.rect.x = self.player.start_x
        self.player.rect.y = self.player.start_y
        self.player.start_timer(5, self.player.start_delay)
        self.player.started = False
        self.player.current_rotation = RIGHT
        self.player.animation()
        self.player.last_move = lambda: self.player.rect.move_ip([2, 0])


        i = 1
        # reseting ghosts
        for ghost in self.ghosts:
            ghost.rect.x = ghost.start_x
            ghost.rect.y = ghost.start_y
            ghost.start_timer(5 * i, EXIT_CAGE)
            ghost.image = ghost.image_storage
            ghost.current_mode = -1
            ghost.last_move = 0
            ghost.frighten_mode_first = True
            ghost.eaten = True
            i += 1

    def win(self):
        not_small_dots = not any(1 in row for row in self.board)
        not_big_dots = not any(2 in row for row in self.board)
        if not_small_dots and not_big_dots:
            self.player.score += 200 * self.player.lifes
            self.is_game_running = ENDING_PANEL
            PACMAN_WIN_SOUND.play()
            self.text_update("YOU WIN")

    def lose(self):
        if self.player.lifes == 0:
            self.is_game_running = ENDING_PANEL
            self.text_update("YOU DIED")

    def ending_timers(self):
        self.player.stop_timer()
        for ghost in self.ghosts:
            ghost.stop_timer()

    def ending_panel_display(self, screen: pygame.Surface):
        screen.blit(self.text_render, self.text_rect)
        screen.blit(self.text_render_score, self.text_rect_score)

    def text_update(self, text: str):
        self.text_render = self.font.render(text, True, self.font_color, None)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = (WIDTH // 2, (HEIGHT // 2) - 100)

        self.text_render_score = self.font_score.render(("Score: " + str(self.player.score)), True,
                                                        self.font_color, None)
        self.text_rect_score = self.text_render_score.get_rect()
        self.text_rect_score.center = (WIDTH // 2, HEIGHT // 2)

# class Level
# in constructor:
#   List[int] board - deep copy of the board
#   List[int] board_cp = deep copy of the board to restore the board after restart
#   List[Ghost] ghosts - it will be initialized later in ghosts_init with the table filled with ghosts objects
#   Player player - it will be initialized later in player_init with player object
#   int is_game_running - in which mode the game is. starting with STARTING_PANEL
#   boolean first_start - True if game is started for the first time
#   color - color of the lines in the maze
#   starting_image - starting image of pacman
#   int font_size
#   font_color = (79, 0, 1)
#   font
#   text_render
#   text_rect
#   text_rect.center
#   int font_size_score
#   font_score
#   text_render_score
#   text_rect_score
#   Button restart_button 
#   Button start_button
#
# def player_init(self, player: Player)
#   initialazing player with Player object and initializing text connected to player
#
# def ghosts_init(self, ghosts: List[Ghost])
#   initializing ghosts with table filled with ghosts objects
#
# def starting_panel(self, screen: pygame.Surface)
#   drawing starting panel
#
# def restart(self)
#   restarting game
#
# def draw_board(self, screen: pygame.Surface)
#   drawing board
#
# def start(self)
#   settings everything to default
#
# def win(self)
#   settings mode to ENDING_PANEL and updating text ot "YOU WIN"
#
# def lose(self)
#   settings mode to ENDING_PANEL and updating text ot "YOU DIED"
#
# def ending_timers(self)
#   stops all timers in player and ghosts
#
# def ending_panel_display(self, screen: pygame.Surface)
#   displaying ending panel
# 
# def text_update(self, text: str)
#   updating all texts