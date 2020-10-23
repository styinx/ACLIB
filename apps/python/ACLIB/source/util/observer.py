from util.event import EventListener


class Observer:
    def update_observer(self, subject):
        raise NotImplementedError('Override this function!')

class Subject:
    def __init__(self):
        self._observers = []

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify_observers(self):
        for o in self._observers:
            o.update_observer(self)


class Observable:
    def __init__(self, parent: EventListener, initial_value: int, event: str):
        self._parent = parent
        self._value = initial_value
        self._event = event

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: int):
        if self._value != new_value:
            self._value = new_value

            self._parent.fire(self._event, self._value)


class IntervalObservable(Observable):
    def __init__(self, parent: EventListener, initial_value: int, less_event: str, more_event: str):
        super().__init__(parent, initial_value, '')

        self._parent = parent
        self._value = initial_value
        self._less_event = less_event
        self._more_event = more_event

    @Observable.value.setter
    def value(self, new_value: int):
        if self._value != new_value:
            if self._value < new_value:
                self._value = new_value
                self._parent.fire(self._more_event, self._value)
            else:
                self._value = new_value
                self._parent.fire(self._less_event, self._value)


class RangeObservable(Observable):
    def __init__(self, parent: EventListener, initial_value: int, change: float, event: str, absolute: bool = True):
        super().__init__(parent, initial_value, event)

        self._parent = parent
        self._value = initial_value
        self._absolute = absolute
        self._change = abs(change)

        if not absolute:
            self._change = max(1.0, self._change)

    @Observable.value.setter
    def value(self, new_value: int):
        if self._value != new_value:
            if self._absolute:
                yes = new_value < self._value - self._change or new_value > self._value + self._change
            else:
                yes = new_value < self._value * (1 - self._change) or new_value > self._value * (1 + self._change)
            if yes:
                self._value = new_value
                self._parent.fire(self._event, self._value)


class BoolObservable(Observable):
    def __init__(self, parent, initial_value: bool, true_event: str, false_event: str):
        super().__init__(parent, initial_value, '')

        self._parent = parent
        self._value = initial_value
        self._true_event = true_event
        self._false_event = false_event

    @Observable.value.setter
    def value(self, new_value: bool):
        if self._value != new_value:
            self._value = new_value
            if self._value:
                self._parent.fire(self._true_event)
            else:
                self._parent.fire(self._false_event)
