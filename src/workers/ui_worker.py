from src.systems.event_system import EventSystem

from .worker_register import add_worker
from .worker import Worker

from src.game_manager import GameManager
from src.render.canvas import Canvas

from src.ui.label import Label
from ..physics.transform import TransformUI
from ..physics.vectors import Vector2
from ..settings import CENTER, GRAY


class UIWorker(Worker):
    def __init__(self):
        super().__init__()
        EventSystem.reg_event("start", self.start)
        EventSystem.reg_event("end_game", self.game_end)
        EventSystem.reg_event("reset", self.reset)
        self.canvas: Canvas | None = None

    def start(self):
        self.canvas = GameManager.get_canvases()[0]

    def reset(self):
        self.canvas = GameManager.get_canvases()[0]
        """pygame.draw.rect(self.screen, (40, 60, 80), (15, 15, bar_w, bar_h), border_radius=6)
        ratio = clamp(self.player.focus / FOCUS_MAX, 0.0, 1.0)
        pygame.draw.rect(self.screen, FOCUS_COLOR, (15, 15, int(bar_w * ratio), bar_h), border_radius=6)
        self.screen.blit(self.font.render("FOCUS", True, WHITE), (15, 28))

        # score
        self.screen.blit(self.font.render(f"Score: {int(self.score)}", True, WHITE), (WIDTH - 170, 12))
        self.screen.blit(self.font.render(f"Best:  {self.high}", True, GRAY), (WIDTH - 170, 32))"""

    def update(self, dt):
        pass

    def game_end(self):
        self.canvas.add_ui(Label(text="GAME OVER",
                                      transform=TransformUI(position=Vector2(CENTER[0], CENTER[1] - 15),
                                                            size_px=Vector2(300, 80)),
                                      font_size=48, text_auto_scale=False, text_color=GRAY, alignment="c",
                                      size_by_font=True))
        self.canvas.add_ui(Label(text="R - restart    ESC - quit",
                                      transform=TransformUI(position=Vector2(CENTER[0], CENTER[1] + 15),
                                                            size_px=Vector2(300, 80)),
                                      font_size=20, text_auto_scale=False, text_color=GRAY, alignment="c",
                                      size_by_font=True))
        self.canvas.add_ui(Label(text="Tip: Grab green orbs to cash-in echoes!",
                                      transform=TransformUI(position=Vector2(CENTER[0], CENTER[1] + 36),
                                                            size_px=Vector2(300, 80)),
                                      font_size=20, text_auto_scale=False, text_color=GRAY, alignment="c",
                                      size_by_font=True))


worker = UIWorker()
add_worker(worker)
