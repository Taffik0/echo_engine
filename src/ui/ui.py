import pygame
from pygame import Surface
from typing import Optional

from src.render.surface_manager import create_surface_by_react

from src.physics.transform import TransformUI
from src.physics.vectors import Vector2
from src.render.alignment import alignment_dict


class UI:
    def __init__(self, layer: int = 0, transform: TransformUI = None, draw_alignment: str = "ld", alignment: str = "ld",
                 parent: Optional["UI"] = None, children: Optional[list["UI"]] = None):
        self.transform = transform
        if transform is None:
            self.transform = TransformUI(alignment=alignment, draw_alignment=draw_alignment)
        self.alignment = alignment
        self.draw_alignment = draw_alignment
        self.layer = layer

        self.parent = parent
        self.children = []
        if children:
            self.children = children

    def draw(self) -> Surface:
        pass

    def get_global_size(self) -> Vector2:
        size = self.transform.size_px
        if self.parent:
            parent_size = self.parent.get_global_size()
            size += Vector2(parent_size.x * self.transform.relative_size.x,
                            parent_size.y * self.transform.relative_size.y)
        return size

    def get_global_position(self) -> Vector2:
        position = self.transform.position
        if self.parent:
            parent_size = self.parent.get_global_size()
            position += Vector2(parent_size.x * self.transform.relative_position.x,
                                parent_size.y * self.transform.relative_position.y)
        size = self.get_global_size()
        return position + (size * alignment_dict[self.alignment])
