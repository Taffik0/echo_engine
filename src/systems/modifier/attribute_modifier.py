class Ref:
    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

    def get(self):
        return getattr(self.obj, self.attr)

    def set(self, value):
        setattr(self.obj, self.attr, value)


class AttributeModifier:
    def __init__(self, ref: Ref, op="mul", value=1.0, duration=None):
        self.ref = ref
        self.op = op
        self.value = value
        self.duration = duration

    def apply(self):
        v = self.ref.get()
        if self.op == "mul":
            self.ref.set(v * self.value)

    def cansel(self):
        v = self.ref.get()
        if self.op == "mul":
            self.ref.set(v / self.value)
