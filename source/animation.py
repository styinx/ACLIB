from source.aclib import ACLIB


class Animation:
    def __init__(self, target, var, start, step, stop):
        self.var = var
        self.target = target
        self.start = start
        self.step = step
        self.stop = stop

        self.direction = "Forwards"
        self.loops = 0
        self.loop = 0
        self.progress = 0
        self.finished = False

    def setDirection(self, direction):
        if direction in ["Forwards", "Backwards", "Alternate"]:
            self.direction = direction

        return self

    def setLoops(self, loops=0):
        self.loops = loops
        return self

    def isFinished(self):
        return self.finished

    def init(self):
        if getattr(self.target, self.var) != self.start:
            setattr(self.target, self.var, self.start)
        return self

    def update(self, delta):
        val = getattr(self.target, self.var)

        if self.direction == "Forwards":
            if val != self.stop:
                setattr(self.target, self.var, (val + self.step))
            else:
                if self.loop >= self.loops:
                    self.finished = True
                self.loop += 1
        if self.direction == "Alternate":
            if self.progress == 0 or val != self.start:
                if val == self.stop:
                    self.step *= -1
                setattr(self.target, self.var, (val + self.step))
                self.progress = 1
            else:
                if self.loop >= self.loops:
                    self.finished = True
                self.loop += 1
