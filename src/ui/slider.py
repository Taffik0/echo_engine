import pygame
from pygame import Surface

from src.render.surface_manager import create_surface_by_react
from .ui import UI


class Slider(UI):
    def __init__(self, background_color=(100, 100, 100), slider_color=(255, 255, 255),
                 max_value=100, value=0,
                 border_radius=0,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_color = background_color
        self.slider_color = slider_color
        self.max_value = max_value
        self.value = value
        self.border_radius = border_radius

    def draw(self) -> Surface:
        my_size = self.get_global_size()
        sur = create_surface_by_react(my_size.x, my_size.y)
        pygame.draw.rect(sur, self.background_color, (0, 0, my_size.x, my_size.y),
                         border_radius=self.border_radius)
        persent = self.value / self.max_value
        pygame.draw.rect(sur, self.slider_color, (0, 0, int(my_size.x*persent), my_size.y),
                         border_radius=self.border_radius)
        return sur
