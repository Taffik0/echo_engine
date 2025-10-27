from .worker import Worker
from .worker_register import WorkerRegister
from src.systems.global_variables import *
from src.systems.event_system import EventSystem
from src.game_manager import GameManager

from src.ui.label import Label
from src.physics.transform import TransformUI
from src.physics.vectors import Vector2

from src.settings import GRAY, FPS


class ScoreWorker(Worker):
    def __init__(self):
        super().__init__()
        GlobalVariablesSystem.set_or_create("score", 0)
        GlobalVariablesSystem.set_or_create("high", 0, is_saving=True)
        EventSystem.reg_event("init", self.init)
        EventSystem.reg_event("reset", self.reset)
        EventSystem.reg_event("end_game", self.end_game)
        self.canvas = None
        self.score_lb: Label = None
        self.high_lb: Label = None

    def init(self):
        self.canvas = GameManager.get_canvases()[0]
        canvas_size = self.canvas.get_global_size()
        score = GlobalVariablesSystem.get_variable("score")
        high = GlobalVariablesSystem.get_variable("high")
        self.score_lb = Label(text=f"Score: {score}", font_size=20, size_by_font=True,
                              transform=TransformUI(position=Vector2(canvas_size.x - 170, 12)))
        self.high_lb = Label(text=f"Best:  {high}", font_size=20, size_by_font=True, text_color=GRAY,
                             transform=TransformUI(position=Vector2(canvas_size.x - 170, 32)))
        self.canvas.add_ui(self.score_lb)
        self.canvas.add_ui(self.high_lb)

    def reset(self):
        self.canvas = GameManager.get_canvases()[0]
        GlobalVariablesSystem.set_or_create("score", 0)
        if self.score_lb:
            self.score_lb.text = f"Score: {int(0)}"
            self.canvas.add_ui(self.score_lb)
            self.canvas.add_ui(self.high_lb)

    def update(self, dt):
        score = GlobalVariablesSystem.get_variable("score")
        score += FPS*dt
        GlobalVariablesSystem.set_or_create("score", score)
        self.score_lb.text = f"Score: {int(score)}"

    def end_game(self):
        score = GlobalVariablesSystem.get_variable("score")
        high = GlobalVariablesSystem.get_variable("high")
        high = max(high, int(score))
        GlobalVariablesSystem.set_or_create("high", high)
        if self.high_lb:
            self.high_lb.text = f"Best:  {high}"


WorkerRegister.add_worker(ScoreWorker())
