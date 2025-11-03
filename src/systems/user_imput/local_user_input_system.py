import pygame
import inspect

from src.settings import KEY_INPUT_LOG


def call_with_available_args(method, **possible_args):
    # получаем имена параметров метода
    sig = inspect.signature(method)
    params = sig.parameters

    # оставляем только те аргументы, которые есть в сигнатуре
    filtered_args = {k: v for k, v in possible_args.items() if k in params}
    return method(**filtered_args)


class InputKey:
    def __init__(self, key, time):
        self.key = key
        self.time = time


class KeyEvent:
    def __init__(self, key, method, on_down=False, on_hold=False, on_up=False):
        self.key = key
        self.method = method
        self.on_down = on_down
        self.on_hold = on_hold
        self.on_up = on_up


class LocalUserInputSystem:
    def __init__(self):
        self.keys = {}
        self.key_events = {}

    def update(self, dt):
        pressed = pygame.key.get_pressed()
        for key_code, is_pressed in enumerate(pressed):
            if is_pressed:
                if KEY_INPUT_LOG:
                    print(key_code)
                if key_code in self.keys:
                    self.keys[key_code].time += dt
                    if key_code in self.key_events:
                        for event in self.key_events[key_code]:
                            if event.on_hold:
                                call_with_available_args(event.method, time=self.keys[key_code].time, dt=dt)
                else:
                    self.keys[key_code] = InputKey(key_code, dt)
                    if key_code in self.key_events:
                        for event in self.key_events[key_code]:
                            if event.on_down:
                                call_with_available_args(event.method, time=self.keys[key_code].time, dt=dt)
            else:
                if key_code in self.keys:
                    if key_code in self.key_events:
                        for event in self.key_events[key_code]:
                            if getattr(event, "on_up", False):
                                call_with_available_args(event.method, time=self.keys[key_code].time, dt=dt)
                    self.keys.pop(key_code)

    def registration_event(self, key_event: KeyEvent):
        """Подписывание на событие пользовательского ввода"""
        key = key_event.key
        if key in self.key_events:
            self.key_events[key].append(key_event)
        else:
            self.key_events[key] = [key_event]

    def unregister_event(self, key_event: KeyEvent):
        """Аннулирование подписи на событие пользовательского ввода"""
        self.key_events.pop(key_event)

    def get_key(self, key):
        """Получение клавиши ввода если такая есть"""
        if key in self.keys:
            return self.keys[key]
        else:
            return None

