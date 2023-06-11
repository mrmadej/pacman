from Global import *
class Button:
    def __init__(self, x, y, text, function):
        self.rect = pygame.Rect(x - 150, y, 300, 75)
        self.text = text
        self.function = function
        self.button_color = (117, 117, 117)

        self.font_size = 50
        self.font_color = (79, 0, 1)  # Biały kolor tekstu
        self.font = pygame.font.Font(FONT, self.font_size)
        self.text_render = self.font.render(self.text, True, self.font_color, None)
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.button_color, self.rect)
        screen.blit(self.text_render, self.text_rect)

    def if_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                START_SOUND.play()
                self.function()

# class Button
# in constructor:
#   rect - creating rect with given position and dimensions
#   text - its simlpe text that will be on the button
#   function - function that will be called after clicking button
#   button_color
#   font_size
#   font_color
#   font
#   text_render
#   text_rect
#
# def draw(self)
#   drawing button on the screen
#
# def if_clicked(self, event)
#   chcecking if button has been clicked if yes then calling function