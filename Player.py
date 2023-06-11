import threading
from Global import *
from Collision import Collision
from HUD import HUD


class Player(Collision):
    def __init__(self, player_x: int, player_y: int, image: pygame.Surface, level, hud: HUD) -> None:
        super().__init__(level.board)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.score = 0
        self.powerup = False
        self.lifes = 3
        self.current_rotation = RIGHT
        self.start_x = player_x
        self.start_y = player_y
        self.timer = None
        self.started = False
        self.last_move = lambda: self.rect.move_ip([STEP, 0])
        self.counter = 0
        self.hud = hud
        self.level = level

    def start_timer(self, duration, callback):
        self.stop_timer()
        self.timer = threading.Timer(duration, callback)
        self.timer.start()

    def stop_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()

    def start_delay(self):
        self.started = True

    def powerUp(self):
        self.powerup = False

    def make_a_move(self, direction):
        # distance from the middle of the tile
        move_x = - (self.x_offset - TILE_X_LEN // 2)
        move_y = - (self.y_offset - TILE_Y_LEN // 2)

        if LEFT == direction:
            if self.possible_turns[LEFT]:
                self.current_rotation = LEFT
                if self.center_x > STEP:
                    self.rect.move_ip([-STEP, move_y])
                else:
                    self.rect.move_ip([WIDTH - STEP, move_y])
                self.last_move = lambda: self.make_a_move(LEFT)
        if RIGHT == direction:
            if self.possible_turns[RIGHT]:
                self.current_rotation = RIGHT
                if self.center_x < (WIDTH - STEP):
                    self.rect.move_ip([STEP, move_y])
                else:
                    self.rect.move_ip([-WIDTH, move_y])
                self.last_move = lambda: self.make_a_move(RIGHT)
        if UP == direction:
            if self.possible_turns[UP]:
                self.current_rotation = UP
                if self.center_y > STEP:
                    self.rect.move_ip([move_x, -STEP])
                else:
                    self.rect.move_ip([move_x, HEIGHT - MARGIN - STEP - 1])
                self.last_move = lambda: self.make_a_move(UP)
        if DOWN == direction:
            if self.possible_turns[DOWN]:
                self.current_rotation = DOWN
                if self.center_y < (HEIGHT - MARGIN - STEP):
                    self.rect.move_ip([move_x, STEP])
                else:
                    self.rect.move_ip([move_x, -HEIGHT + MARGIN])
                self.last_move = lambda: self.make_a_move(DOWN)

    def _get_event(self, key_pressed):
        x_in_center = self.x_offset == TILE_X_LEN // 2
        y_in_center = self.y_offset == TILE_Y_LEN // 2

        self.position()
        if x_in_center and y_in_center:
            if key_pressed[pygame.K_LEFT]:
                self.make_a_move(LEFT)
            if key_pressed[pygame.K_RIGHT]:
                self.make_a_move(RIGHT)
            if key_pressed[pygame.K_UP]:
                self.make_a_move(UP)
            if key_pressed[pygame.K_DOWN]:
                self.make_a_move(DOWN)
            if self.possible_turns[self.current_rotation]:
                self.last_move()
        else:
            if self.possible_turns[self.current_rotation]:
                self.last_move()

    def eating(self):
        position = self.level.board[(self.center_y // TILE_Y_LEN) % NUM_ROWS][(self.center_x // TILE_X_LEN) % NUM_COLS]

        if position == 1 or position == 2:
            self.level.board[self.center_y // TILE_Y_LEN][self.center_x // TILE_X_LEN] = 0
            if position == 1:
                self.score += 10
                if not pygame.mixer.get_busy():
                    EATING_SOUND.play()
            elif position == 2:
                self.score += 50
                self.powerup = True
                self.start_timer(POWERUP_TIME, self.powerUp)
                if not pygame.mixer.get_busy():
                    EATING_SOUND.play()

        self.hud.update(self.score, self.lifes)

    def animation(self):
        if self.counter < 19:
            self.counter += 1
        else:
            self.counter = 0
        which_image = self.counter // 5
        if self.current_rotation == RIGHT:
            self.image = pacman_images[which_image]
        elif self.current_rotation == DOWN:
            self.image = pygame.transform.rotate(pacman_images[which_image], -90)
        elif self.current_rotation == LEFT:
            self.image = pygame.transform.rotate(pacman_images[which_image], 180)
        elif self.current_rotation == UP:
            self.image = pygame.transform.rotate(pacman_images[which_image], 90)

    def update(self, key_pressed):
        if self.started:
            self.update_position()
            self.eating()
            self._get_event(key_pressed)
            self.animation()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
# class Player derived from Collision class
# in constructor:
#   int player_x, player_y - int coordinates of start position
#   pygame.Surface image - image of pacman
#   Rect rect - rectangle outlined image get by get_rect
#   int rect.x, rect.y - coordinates o left upper corner of the rectangle rect
#   int score - number of points currently possed by player
#   boolean powerup -  defining if player can eat ghosts (for 10 sec after eating big dot)
#   int lifes - number of lifes of player, after reaching 0 the game ends
#   int current_rotation - in wich direction player is currently rotated
#   int start_x, start_y - starting coordinates of player
#   threading.Timer timer - timer object, it suposed to call given function after certain amount of time in secends
#   boolean started - if True player can use function in update method (update_position(), eating(), _get_event(key_pressed), animation())
#   last_move - it stores lambda function that was last activated to perform move in: def make_a_move(self, direction)
#   int counter - for animation
#   hud - HUD object
#   level - Level object
#   
#   def start_timer(self, duration, callback):
#       duration - time in seconds
#       callback - function that will be called after duration
#       
#       it stops previous timer, creating new and starts it
#
#   def stop_timer(self)
#       if timer exists and is still alive cancels it
#
#   def start_delay(self)
#       sets strted to True after called by timer
#
#   def powerUp(self)
#       sets powerup to False, player can no longer eat ghosts
#
#   def make_a_move(self, direction)
#       making the move by STEP and correctig position to be sure it will be in the center       
#
#   def _get_event(self, key_pressed)
#       deciding in which direction to move
#       if in center then can chose the direction (or still go the same)
#       else going the same direction       
#
#   def eating(self)
#       based on current tile in wich player is modifying board (if there was a big or small dot [1 or 2], changes it to 0 [empty tile])
#       and adding 10 points if small dot (1) or 50 points and starting powerup (10 sec) (big dot - 2)
#   
#   def animation(self)
#       for animation of pacman (open and closing mouth)
#
#   def update(self, key_pressed)
#       calling functions (update_position, eating, _get_event, animation), it is called every loop
#
#   def draw(self, screen: pygame.Surface)
#       drawing pacman on screen