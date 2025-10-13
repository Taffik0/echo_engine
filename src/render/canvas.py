from pygame import Surface
from src.physics.vectors import Vector2
from src.physics.transform import Transform

from src.ui.ui import UI


alignment_draw_dict = {
    "c": Vector2(-0.5, -0.5),
    "ld": Vector2(0, 0),
    "lf": Vector2(0, -1),
    "rd": Vector2(-1, 0),
    "rf": Vector2(-1, -1)
}


class DrawQueueRecord:
    def __init__(self, surface: Surface, position: Vector2,size: Vector2 , ui_element: UI, alignment_draw: Vector2):
        self.surface = surface
        self.position = position
        self.size = size
        self.ui_element = ui_element
        self.alignment_draw = alignment_draw


class Canvas:
    def __init__(self, transform, pixels_per_unit):
        self.transform: Transform = transform
        self.pixels_per_unit = pixels_per_unit
        self.draw_queue = []

        self.ui_elements = []

    def get_global_size(self):
        unit_size = self.transform.size
        return Vector2(unit_size.x * self.pixels_per_unit,
                       unit_size.y * self.pixels_per_unit)

    def get_global_position(self) -> Vector2:
        position = self.transform.position
        return Vector2(position.x * self.pixels_per_unit,
                       position.y * self.pixels_per_unit)

    def add_ui(self, ui_element: UI):
        """Добавить элемент на канвас и назначить ему parent"""
        ui_element.parent = self
        self.ui_elements.append(ui_element)

    def _surface_in_canvas(self, ui_element: UI):
        position = ui_element.get_global_position()
        size = ui_element.get_global_size()
        my_position = self.get_global_position()
        my_size = self.get_global_size()
        return not (my_position.x + my_size.x < position.x or
                    my_position.x > position.x + size.x or
                    my_position.y + my_size.y < position.y or
                    my_position.y > position.y + size.y)

    def add_to_draw_queue(self, surface: Surface, ui_element: UI, alignment: str = "c"):
        if self._surface_in_canvas(ui_element):
            position = ui_element.get_global_position()
            size = ui_element.get_global_size()
            self.draw_queue.append(DrawQueueRecord(surface, position, size, ui_element,
                                   alignment_draw=alignment_draw_dict[alignment]))

    def add_to_draw_queue_all_ui(self):
        for ui_element in self.ui_elements:
            surface = ui_element.draw()
            self.add_to_draw_queue(surface, ui_element)

    def drawing_queue(self, screen: Surface):
        for draw_queue_record in self.draw_queue:
            self.draw(draw_queue_record, screen)
        self.draw_queue.clear()

    def draw(self, draw_queue_record: DrawQueueRecord, screen: Surface):
        position = draw_queue_record.ui_element.get_global_position()
        surface = draw_queue_record.surface
        screen.blit(surface, (position.x, position.y))
