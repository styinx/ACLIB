class EventListener:
    def __init__(self):
        self._callbacks = {}
        self._callback_id = 0

    def fire(self, event: str, *args):
        if event in self._callbacks:
            for _, callback in self._callbacks[event].items():
                if len(args) > 0:
                    callback(*args)
                else:
                    callback()

    def on(self, event: str, callback: callable):
        if event not in self._callbacks:
            self._callbacks[event] = {}

        callback_id = self._callback_id
        self._callbacks[event][callback_id] = callback
        self._callback_id += 1

        return event, callback_id

    def remove(self, unique_id: tuple):
        if len(unique_id) == 2:
            event_id = unique_id[0]
            callback_id = unique_id[1]
            if event_id in self._callbacks:
                if callback_id in self._callbacks[event_id]:
                    del self._callbacks[event_id][callback_id]

