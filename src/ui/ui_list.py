from .ui import UI


class UiList:
    def __init__(self, ui_elements):
        self.ui_elements = ui_elements

    def list(self):
        return self.ui_elements