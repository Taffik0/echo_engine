from .ui import UI


class UiList:
    def __init__(self, ui_elements: list[UI]):
        self.ui_elements: list[UI] = ui_elements

    def list(self):
        return self.ui_elements

    def get_element_by_name(self, name):
        for element in self.ui_elements:
            if element.name == name:
                return element
