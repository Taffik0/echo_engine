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

    def _draw(self, record: DrawQueueRecord, screen: Surface):
        screen_size = Vector2(*screen.get_size())
        cam = self.transform

        # позиция объекта в долях камеры (0..1)
        rel_x = (record.transform.position.x - cam.position.x) / cam.size.x
        rel_y = (record.transform.position.y - cam.position.y) / cam.size.y

        # преобразуем в пиксели
        screen_x = rel_x * screen_size.x
        screen_y = rel_y * screen_size.y

        # размеры спрайта
        surf_w, surf_h = record.surface.get_size()

        # масштаб камеры
        unit_scale_x = screen_size.x / (cam.size.x * self.pixels_per_unit)
        unit_scale_y = screen_size.y / (cam.size.y * self.pixels_per_unit)

        draw_w = surf_w * unit_scale_x
        draw_h = surf_h * unit_scale_y

        if record.is_scaling:
            draw_w *= record.transform.size.x
            draw_h *= record.transform.size.y

        # применяем выравнивание
        screen_x += draw_w * record.alignment.x
        screen_y += draw_h * record.alignment.y

        # финальный рендер
        screen.blit(
            pygame.transform.scale(record.surface, (int(draw_w), int(draw_h))),
            (int(screen_x), int(screen_y))
        )
