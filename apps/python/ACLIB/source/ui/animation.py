from util.log import console


class Animation:
    def __init__(self, target, var, start, step, stop, loops=0, direction='Forwards'):
        self.var = var
        self.target = target
        self.start = start
        self.step = step
        self.stop = stop

        self.direction = 'Forwards'
        self.loops = loops
        self.loop = 0
        self.progress = 0
        self.finished = False
        self.valid = False

        self.setDirection(direction)

        animation_var = getattr(self.target, self.var)
        if hasattr(type(animation_var), '__add__') and hasattr(type(animation_var), '__imul__') and \
                hasattr(type(animation_var), '__ne__') and hasattr(type(animation_var), '__eq__'):
            self.valid = True
            self.init()
        else:
            console('Class {} does not fulfill animation requirements.'.format(animation_var))

    def setDirection(self, direction):
        directions = ['Forwards', 'Backwards', 'Alternate']
        if isinstance(direction, str):
            if direction in directions:
                self.direction = direction
        elif isinstance(direction, int):
            self.direction = directions[direction]

        return self

    def setLoops(self, loops=0):
        self.loops = loops
        return self

    def isFinished(self):
        return self.finished

    def isValid(self):
        return self.valid

    def init(self):
        if getattr(self.target, self.var) != self.start:
            setattr(self.target, self.var, self.start)
        return self

    def update(self, delta):
        if self.valid:
            val = getattr(self.target, self.var)

            if self.direction == 'Forwards':
                if val != self.stop:
                    setattr(self.target, self.var, (val + self.step))
                else:
                    if self.loop >= self.loops != -1:
                        self.finished = True
                    self.loop += 1
                    self.init()

            elif self.direction == 'Alternate':
                if val != self.start or self.progress == 0:
                    if val == self.stop:
                        self.step *= -1
                    setattr(self.target, self.var, (val + self.step))
                    self.progress = 1
                else:
                    if self.loop >= self.loops != -1:
                        self.finished = True
                    self.loop += 1
                    self.step *= -1
                    self.progress = 0
