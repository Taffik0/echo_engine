class Spawner:
    def __init__(self, spawn_delay, diff_delay_mult, diff_delay, factory):
        self.spawn_delay = spawn_delay
        self.start_spawn_delay = spawn_delay

        self.spawn_time = 0
        self.diff_time = 0

        self.diff_delay_mult = diff_delay_mult
        self.diff_delay = diff_delay
        self.start_diff_delay = diff_delay
        self.factory = factory

    def update(self, dt):
        self.spawn_time += dt
        self.diff_time += dt

        if self.diff_time >= self.diff_delay:
            self.diff_time = 0
            self.diff_add()

        if self.spawn_time >= self.spawn_delay:
            self.spawn_time = 0
            self.spawn()

    def spawn(self):
        pass

    def diff_add(self):
        self.spawn_delay *= self.diff_delay_mult

    def reset(self):
        self.spawn_time = 0
        self.diff_time = 0
        self.spawn_delay = self.start_spawn_delay
        self.start_diff_delay = self.start_diff_delay
