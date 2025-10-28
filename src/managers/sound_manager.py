import pygame


class SoundManager:
    @classmethod
    def load_and_run_sound(cls, path: str, loops: int):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)
