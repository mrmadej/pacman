import threading
from Global import *
from Collision import Collision
from HUD import HUD

class Ghost(Collision):
    def __init__(self, image: pygame.Surface, x: int, y: int, scatter_target_x: int, scatter_target_y: int, name: int,
                 points: int, level, hud: HUD) -> None:
        super().__init__(level.board)
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
        # RIGHT, DOWN, LEFT, UP
        self.directionImportance = [0, 1, 2, 3]
        self.frighten_mode_first = True
        self.eaten = True
        self.current_mode = -1
        self.timer = None
        self.points = points
        self.level = level
        self.hud = hud
        self.image_power_up = IMAGE_GHOST_POWERUP
        self.image_dead = IMAGE_GHOST_DEAD

    def getting_pinky(self):
        for i in range(4):
            if self.level.ghosts[i].ghost_name == PINKY:
                return i

    def killing_pacman(self):
        if abs(self.center_x - self.level.player.center_x) <= 2 and abs(
                self.center_y - self.level.player.center_y) <= 2 and self.current_mode != EATEN_MODE and self.current_mode != FRIGHTEN_MODE:
            PACMAN_DEATH_SOUND.play()
            self.level.player.lifes -= 1
            self.hud.update(self.level.player.score, self.level.player.lifes)
            self.level.start()

    def is_in_cage(self) -> bool:
        x = 12 <= self.center_x // TILE_X_LEN <= 17
        y = 13 <= self.center_y // TILE_Y_LEN <= 16
        cage = x and y
        front_cage_x = 14 <= self.center_x // TILE_X_LEN <= 15
        front_cage_y = self.center_y // TILE_Y_LEN == 12
        front_cage = front_cage_x and front_cage_y
        return cage or front_cage

    def start_timer(self, duration, callback):
        self.stop_timer()
        self.timer = threading.Timer(duration, lambda: self.timer_callback(mode=callback))
        self.timer.start()

    def stop_timer(self):
        if self.timer and self.timer.is_alive():
            self.timer.cancel()

    def timer_callback(self, mode):
        self.current_mode = mode

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self, direction: int):
        self.last_move = direction

        if direction == RIGHT:
            if self.center_x < (WIDTH - STEP):
                self.rect.move_ip([STEP, 0])
            else:
                self.rect.move_ip([-WIDTH, 0])
        if direction == LEFT:
            if self.center_x > STEP:
                self.rect.move_ip([-STEP, 0])
            else:
                self.rect.move_ip([WIDTH - STEP, 0])
        if direction == UP:
            if self.center_y > STEP:
                self.rect.move_ip([0, -STEP])
            else:
                self.rect.move_ip([0, HEIGHT - MARGIN - STEP - 1])
        if direction == DOWN:
            if self.center_y < (HEIGHT - MARGIN - STEP):
                self.rect.move_ip([0, STEP])
            else:
                self.rect.move_ip([0, -HEIGHT + MARGIN])

    def change_mode(self, mode=None):
        if mode is not None:
            self.current_mode = mode

        if self.current_mode != FRIGHTEN_MODE and self.current_mode != EATEN_MODE and self.level.player.powerup == True and not self.is_in_cage():
            self.image = self.image_power_up
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

        if self.ghost_name == BLINKY:
            self.move(self.calculate_distance(self.level.player.center_x, self.level.player.center_y))
        elif self.ghost_name == INKY:
            i = self.getting_pinky()
            self.move(self.calculate_distance(self.level.ghosts[i].center_x, self.level.ghosts[i].center_y))
        elif self.ghost_name == PINKY:
            direction = self.level.player.current_rotation
            if direction == RIGHT:
                self.move(self.calculate_distance(self.level.player.center_x + 2 * TILE_X_LEN, self.level.player.center_y))
            elif direction == LEFT:
                self.move(self.calculate_distance(self.level.player.center_x - 2 * TILE_X_LEN, self.level.player.center_y))
            elif direction == UP:
                self.move(self.calculate_distance(self.level.player.center_x, self.level.player.center_y - 2 * TILE_Y_LEN))
            elif direction == DOWN:
                self.move(self.calculate_distance(self.level.player.center_x, self.level.player.center_y + 2 * TILE_Y_LEN))
        elif self.ghost_name == CLYDE:
            condition = abs((self.center_x // TILE_X_LEN) + (
                        (self.center_y // TILE_Y_LEN) - self.level.player.center_x // TILE_X_LEN - self.level.player.center_y // TILE_Y_LEN))
            if condition > 8:
                self.move(self.calculate_distance(self.level.player.center_x, self.level.player.center_y))
            else:
                self.move(self.calculate_distance(self.scatter_target_x, self.scatter_target_y))

    def scatter_mode(self):
        self.image = self.image_storage
        if self.timer and not self.timer.is_alive():
            duration = random.randint(5, 15)
            self.start_timer(duration, CHASE_MODE)
        self.move(self.calculate_distance(self.scatter_target_x, self.scatter_target_y))

    def exit_cage(self):
        if self.center_x == EATEN_MODE_TARGET_X and self.center_y == EATEN_MODE_TARGET_Y:
            self.eaten = False
            self.current_mode = CHASE_MODE
            duration = random.randint(5, 15)
            self.start_timer(duration, SCATTER_MODE)
        else:
            self.move(self.calculate_distance(EATEN_MODE_TARGET_X, EATEN_MODE_TARGET_Y))

    def eaten_mode(self):
        self.stop_timer()
        if self.eaten == False:
            PACMAN_EATGHOST_SOUND.play()
            self.eaten = True
            self.image = self.image_dead
            self.frighten_mode_first = False
        if self.center_x == self.start_x + CENTER_X_PLAYER and self.center_y == self.start_y + CENTER_Y_PLAYER:
            self.last_move = -1
            self.image = self.image_storage
            self.current_mode = EXIT_CAGE
        else:
            self.move(self.calculate_distance(self.start_x + CENTER_X_PLAYER, self.start_y + CENTER_Y_PLAYER))

    def frighten_mode(self):

        if (self.center_x // TILE_X_LEN == self.level.player.center_x // TILE_X_LEN) and (
                self.center_y // TILE_Y_LEN == self.level.player.center_y // TILE_Y_LEN):
            self.stop_timer()
            self.current_mode = EATEN_MODE
            self.level.player.score += self.points
        if self.frighten_mode_first:
            self.frighten_mode_first = False
            if self.last_move == DOWN:
                self.last_move = UP
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
            while not self.possible_turns[next_direction]:
                next_direction = random.randint(0, 3)
        self.move(next_direction)

    def calculate_distance(self, target_x, target_y):

        if self.eaten:
            if self.level.board[(self.center_y // TILE_Y_LEN) + 1][(self.center_x // TILE_X_LEN)] == 9:
                self.possible_turns[DOWN] = True
            if self.level.board[(self.center_y // TILE_Y_LEN) - 1][(self.center_x // TILE_X_LEN)] == 9:
                self.possible_turns[UP] = True
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
        self.update_position()
        self.position()
        self.killing_pacman()
        self.change_mode()

    def center_check(self) -> bool:
        return self.x_offset == TILE_X_LEN // 2 and self.y_offset == TILE_Y_LEN // 2
    
# class Ghost derived from Collision
# in constructor:
#   pygame.Surface image - image of the ghost
#   int ghost_name - id of ghost (Blinky, Inky, Piky, Clyde). It decide which chase_mode algorithm use
#   image_storage - it is for restore oryginal image after changing for frighten and eaten image
#   rect - rect of the image
#   start_x, start_y - starting coordinates, used for retoring starting position and final destinetion of eaten ghost
#   rect.x, rect.y - coordinates
#   scatter_target_x, scatter_target_y - target coordinations in scatter_mode
#   int last_move - what was the last direction
#   directionImportance - importance of directions, used to decide which direction chose if both have same distance
#   boolean frighten_mode_first - decide if this enter to frighten_mode was first
#   boolean eaten - if ghost is eaten then True (when in cage also True)
#   int current_mode - which mode is currently in use
#   threading.Timer timer - used to changing mode after certain amount of time
#   int points - number of points added to players score after eating that ghost
#   level - Level object
#   hud - HUD object
#   image_power_up - image that is used in frighten mode
#   image_dead - image that is used in eaten mode
#
#   def getting_pinky(self)
#       to get pinky's index to get to the pinky's coordinates in chase mode
#
# def killing_pacman(self)
#   if pacman ang ghost are between <0, 2> of each other and ghost is either in scatter or chase mode then pacman is dead
#   plays PACMAN_DEATH_SOUND, decreasing player.lifes by 1, updating information about score and lifes in HUD
#   and starting level again
#
# def is_in_cage(self) -> bool
#   return True if ghost is either in cage or in front of gate (white line) to the cage
#
# def start_timer(self, duration, callback)
#   stops previous timer using stop_timer
#   creating new timer with duration and calling timer_callback, with callback as mode, after duration
#   stats new created timer
#
# def stop_timer(self)
#   stops previous timer if exists and is_alive
#
# def timer_callback(self, mode)
#   setting current_mode to mode after called by timer
#
# def draw(self, screen: pygame.Surface)
#   drawing on the screen image of the ghost
#
# def move(self, direction: int)
#   sets last_move to direction (when move is called it is certain that direction will be used so it will be las_move next time)
#   move pacman by STEP (2) in direction, or if entering the tunel to move on the opposite site of the board
# 
# def change_mode(self, mode=None)
#   using mode based on current_mode
#   if mode is given, sets current_mode to mode
#   and sets frithen_mode for first time
#
# def chase_mode(self)
#   setting image to normal ghost picture
#   setting timer with random duration to change mode to scatter_mode
#   chosing algorithm based on ghost_name
#   BLINKY go to the center of the player
#   INKY goes to the center of the PINKY
#   PINKY goes 2 tiles in front of player
#   CLYDE goes to the center of player if ghost_tiles_in_x + ghost_tiles_in_y - player_tiles_in_x - player_tiles_in_y > 8
#   in other case it goes to the scatter mode target
#
# def scatter_mode(self)
#   setting image to normal ghost picture
#   setting timer with random duration to change mode to chase_mode
#   goes to the scatter mode target
#
# def exit_cage(self)
#   moving ghost outside of the cage (tile in front of the cage) and setting timer with random duration to scatter_mode
#
# def eaten_mode(self)
#   changing image to the eaten image (only eayes)
#   and going to the start position
#
#  def frighten_mode(self)
#   setting timer to know when end frighten mode
#   if met player then changing mode to eaten
#   chosing random direction at crossroads and at the begining turning 180 degree
#
# def calculate_distance(self, target_x, target_y)
#   calculating distance from the target and chosing direction that gives the closest distance
# 
# def update(self)
#   using methods: update_position, position, killing_pacman, change_mode
#
#  center_check(self) -> bool
#   returns True if ghost is in the middle of the tile