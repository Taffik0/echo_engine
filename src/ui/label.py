import pygame
from pygame import Surface

from src.physics.vectors import Vector2, Vector2N
from src.physics.transform import Transform
from src.render.surface_manager import create_surface_by_react

from src.ui.ui import UI


class Label(UI):
    def __init__(self, text: str = "", text_alignment: str = "l",
                 font: str = "consolas", text_auto_scale: bool = True, font_size: int = 30,
                 text_color: tuple = (255, 255, 255), size_by_font: bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = text
        self.text_alignment = text_alignment
        self.font = pygame.font.SysFont(font, font_size)
        self.text_auto_scale = text_auto_scale
        self.text_color = text_color
        self.size_by_font = size_by_font

    def draw(self) -> Surface:
        text_surface = self.font.render(self.text, True, self.text_color)

        if self.size_by_font:
            self.transform.size_px = Vector2(text_surface.get_width(), text_surface.get_height())
        my_size = self.get_global_size()
        sur = create_surface_by_react(my_size.x, my_size.y)

        if self.text_auto_scale:
            current_height = text_surface.get_height()
            target_height = sur.get_height()
            if current_height > 0:
                scale_factor = target_height / current_height
                new_width = int(text_surface.get_width() * scale_factor)
                text_surface = pygame.transform.scale(text_surface, (new_width, target_height))

        # вычисляем позицию по выравниванию
        text_rect = text_surface.get_rect()
        surf_rect = sur.get_rect()

        if self.text_alignment == "c":
            text_rect.center = surf_rect.center
        elif self.text_alignment == "r":
            text_rect.midright = surf_rect.midright
        else:  # left
            text_rect.midleft = surf_rect.midleft

        # рисуем
        sur.blit(text_surface, text_rect)
        return sur
