import math
import pygame
import numpy as np
from pygame.math import Vector2
from utils import write_text, YELLOW, WHITE, HEIGHT, WIDTH
from ml import MLModelEquations

class Sandbox:
    def __init__(self):
        self.particle = {
            "pos": Vector2(400, 300),
            "vel": Vector2(0, 0),
            "mass": 10,
            "radius": 15
        }
        self.anchor = Vector2(400, 200)
        self.spring = {
            "k": 2.5,
            "damping": 0.09,
            "rest_length": 50
        }
        self.gravity = Vector2(0, 0.5)
        self.dragging = False
        self.background_color = (10, 10, 40)
        self.last_force = Vector2(0, 0)
        self.last_acceleration = Vector2(0, 0)
        self.last_stretch = 0.0
        self.history = []
        self.fps = 60

        self.ml_model_eq = MLModelEquations(degree=10)
        self.eq_x_str = None
        self.eq_y_str = None
        self.predicted_pos = None 

    def draw(self):
        window = self.state_machine.window
        window.fill(self.background_color)

        pygame.draw.line(window, (200, 200, 200), self.anchor, self.particle["pos"], 3)
        pygame.draw.circle(window, (100, 100, 255), self.anchor, 8)
        color_real = (255, 180, 90) if not self.dragging else (255, 90, 90)
        pygame.draw.circle(window, color_real, self.particle["pos"], self.particle["radius"])
        window.blit(write_text("Sistema Real",12, WHITE), (self.anchor.x - 50, self.anchor.y - 50))

        if self.predicted_pos is not None:
            offset = Vector2(0, 200)
            predicted_anchor = self.anchor + offset
            predicted_pos_display = self.predicted_pos + offset
            pygame.draw.line(window, (200, 255, 90), predicted_anchor, predicted_pos_display, 3)
            pygame.draw.circle(window, (100, 100, 255), predicted_anchor, 8)
            pygame.draw.circle(window, (100, 255, 90), (int(predicted_pos_display.x), int(predicted_pos_display.y)), self.particle["radius"])


        pos = self.particle["pos"]
        vel = self.particle["vel"]
        force = self.last_force
        acc = self.last_acceleration
        stretch = self.last_stretch

        window.blit(write_text(f"Posicao: ({pos.x:.2f}, {pos.y:.2f})", 25), (10, 10))
        window.blit(write_text(f"Velocidade: ({vel.x:.2f}, {vel.y:.2f})", 25), (10, 40))
        window.blit(write_text(f"Forca: ({force.x:.2f}, {force.y:.2f})", 25), (10, 70))
        window.blit(write_text(f"Aceleracao: ({acc.x:.2f}, {acc.y:.2f})", 25), (10, 100))
        window.blit(write_text(f"Estiramento: {stretch:.2f}", 25), (10, 130))
        window.blit(write_text(f"FPS: {self.fps}", 25), (10, 160))
        window.blit(write_text(f"Constante Elastica (k): {self.spring['k']:.2f}", 25), (10, 190))
        window.blit(write_text(f"Amortecimento: {self.spring['damping']:.2f}", 25), (10, 220))

        self.draw_graphs(window)

    def draw_graphs(self, window):
        graph_x_area = pygame.Rect(500, 10, 280, 150)
        graph_y_area = pygame.Rect(500, 170, 280, 150)
        pygame.draw.rect(window, WHITE, graph_x_area, 1)
        pygame.draw.rect(window, WHITE, graph_y_area, 1)
        self.draw_cartesian_axes(window, graph_x_area, max_value=WIDTH, label="X")
        self.draw_cartesian_axes(window, graph_y_area, max_value=HEIGHT, label="Y")

        if len(self.history) < 2:
            return

        num_points = min(len(self.history), graph_x_area.width)
        step = len(self.history) / num_points
        x_points = []
        for i in range(num_points):
            index = int(i * step)
            pos_val = self.history[index].x
            normalized = pos_val / float(WIDTH)
            graph_y = graph_x_area.bottom - normalized * graph_x_area.height
            graph_x = graph_x_area.left + i
            x_points.append((graph_x, graph_y))
        if len(x_points) > 1:
            pygame.draw.lines(window, (255, 0, 0), False, x_points, 2)
            window.blit(write_text("X", 20, YELLOW), (graph_x_area.left + 5, graph_x_area.top + 5))

        num_points = min(len(self.history), graph_y_area.width)
        step = len(self.history) / num_points
        y_points = []
        for i in range(num_points):
            index = int(i * step)
            pos_val = self.history[index].y
            normalized = pos_val / float(HEIGHT)
            graph_y = graph_y_area.bottom - normalized * graph_y_area.height
            graph_x = graph_y_area.left + i
            y_points.append((graph_x, graph_y))
        if len(y_points) > 1:
            pygame.draw.lines(window, (0, 255, 0), False, y_points, 2)
            window.blit(write_text("Y", 20, YELLOW), (graph_y_area.left + 5, graph_y_area.top + 5))

    def draw_cartesian_axes(self, window, graph_area, max_value, label):
        pygame.draw.line(window, WHITE, (graph_area.left, graph_area.bottom), (graph_area.right, graph_area.bottom), 1)
        pygame.draw.line(window, WHITE, (graph_area.left, graph_area.top), (graph_area.left, graph_area.bottom), 1)
        ticks = 5
        for i in range(ticks + 1):
            y = graph_area.bottom - i * (graph_area.height / ticks)
            value = i / ticks * max_value
            tick_text = write_text(f"{value:.0f}", 15, WHITE)
            window.blit(tick_text, (graph_area.left - tick_text.get_width() - 5, y - tick_text.get_height() / 2))
            pygame.draw.line(window, WHITE, (graph_area.left, y), (graph_area.left + 5, y), 1)

        num_ticks = 5
        for i in range(num_ticks + 1):
            x = graph_area.left + i * (graph_area.width / num_ticks)
            tick_val = int(i * (len(self.history) / num_ticks)) if self.history else 0
            tick_text = write_text(f"{tick_val}", 15, WHITE)
            window.blit(tick_text, (x - tick_text.get_width() / 2, graph_area.bottom + 5))
            pygame.draw.line(window, WHITE, (x, graph_area.bottom), (x, graph_area.bottom - 5), 1)
        window.blit(write_text(label, 20, YELLOW), (graph_area.left + 5, graph_area.top + 5))

    def update(self):
        if not self.dragging:
            self.apply_physics()
        self.history.append(self.particle["pos"].copy())
        if len(self.history) > 300:
            self.history.pop(0)

        poly_x, poly_y = self.ml_model_eq.fit_equations(self.history)
        if poly_x is not None and poly_y is not None:
            self.eq_x_str = self.ml_model_eq.poly_to_string(poly_x)
            self.eq_y_str = self.ml_model_eq.poly_to_string(poly_y)
            t_future = len(self.history)
            predicted_x = poly_x(t_future)
            predicted_y = poly_y(t_future)
            self.predicted_pos = Vector2(predicted_x, predicted_y)

    def apply_physics(self):
        direction = self.particle["pos"] - self.anchor
        length = direction.length()
        unit_direction = direction.normalize() if length > 0 else Vector2(0, 0)
        stretch = length - self.spring["rest_length"]
        self.last_stretch = stretch

        force = -self.spring["k"] * stretch * unit_direction if length > 0 else Vector2(0, 0)
        force += -self.spring["damping"] * self.particle["vel"]
        force += self.gravity * self.particle["mass"]
        self.last_force = force

        acceleration = force / self.particle["mass"]
        self.last_acceleration = acceleration
        self.particle["vel"] += acceleration
        self.particle["pos"] += self.particle["vel"]

    def process(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.spring["k"] += 0.1
            elif event.key == pygame.K_s:
                self.spring["k"] = max(0, self.spring["k"] - 0.1)
            elif event.key == pygame.K_e:
                self.spring["damping"] += 0.1
            elif event.key == pygame.K_d:
                self.spring["damping"] = max(0, self.spring["damping"] - 0.1)
            elif event.key == pygame.K_r:
                self.fps += 5
            elif event.key == pygame.K_f:
                self.fps = max(5, self.fps - 5)
        mouse_pos = Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.particle["pos"].distance_to(mouse_pos) < self.particle["radius"]:
                self.dragging = True
                self.particle["vel"] = Vector2(0, 0)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.particle["pos"] = mouse_pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def set_state_machine(self, state_machine):
        self.state_machine = state_machine
        return self

    def load(self):
        self.particle["pos"] = Vector2(self.state_machine.window.get_width() / 2,
                                       self.state_machine.window.get_height() / 2)
        self.anchor = Vector2(self.state_machine.window.get_width() / 2,
                              self.state_machine.window.get_height() / 2 - 100)

