import pygame
from pygame import Surface

from src.physics.transform import Transform
from src.physics.vectors import Vector2

from src.entities.entity import Entity


alignment_dict = {
    "c": Vector2(-0.5, -0.5),
    "ld": Vector2(0, 0),
    "lf": Vector2(0, -1),
    "rd": Vector2(-1, 0),
    "rf": Vector2(-1, -1)
}


class DrawQueueRecord:
    def __init__(self, surface: Surface, position: Vector2, is_sizing: bool, transform: Transform, alignment: Vector2):
        self.surface = surface
        self.position = position
        self.is_scaling = is_sizing
        self.transform = transform
        self.alignment = alignment


class Camera:
    def __init__(self, transform, pixels_per_unit):
        self.transform: Transform = transform
        self.pixels_per_unit = pixels_per_unit
        self.draw_queue = []

    def _surface_in_camera(self, surface: Surface, entity):
        x_size_px, y_size_px = surface.get_size()
        x_size = x_size_px/self.pixels_per_unit
        y_size = y_size_px / self.pixels_per_unit
        if entity.transform.is_sizing:
            x_size = x_size*entity.transform.size.x
            y_size = y_size * entity.transform.size.y
        entity_transform = entity.transform
        return not (self.transform.position.x + self.transform.size.x < entity_transform.position.x or
                    self.transform.position.x > entity_transform.position.x + x_size or
                    self.transform.position.y + self.transform.size.y < entity_transform.position.y or
                    self.transform.position.y > entity_transform.position.y + y_size)

    def add_to_draw_queue(self, surface: Surface, entity: Entity, alignment: str = "c"):
        if self._surface_in_camera(surface, entity):
            x_size_px, y_size_px = surface.get_size()
            # вычисляем экранные координаты с учётом камеры
            screen_x = (entity.transform.position.x - self.transform.position.x) * self.pixels_per_unit
            screen_y = (entity.transform.position.y - self.transform.position.y) * self.pixels_per_unit
            self.draw_queue.append(DrawQueueRecord(surface, Vector2(screen_x, screen_y),
                                                   entity.transform.is_sizing, entity.transform,
                                                   alignment_dict[alignment]))

    def drawing_queue(self, screen: Surface):
        for draw_queue_record in self.draw_queue:
            self._draw(draw_queue_record, screen)
        self.draw_queue = []

    def _draw(self, draw_queue_record: DrawQueueRecord, screen: Surface):
        screen_size = Vector2(*screen.get_size())
        surface_size = Vector2(*draw_queue_record.surface.get_size())
        screen_pos_x = draw_queue_record.position.x * (screen_size.x / (self.transform.size.x * self.pixels_per_unit))
        screen_pos_y = draw_queue_record.position.y * (screen_size.y / (self.transform.size.y * self.pixels_per_unit))

        screen_pos_x += surface_size.x * draw_queue_record.alignment.x
        screen_pos_y += surface_size.y * draw_queue_record.alignment.y

        screen_pos_x = int(screen_pos_x)
        screen_pos_y = int(screen_pos_y)

        size_x = int(screen_size.x / (self.transform.size.x * self.pixels_per_unit)) * surface_size.x
        size_y = int(screen_size.y / (self.transform.size.y * self.pixels_per_unit)) * surface_size.y

        if draw_queue_record.is_scaling:
            size_x *= draw_queue_record.transform.size.x
            size_y *= draw_queue_record.transform.size.y

        scaled_surface = pygame.transform.scale(draw_queue_record.surface, (size_x, size_y))
        screen.blit(scaled_surface, (screen_pos_x, screen_pos_y))
