from Global import *

class HUD:
    def __init__(self, score: int, lifes: int, image: pygame.Surface) -> None:
        self.score = score
        self.lifes = lifes
        # text/score
        self.font_size = 32
        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(FONT, self.font_size)
        self.text_render = self.font.render(("Score: " + str(score)), True, self.font_color, None)
        self.text_rect = self.text_render.get_rect()
        self.text_rect.x = 30
        self.text_rect.y = 934
        # lifes
        self.image = image
        self.lifes_rect = self.image.get_rect()
        self.lifes_rect.x = WIDTH - 30 - CENTER_X_PLAYER # 847
        self.lifes_rect.y = self.text_rect.y - 10 # 924

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text_render, self.text_rect)
        for i in range(self.lifes):
            screen.blit(self.image, (self.lifes_rect.x - i * 60, self.lifes_rect.y))

    def update(self, score: int, lifes: int):
        self.score = score
        self.lifes = lifes
        self.text_render = self.font.render(("Score: " + str(score)), True, self.font_color, None)

# class HUD
# in constructor:
#   int score - number of points collected by player
#   int lifes - number of lifes of player
#   int font_size
#   font_color (white)
#   font - custom font(OptimusPrinceps.ttf), size(32)
#   text_render - rendering text("Score: " *current score*) with antialiasing and font_color
#   text_rect - rect of text_render
#   text_rect.x, text_rect.y - coordinates of text
#   image - basic image of pacman that will represent life
#   lifes_rect - rect of image
#   lifes_rect.x, lifes_rect.y - coordinates of life
#
# def draw(self, screen: pygame.Surface)
#   displaying score and lifes on the bottom of the screen
#
# def update(self, score: int, lifes: int)
#   updating score, lifes and rendering new text_render with new score