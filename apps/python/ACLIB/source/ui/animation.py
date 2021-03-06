class Animation:
    def __init__(self, target, var: str, start, step, stop, loops: int = 0, direction: str = 'Forwards'):
        self.var = var
        self.target = target
        self.start = start
        self.step = step
        self.stop = stop

        self.direction = 'Forwards'
        self.loops = loops
        self.loop = 0
        self.progress = 0
        self._finished = False
        self._valid = False

        self.set_direction(direction)

        animation_var = getattr(self.target, self.var)
        has_required_methods = hasattr(type(animation_var), '__add__')
        has_required_methods &= hasattr(type(animation_var), '__imul__')
        has_required_methods &= hasattr(type(animation_var), '__eq__')
        has_required_methods &= hasattr(type(animation_var), '__ne__')

        if has_required_methods:
            self._valid = True
            self.init()
        else:
            raise Exception('Parameter {} of class {} does not fulfill animation requirements.'.format(
                var, target.__class__.__name__))

    def set_direction(self, direction: str):
        if direction in ['Forwards', 'Backwards', 'Alternate']:
            self.direction = direction

    def set_loops(self, loops: int = 0):
        self.loops = loops

    def is_finished(self):
        return self._finished

    def is_valid(self):
        return self._valid

    def init(self):
        if getattr(self.target, self.var) != self.start:
            setattr(self.target, self.var, self.start)
        return self

    def update(self):
        if self._valid:
            val = getattr(self.target, self.var)

            if self.direction == 'Forwards':
                if val != self.stop:
                    setattr(self.target, self.var, (val + self.step))

                else:
                    if self.loop >= self.loops != -1:
                        self._finished = True
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
                        self._finished = True

                    self.loop += 1
                    self.step *= -1
                    self.progress = 0
