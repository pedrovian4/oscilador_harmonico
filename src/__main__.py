from utils import write_text, YELLOW, WHITE, HEIGHT, WIDTH
import math
import pygame
from pygame.math import Vector2
from menu import Menu


class StateMachine:
    def __init__(self, window):
        self.window = window
        self.current_state = None

    def set_state(self, new_state):
        self.current_state = new_state

    def clear_current_state(self):
        if hasattr(self.current_state, 'cleanup') and callable(self.current_state.cleanup):
            self.current_state.cleanup()
        self.current_state = None

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self):
        if self.current_state:
            self.current_state.draw()
            pygame.display.flip()

    def process(self, event):
        if self.current_state:
            self.current_state.process(event)

def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Oscilador Harmônico Simples")

    clock = pygame.time.Clock()
    state_machine = StateMachine(window)

    menu = Menu()
    menu.set_state_machine(state_machine)
    menu.load()
    state_machine.set_state(menu)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            state_machine.process(event)
        state_machine.update()
        state_machine.draw()
        clock.tick(120)
    pygame.quit()

if __name__ == "__main__":
    main()
