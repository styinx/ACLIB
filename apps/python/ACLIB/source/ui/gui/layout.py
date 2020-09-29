import ac

from ui.gui.widget import ACWidget


class ACLayout(ACWidget):
    def __init__(self, parent: ACWidget = None):
        super().__init__(parent)

        self._children = []

        self.id = ac.addLabel(self.app, '')

    def __iter__(self):
        return iter(self._children)

    @property
    def children(self) -> list:
        return self._children

    @property
    def child(self):
        if len(self._children) > 0:
            return self._children[0]
        return None

    @child.setter
    def child(self, child: ACWidget):
        pass

    def update(self, delta: int):
        super().update(delta)

        for child in self.children:
            child.update(delta)

    def render(self, delta: int):
        super().render(delta)

        for child in self.children:
            child.render(delta)


class ACBox(ACLayout):
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, orientation: int = 0, parent: ACWidget = None):
        super().__init__(parent)

        self._orientation = 0

        self.orientation = orientation

    @property
    def orientation(self) -> int:
        return self._orientation

    @orientation.setter
    def orientation(self, orientation: int):
        self._orientation = orientation

    def add(self, widget: ACWidget):
        self._children.append(widget)
        widget.parent = self


class ACHBox(ACBox):
    def __init__(self, parent: ACWidget = None):
        super().__init__(ACBox.HORIZONTAL, parent)

    def add(self, widget: ACWidget):
        super().add(widget)

        x, y = self.position
        w, h = self.size
        width_per_child = round(w / len(self._children))

        for c in self._children:
            c.position = (x, h)
            c.size = (width_per_child, h)
            x += width_per_child


class ACVBox(ACBox):
    def __init__(self, parent: ACWidget = None):
        super().__init__(ACBox.VERTICAL, parent)

    def add(self, widget: ACWidget):
        super().add(widget)

        x, y = self.position
        w, h = self.size
        height_per_child = round(h / len(self.children))

        for child in self.children:
            child.position = (x, y)
            child.size = (w, height_per_child)
            y += height_per_child


class ACGrid(ACLayout):
    def __init__(self, cols: int = 1, rows: int = 1, parent: ACWidget = None):
        super().__init__(parent)

        self._cols = max(1, cols)
        self._rows = max(1, rows)
        self._cell_width = round(self.size[0] / self.cols)
        self._cell_height = round(self.size[1] / self.rows)

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def rows(self) -> int:
        return self._rows

    def child_at(self, x: int, y: int):
        if not (0 <= x < self.cols) or not (0 <= y < self.rows):
            return self._children[y * self._cols + x]
        return None

    def add(self, widget: ACWidget, x: int, y: int, w: int = 1, h: int = 1):
        if not (0 <= x < self.cols) or not (0 <= y < self.rows):
            return

        self._children.insert(y * self._cols + x, widget)
        widget.parent = self
        widget.position = (self.position[0] + self._cell_width * x, self.position[1] + self._cell_height * y)
        widget.size = (self._cell_width * w, self._cell_height * h)
