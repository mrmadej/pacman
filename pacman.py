import pygame, os

pygame.init()

window_open = True
# wymiary okna
WIDTH = 1280
HEIGHT = 720


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
button_x = 471.5
button_y = 500
button_width = 337
button_height = 130

# Utworzenie przycisku
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)


screen.fill((0, 0, 0))
is_game_running = False

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

    
    
    screen.fill((255, 255, 255))  # Czyszczenie ekranu
    
    # Rysowanie na ekranie
    screen.blit(background_image, (0, 0))  # Wyświetlanie obrazka tła
    screen.blit(button_image, button_rect)  # Wyświetlanie obrazka na przycisku


    if is_game_running:
        # Renderowanie planszy gry

        # Ustawienie koloru tła na czerwony
        screen.fill((255, 0, 0))
    
        # Renderowanie ekranu startowego

    # Aktualizacja ekranu
    pygame.display.flip()
    


pygame.quit()