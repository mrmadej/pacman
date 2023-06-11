from Global import *
from Player import Player
from Ghost import Ghost
from Level import Level
from HUD import HUD
from board import *

def main():
    # concretization 
    level = Level(boards, COLOR_BOARD, STARTING_IMAGE)
    hud = HUD(0, 3, pacman_images[0])
    player = Player(PLAYER_X, PLAYER_Y, pacman_images[0], level, hud)
    blinky = Ghost(IMAGE_GHOST_BLUE, 472, 410, 0, 0, BLINKY, 100, level, hud)
    inky = Ghost(IMAGE_GHOST_ORANGE, 412, 410, WIDTH, 0, INKY, 200, level, hud)
    pinky = Ghost(IMAGE_GHOST_PINK, 352, 410, WIDTH, HEIGHT, PINKY, 300, level, hud)
    clyde = Ghost(IMAGE_GHOST_RED, 412, 326, 0, HEIGHT, CLYDE, 400, level, hud)
    level.player_init(player)
    level.ghosts_init([clyde, blinky, inky, pinky])

    # filling screen with black
    screen.fill((0, 0, 0))

    # fps
    clock = pygame.time.Clock()

    window_open = True

    # main loop
    while window_open:
        for event in pygame.event.get():
            # exiting game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level.ending_timers()
                    window_open = False
            elif event.type == pygame.QUIT:
                level.ending_timers()
                window_open = False

            # checking if buttons were clicked
            if level.is_game_running == STARTING_PANEL:
                level.start_button.if_clicked(event)

            if level.is_game_running == ENDING_PANEL:
                level.restart_button.if_clicked(event)
        
        # displaying starting panel
        if level.is_game_running == STARTING_PANEL:
            level.starting_panel(screen)
        
        # displaying game
        if level.is_game_running == RUNNING_GAME:
            if level.first_start:
                level.first_start = False
                level.start()
            
            # checking win/lose conditions
            level.win()
            level.lose()
            
            # filling screen with black
            screen.fill((0, 0, 0))

            # drawing everything on the screen (board, hud, ghosts and player)
            level.draw_board(screen)
            hud.draw(screen)
            player.draw(screen)
            blinky.draw(screen)
            pinky.draw(screen)
            inky.draw(screen)
            clyde.draw(screen)

            # checking pressed keys
            key_pressed = pygame.key.get_pressed()

            # updating everything (player and ghosts)
            player.update(key_pressed)
            blinky.update()
            pinky.update()
            inky.update()
            clyde.update()

        # displaying ending panel
        if level.is_game_running == ENDING_PANEL:
            screen.fill((0, 0, 0))
            level.ending_panel_display(screen)
            level.restart_button.draw(screen)

        # updating screen
        pygame.display.flip()
        
        # fps 60
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()