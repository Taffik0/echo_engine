from attribute_modifier import AttributeModifier


class ModifierSystem:
    modifiers: list[AttributeModifier] = []

    @classmethod
    def update(cls, dt: float):
        pass

    @classmethod
    def add_modifier(cls, modifier: AttributeModifier):
        cls.modifiers.append(modifier)
        modifier.apply()

    @classmethod
    def remove_modifier(cls, modifier: AttributeModifier):
        cls.modifiers.remove(modifier)
        modifier.cansel()
