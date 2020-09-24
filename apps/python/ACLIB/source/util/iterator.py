# Iterator that starts again from the beginning after the last item has been reached.
class EndlessIterator:
    def __init__(self, collection):
        self.step = 1
        self.index = 0
        self.collection = collection
        self.len = len(self.collection) - 1

    def __getitem__(self, item):
        return self.collection[self.index]

    def __next__(self):
        return self.next()

    def next(self):
        el = self.collection[self.index]

        if 0 <= self.index + self.step <= self.len:
            self.index += self.step
        else:
            self.index = (self.index + self.step) % self.len + 1

        return el

    def prev(self):
        el = self.collection[self.index]

        if 0 <= self.index - self.step <= self.len:
            self.index -= self.step
        else:
            self.index = (self.index - self.step) % self.len + 1

        return el

    def __iadd__(self, other):
        for i in range(0, other):
            self.next()
        return self

    def __add__(self, other):
        for i in range(0, other):
            self.next()