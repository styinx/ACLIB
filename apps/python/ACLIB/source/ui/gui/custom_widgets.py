import ac
from ui.color import Color
from ui.gui.widget import ACWidget
from ui.gl import rect


# TODO still legacy


class ProgressBar(ACWidget):
    def __init__(self, orientation: int = 0, value: int = 0, min_val: int = 0, max_val: int = 100,
                 parent: ACWidget = None):
        super().__init__(parent)

        self.orientation = orientation
        self.border = 1
        self.color = Color(1, 0, 0)
        self.h_margin = 1
        self.v_margin = 0.05
        self.value = value
        self.min_val = min_val
        self.max_val = max(max_val, 1)

        if orientation == 1:
            self.h_margin = 0.05
            self.v_margin = 1

    def render(self, delta):
        x, y = self.position
        w, h = self.size

        if self.orientation == 0:
            v_margin = h * self.v_margin
            ratio = w * (self.value / self.max_val)
            rect(x, y + v_margin, ratio, h - 2 * v_margin, self.color)

            if self.border:
                rect(x, y + v_margin, w, h - 2 * v_margin, self.border_color, False)
        # elif self.orientation == 1:
        #     h_margin = h * self.h_margin
        #     ratio = h * (self.value / self.max_val)
        #     rect(x + h_margin, y + h - ratio, w - 2 * h_margin, ratio, self.color)
        #
        #     if self.border:
        #         rect(x + h_margin, y, w - 2 * h_margin, h, self.border_color, False)
        return self


class Spinner(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)


class Graph(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.points = {}
        self.key = 0

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')

        self.x_dist = 0
        self.x_ratio = 0
        self.y_dist = 0
        self.y_ratio = 0

        self.x_axis = True
        self.x_axis_size = 3
        self.border = 1

        self.draw_colors = [Color(1, 1, 1)]
        self.background_colors = [Color(0, 0, 0, 0.5)]

    def __iter__(self):
        return iter(self.points)

    def __iadd__(self, other):
        if isinstance(other, tuple):
            self.x_max = max(self.x_max, other[0])
            self.x_min = min(self.x_min, other[0])
            self.y_max = max(self.y_max, other[1])
            self.y_min = min(self.y_min, other[1])
            self.points[other[0]] = other[1]
            self.key = other[0] + 1
        elif isinstance(other, list):
            for i in other:
                self.x_max = max(self.x_max, self.key)
                self.x_min = min(self.x_min, self.key)
                self.y_max = max(self.y_max, i)
                self.y_min = min(self.y_min, i)
                self.points[self.key] = i
                self.key += 1
        else:
            self.x_max = max(self.x_max, self.key)
            self.x_min = min(self.x_min, self.key)
            self.y_max = max(self.y_max, other)
            self.y_min = min(self.y_min, other)
            self.points[self.key] = other
            self.key += 1

        self.calc()
        return self

    def __setitem__(self, key, value):
        self.x_max = max(self.x_max, key)
        self.x_min = min(self.x_min, key)
        self.y_max = max(self.y_max, value)
        self.y_min = min(self.y_min, value)
        self.points[key] = value
        self.key = key + 1

        self.calc()
        return self

    def setDrawColors(self, colors):
        if isinstance(colors, list):
            self.draw_colors = colors

    def setBackgroundColors(self, colors):
        if isinstance(colors, list):
            self.background_colors = colors

    def setPoints(self, points):
        for k in points:
            self[k] = points[k]

    def setColor(self, c):
        ac.glColor4f(c.r, c.g, c.b, c.a)

    def calc(self):
        if len(self.points) > 0:
            self.x_dist = self.x_max - self.x_min
            if self.x_dist > 0:
                self.x_ratio = self.geometry.w / self.x_dist
            else:
                self.x_ratio = self.geometry.w / 100

            # self.x_ratio = self.geometry.w / max(self.key, 1)

            self.y_dist = self.y_max - self.y_min
            if self.y_dist > 0:
                self.y_ratio = self.geometry.h / self.y_dist
            else:
                self.y_ratio = self.geometry.h / 100

    def reset(self):
        self.points = {}
        self.key = 0

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')

        self.x_dist = 0
        self.x_ratio = 0
        self.y_dist = 0
        self.y_ratio = 0

    def update(self, delta):
        super().update(delta)

    def render(self, delta):
        super().update(delta)

    def paint(self):
        x, y = self.getPos()
        w, h = self.getSize()

        step = w * (1 / len(self.background_colors))
        current = x

        for c in self.background_colors:
            rect(current, y, step, h, c)
            current += step

        if len(self.points) > 0 and self.x_axis and self.y_max != float('-inf'):
            rect(x, y + self.y_max * self.y_ratio - 1, w, self.x_axis_size)


class LineGraph(Graph):
    def __init__(self, parent=None):
        super().__init__(parent)

    def render(self, delta):
        super().render(delta)

        self.paint()

        x, y = self.position
        w, h = self.size
        current = 0

        ac.glBegin(1)

        self.setColor(self.draw_colors[0])

        for p in sorted(self.points):
            if p * self.x_ratio > w / len(self.draw_colors) * current:
                c = self.draw_colors[current]
                self.setColor(c)
                current = min(current + 1, len(self.draw_colors) - 1)

            ac.glVertex2f(x + p * self.x_ratio, y + self.y_max * self.y_ratio - self.points[p] * self.y_ratio)

        ac.glEnd()

        return self


class AreaGraph(Graph):
    def __init__(self, parent=None):
        super().__init__(parent)

    def render(self, delta):
        super().render(delta)

        x, y = self.position
        w, h = self.size
        current = 0

        self.paint()
        self.setColor(self.draw_colors[current])

        ac.glBegin(1)

        for p in sorted(self.points):
            if p * self.x_ratio > w / len(self.draw_colors) * current:
                c = self.draw_colors[current]
                self.setColor(c)
                current = min(current + 1, len(self.draw_colors) - 1)

            ac.glVertex2f(x + p * self.x_ratio, y + self.y_max * self.y_ratio - self.points[p] * self.y_ratio)

        ac.glEnd()

        return self
