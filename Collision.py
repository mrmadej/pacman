from Global import *


class Collision:
    def __init__(self, board) -> None:
        self.rect = None
        self.possible_turns = [False, False, False, False]
        self.center_x = 0
        self.center_y = 0
        self.square_x = 0
        self.square_y = 0
        self.x_offset = 0
        self.y_offset = 0
        self.board = board

    def update_position(self):
        # center_x , center_y coordinates of center of element
        self.center_x = self.rect.x + CENTER_X_PLAYER
        self.center_y = self.rect.y + CENTER_Y_PLAYER

        # try to calculate square coordinates
        self.square_x = self.center_x // TILE_X_LEN
        self.square_y = self.center_y // TILE_Y_LEN

        self.x_offset = self.center_x % TILE_X_LEN
        self.y_offset = self.center_y % TILE_Y_LEN

    def position(self):
        self.possible_turns = [False, False, False, False]

        if self.board[self.square_y][(self.square_x + 1) % NUM_COLS] < 3 or self.x_offset < (TILE_X_LEN // 2):
            self.possible_turns[RIGHT] = True
        if self.board[self.square_y][(self.square_x - 1) % NUM_COLS] < 3 or self.x_offset > (TILE_X_LEN // 2):
            self.possible_turns[LEFT] = True
        if self.board[self.square_y - 1][self.square_x % NUM_COLS] < 3 or self.y_offset > (TILE_Y_LEN // 2):
            self.possible_turns[UP] = True
        if self.board[(self.square_y + 1) % NUM_ROWS][self.square_x % NUM_COLS] < 3 or self.y_offset < (
                TILE_Y_LEN // 2):
            self.possible_turns[DOWN] = True