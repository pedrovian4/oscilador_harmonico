from utils import write_text, YELLOW, WHITE, HEIGHT, WIDTH
import math
import pygame
from pygame.math import Vector2
from sand_box import Sandbox

class Menu:
    options = ["Iniciar", "Sair"]
    selected = 0
    coeficiente = 80

    def draw(self):
        self.state_machine.window.fill((0, 0, 0))
        screen_middle_x = self.state_machine.window.get_width() / 2 - 70
        screen_middle_y = self.state_machine.window.get_height() / 2 - 70
        for i, option in enumerate(self.options):
            color = YELLOW if self.options[self.selected] == option else WHITE
            text = write_text(option, 80, color)
            self.state_machine.window.blit(text, (screen_middle_x, screen_middle_y + self.coeficiente * i))
        
    def update(self):
        pass

    def process(self, event):
        if self.selected < 0:
            self.selected = 0
        elif self.selected > (len(self.options) - 1):
            self.selected = (len(self.options) - 1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected -= 1
            elif event.key == pygame.K_DOWN:
                self.selected += 1
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected] == "Iniciar":
                    self.state_machine.clear_current_state()
                    sandbox = Sandbox()
                    sandbox.set_state_machine(self.state_machine)
                    sandbox.load()
                    self.state_machine.set_state(sandbox)
                elif self.options[self.selected] == "Sair":
                    pygame.quit()
                    quit()

    def set_state_machine(self, state_machine):
        self.state_machine = state_machine
        return self

    def load(self):
        ...
