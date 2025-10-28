import xml.etree.ElementTree as ET

from .ui_list import UiList, UI

from .label import Label
from .slider import Slider

from src.physics.transform import TransformUI, Vector2, Vector2N

ui_tags = {
    "ui": None,
    "label": Label,
    "slider": Slider
}

TRANSFORM_FIELDS = {
    # Абсолютная позиция
    "x": ("position", Vector2, "x"),
    "y": ("position", Vector2, "y"),

    # Вращение
    "rx": ("rotation", Vector2, "x"),
    "ry": ("rotation", Vector2, "y"),

    # Относительная позиция
    "rpx": ("relative_position", Vector2N, "x"),
    "rpy": ("relative_position", Vector2N, "y"),

    # Относительный размер
    "rsx": ("relative_size", Vector2N, "x"),
    "rsy": ("relative_size", Vector2N, "y"),

    # Прочие параметры
    "is_sizing": ("is_sizing", bool, None),
    "alignment": ("alignment", str, None),
    "draw_alignment": ("draw_alignment", str, None),
}


class XMLUIReader:
    @staticmethod
    def _is_addable(a, b):
        if not hasattr(a, "__add__"):
            return False
        try:
            a + b
            return True
        except TypeError:
            return False
    @staticmethod
    def read_xml(xml_elements: str):
        root = ET.fromstring(xml_elements)
        elements = XMLUIReader.parse_element(root)
        return UiList(elements)

    @staticmethod
    def parse_element(node):
        elements = []
        transform, parse_elements = XMLUIReader.parse_transform_from_xml(node.attrib)
        if ui_tags[node.tag]:
            elements.append(ui_tags[node.tag](transform=transform, **parse_elements))
        # Рекурсивно пройтись по всем детям
        for child in node:
            elements += XMLUIReader.parse_element(child)
        return elements

    @staticmethod
    def parse_transform_from_xml(attrs: dict):
        transform = TransformUI()
        parse_attrs = XMLUIReader.parse_transform_attrs(attrs)
        for name, value, key in parse_attrs:
            attrs.pop(key)
            if XMLUIReader._is_addable(getattr(transform, name), value):
                setattr(transform, name, getattr(transform, name) + value)
            else:
                setattr(transform, name, value)
        return transform, attrs




    @staticmethod
    def parse_transform_attrs(attrs):
        parse_attrs = []
        for key, value in attrs.items():
            if key not in TRANSFORM_FIELDS:
                continue  # этот атрибут не из TransformUI

            field_name, field_type, axis = TRANSFORM_FIELDS[key]
            parse_attr = None

            if field_type == bool:
                value = str(value).lower() == "true"
                parse_attr = value
            elif field_type == str:
                pass
            else:
                value = float(value)
                parse_attr = value

                # 🧱 Если у нас подполе (например x у Vector2)
            if axis:
                obj = field_type()
                setattr(obj, axis, value)
                parse_attr = obj
            else:
                obj = field_type(value)
                parse_attr = obj

            parse_attrs.append((field_name, parse_attr, key))
        return parse_attrs
