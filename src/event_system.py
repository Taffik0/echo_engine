import inspect


class EventSystem:
    _event_register = {}

    @classmethod
    def reg_event(cls, event_name, method):
        if event_name in cls._event_register:
            cls._event_register[event_name].append(method)
        else:
            cls._event_register[event_name] = [method]

    @classmethod
    def trigger_event(cls, event_name, *args, **kwargs):
        """Вызвать событие, передав аргументы"""
        if event_name not in EventSystem._event_register:
            return

        for callback in EventSystem._event_register[event_name]:
            sig = inspect.signature(callback)
            try:
                # Смотрим сколько аргументов принимает метод
                bound = sig.bind_partial(*args, **kwargs)
                callback(*bound.args, **bound.kwargs)
            except TypeError:
                # Игнорируем лишние аргументы, если метод принимает меньше.
                # Используем только те аргументы, которые реально принимает callback.
                filtered_args = args[:len(sig.parameters)]
                callback(*filtered_args)

    @classmethod
    def unregister_event(cls, event_name, method):
        if event_name in cls._event_register:
            cls._event_register[event_name].remove(method)
            if not cls._event_register[event_name]:
                del cls._event_register[event_name]
