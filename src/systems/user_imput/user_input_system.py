import pygame


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


class UserInputSystem:
    keys = {}
    key_events = {}

    @classmethod
    def update(cls, dt):
        pressed = pygame.key.get_pressed()
        for key_code, is_pressed in enumerate(pressed):
            if is_pressed:
                if key_code in cls.keys:
                    cls.keys[key_code].time += dt
                    if key_code in cls.key_events:
                        for event in cls.key_events[key_code]:
                            if not event.on_down:
                                event.method(cls.keys[key_code].time)
                else:
                    cls.keys[key_code] = InputKey(key_code, dt)
                    if key_code in cls.key_events:
                        for event in cls.key_events[key_code]:
                            if event.on_hold:
                                event.method(cls.keys[key_code].time)
            else:
                if key_code in cls.keys:
                    if key_code in cls.key_events:
                        for event in cls.key_events[key_code]:
                            if getattr(event, "on_up", False):
                                event.method(cls.keys[key_code].time)
                    cls.keys.pop(key_code)

    @classmethod
    def registration_event(cls, key_event: KeyEvent):
        key = key_event.key
        if key in cls.key_events:
            cls.key_events[key].append(key_event)
        else:
            cls.key_events[key] = [key_event]

