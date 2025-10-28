import bisect


class VisualEffectRegister:
    def __init__(self):
        self.effects = []
        self.under_effects = []
        self.over_effects = []

    def add(self, effect, level):
        if level == 0:
            bisect.insort(self.effects, (level, effect))
        elif level > 0:
            bisect.insort(self.over_effects, (level, effect))
        elif level < 0:
            bisect.insort(self.under_effects, (level, effect))

    def remove(self, effect):
        def _remove(lst):
            for i, (lvl, eff) in enumerate(lst):
                if eff == effect:
                    lst.pop(i)
                    break
        _remove(self.effects)
        _remove(self.under_effects)
        _remove(self.over_effects)

    def _draw_list(self, lst, surface, dt):
        for level, effect in lst:
            effect.draw(surface, dt)

    def draw(self, surface, dt):
        self._draw_list(self.effects, surface, dt)

    def under_draw(self, surface, dt):
        self._draw_list(self.under_effects, surface, dt)

    def over_draw(self, surface, dt):
        self._draw_list(self.over_effects, surface, dt)