class EventListener:
    """
    An EventListener holds events and assigned functions to this event.
    Once an event is called all function associated with this event are called.
    """
    def __init__(self):
        self._callbacks = {}
        self._callback_id = 0

    def fire(self, event: str, *args):
        """
        Calls the given event name and executes all associated functions.
        :param event: str   Name of the event.
        :param args: tuple  Parameters that are given to the callback functions.
        """
        if event in self._callbacks:
            for _, callback in self._callbacks[event].items():
                if len(args) > 0:
                    callback(*args)
                else:
                    callback()

    def on(self, event: str, callback: callable):
        """
        Registers an event and an associated callback function.
        The callback function is stored with an unique id.
        :param event: str           Name of the event.
        :param callback: callable   Callback function.
        :return: tuple              Name of the event and the unique id.
        """
        if event not in self._callbacks:
            self._callbacks[event] = {}

        callback_id = self._callback_id
        self._callbacks[event][callback_id] = callback
        self._callback_id += 1

        return event, callback_id

    def remove(self, unique_id: tuple):
        """
        Removes an event from the EventListener
        :param unique_id: tuple     Contains the name of the event and the unique id assigned in 'on'.
        """
        if len(unique_id) == 2:
            event_id = unique_id[0]
            callback_id = unique_id[1]
            if event_id in self._callbacks:
                if callback_id in self._callbacks[event_id]:
                    del self._callbacks[event_id][callback_id]

