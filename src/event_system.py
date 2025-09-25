class EventSystem:
    _event_register = {}

    @classmethod
    def reg_event(cls, event_name, method):
        if event_name in cls._event_register:
            cls._event_register[event_name].append(method)
        else:
            cls._event_register[event_name] = [method]

    @classmethod
    def trigger_event(cls, event_name):
        if event_name in cls._event_register:
            for method in cls._event_register[event_name]:
                method()

    @classmethod
    def unregister_event(cls, event_name, method):
        if event_name in cls._event_register:
            cls._event_register[event_name].remove(method)
            if not cls._event_register[event_name]:
                del cls._event_register[event_name]
