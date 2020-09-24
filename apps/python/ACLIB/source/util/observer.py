class Observer:
    def update_observer(self, subject):
        raise NotImplementedError('Override this function!')

class Subject:
    def __init__(self):
        self._observers = []

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify_observers(self):
        for o in self._observers:
            o.update_observer(self)
