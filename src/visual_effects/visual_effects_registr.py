import bisect


class VisualEffectRegister:
    effects = []
    under_effects = []
    over_effects = []

    @classmethod
    def add(cls, effect, level):
        if level == 0:
            bisect.insort(cls.effects, (level, effect))
        elif level > 0:
            bisect.insort(cls.over_effects, (level, effect))
        elif level < 0:
            bisect.insort(cls.under_effects, (level, effect))

    @classmethod
    def remove(cls, effect):
        def _remove(lst):
            for i, (lvl, eff) in enumerate(lst):
                if eff == effect:
                    lst.pop(i)
                    break
        _remove(cls.effects)
        _remove(cls.under_effects)
        _remove(cls.over_effects)

    @classmethod
    def _draw_list(cls, lst, surface, dt):
        for level, effect in lst:
            effect.draw(surface, dt)

    @classmethod
    def draw(cls, surface, dt):
        cls._draw_list(cls.effects, surface, dt)

    @classmethod
    def under_draw(cls, surface, dt):
        cls._draw_list(cls.under_effects, surface, dt)

    @classmethod
    def over_draw(cls, surface, dt):
        cls._draw_list(cls.over_effects, surface, dt)