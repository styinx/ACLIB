class EventDispatcher:
    events = {}

    def addEvent(self, name, event):
        EventDispatcher.events[name] = event

    def dispatchEvent(self, name):
        EventDispatcher.events[name]()
