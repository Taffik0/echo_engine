class Entity:
    collider = None
    color = (0, 0, 0)
    x = 0
    y = 0

    def update(self, dt):
        pass

    def draw(self, surf):
        pass

    def start(self):
        pass

    def destroy(self):
        pass

    def on_collision(self, other):
        pass
