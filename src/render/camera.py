from pygame import Surface

from src.physics.transform import Transform


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

    def add_to_draw_queue(self, surface: Surface, entity):
        if self._surface_in_camera(surface, entity):
            x_size_px, y_size_px = surface.get_size()
            # вычисляем экранные координаты с учётом камеры
            screen_x = (entity.transform.position.x - self.transform.position.x) * self.pixels_per_unit
            screen_y = (entity.transform.position.y - self.transform.position.y) * self.pixels_per_unit
            self.draw_queue.append((surface, (screen_x, screen_y)))

    def draw(self):
        pass
