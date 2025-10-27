import pygame
from .worker import Worker
from .worker_register import WorkerRegister
from src.systems.user_imput.user_input_system import UserInputSystem, KeyEvent
from src.systems.event_system import EventSystem

from src.ui.label import Label
from src.ui.slider import Slider
from src.render.canvas import Canvas

from src.physics.transform import TransformUI
from src.physics.vectors import Vector2

from src.game_manager import GameManager
from src.utility import clamp


class TimeSlowWorker(Worker):
    def __init__(self):
        super().__init__()
        self.slow_factor = 1.0
        self.focus = 60
        self.focus_max = 100
        self.time_stopped = False
        EventSystem.reg_event("start", self.start)
        EventSystem.reg_event("end_game", self.game_end)
        EventSystem.reg_event("reset", self.reset)
        EventSystem.reg_event("lastUpdate", self.last_update)
        EventSystem.reg_event("init", self.init)
        self.canvas: Canvas | None = None
        self.focus_lb = None
        self.slider = None

    def init(self):
        bar_w, bar_h = 180, 10
        self.slider = Slider(slider_color=(120, 200, 255), background_color=(40, 60, 80),
                             transform=TransformUI(size_px=Vector2(180, 10), position=Vector2(15, 15)),
                             max_value=100, value=60, border_radius=6)
        self.focus_lb = Label(text="FOCUS", font_size=20,
                              transform=TransformUI(position=Vector2(15, 30)), text_color=(255, 255, 255),
                              text_auto_scale=False, size_by_font=True)

    def start(self):
        self.canvas = GameManager.get_canvases()[0]
        UserInputSystem.registration_event(KeyEvent(225, self.time_slow, on_hold=True))
        print("time slow started")
        self.canvas.add_ui(self.focus_lb)
        self.canvas.add_ui(self.slider)

    def time_slow(self, dt=1):
        self.time_stopped = True
        if self.focus > 0:
            self.slow_factor = 0.55
            self.focus = clamp(self.focus - 45 * dt, 0, 100)
        GameManager.game.slow_factor = self.slow_factor

    def reset(self):
        self.canvas = GameManager.get_canvases()[0]
        if self.focus_lb:
            self.canvas.add_ui(self.focus_lb)
            self.canvas.add_ui(self.slider)

    def update(self, dt):
        if self.focus < self.focus_max and not self.time_stopped:
            self.focus = clamp(self.focus + 45 * dt, 0, self.focus_max)
        self.slider.value = int(self.focus)

    def last_update(self):
        GameManager.game.slow_factor = self.slow_factor
        self.slow_factor = 1.0
        self.time_stopped = False

    def game_end(self):
        pass


worker = TimeSlowWorker()
WorkerRegister.add_worker(worker)
