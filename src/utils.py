import pygame


WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (215, 184, 40)


HEIGHT = 600
WIDTH = 800

def write_text(text: str, size:int = 50, color:tuple = WHITE):
    pygame.init()
    font = pygame.font.SysFont(None, size, True)
    return font.render(text, size, color)

