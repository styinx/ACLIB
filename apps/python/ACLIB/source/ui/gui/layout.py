import ac

from ui import gl
from ui.gui.ac_widget import ACWidget


class ACLayout(ACWidget):
    def __init__(self, parent: ACWidget = None):
        super().__init__(parent)

        self._children = []

        self.id = ac.addLabel(self.app, '')

    def __iter__(self):
        return iter(self._children)

    def _on_visibility_changed(self):
        for child in self._children:
            child.visible = self.visible

    @property
    def children(self) -> list:
        return self._children

    def update(self, delta: int):
        self.update_animation()

        for child in self._children:
            child.update(delta)

    def render(self, delta: int):
        if self.border:
            x, y = self.position
            w, h = self.size
            gl.rect(x, y, w, h, self.border_color, False)

        for child in self._children:
            child.render(delta)


class ACBox(ACLayout):
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, parent: ACWidget, orientation: int = 0):
        super().__init__(parent)

        self._orientation = 0

        self.orientation = orientation

    def _on_position_changed(self):
        if hasattr(self, '_orientation'):
            x, y = self.position
            w, h = self.size

            if self.orientation == ACBox.HORIZONTAL:
                dim = round(w / max(1, len(self._children)))
            else:
                dim = round(h / max(1, len(self._children)))

            for c in self._children:
                c.position = (x, y)
                if self.orientation == ACBox.HORIZONTAL:
                    x += dim
                else:
                    y += dim

    def _on_size_changed(self):
        if hasattr(self, '_orientation'):
            w, h = self.size
            if self.orientation == ACBox.HORIZONTAL:
                dim = round(w / max(1, len(self._children)))
            else:
                dim = round(h / max(1, len(self._children)))

            for c in self._children:
                if self.orientation == ACBox.HORIZONTAL:
                    c.size = (dim, h)
                else:
                    c.size = (w, dim)

    @property
    def orientation(self) -> int:
        return self._orientation

    @orientation.setter
    def orientation(self, orientation: int):
        self._orientation = orientation

    def add(self, widget: ACWidget):
        self._children.append(widget)

        self._on_position_changed()
        self._on_size_changed()


class ACHBox(ACBox):
    def __init__(self, parent: ACWidget):
        super().__init__(parent, ACBox.HORIZONTAL)


class ACVBox(ACBox):
    def __init__(self, parent: ACWidget):
        super().__init__(parent, ACBox.VERTICAL)


class ACGrid(ACLayout):
    def __init__(self, cols: int = 1, rows: int = 1, parent: ACWidget = None):
        super().__init__(parent)

        self._indices = {}

        self._cols = max(1, cols)
        self._rows = max(1, rows)
        self._cell_width = round(self.size[0] / self.cols)
        self._cell_height = round(self.size[1] / self.rows)

        self.on(ACWidget.EVENT.COLS_CHANGED, self._on_cols_changed)
        self.on(ACWidget.EVENT.ROWS_CHANGED, self._on_rows_changed)

    # Private

    def _on_position_changed(self):
        if hasattr(self, '_indices'):
            x, y = self.position

            for idx, child in self._indices.items():
                child.position = (x + idx[0] * self._cell_width, y + idx[1] * self._cell_height)

    def _on_size_changed(self):
        if hasattr(self, '_indices'):
            self._cell_width = round(self.size[0] / self.cols)
            self._cell_height = round(self.size[1] / self.rows)
            x, y = self.position

            for idx, child in self._indices.items():
                child.position = (x + idx[0] * self._cell_width, y + idx[1] * self._cell_height)
                child.size = (idx[2] * self._cell_width, idx[3] * self._cell_height)

    def _on_cols_changed(self, *args):
        self._on_size_changed()

    def _on_rows_changed(self, *args):
        self._on_size_changed()

    # Public

    @property
    def cell_size(self):
        return self._cell_width, self._cell_height

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def rows(self) -> int:
        return self._rows

    def add_cols(self, cols: int):
        if cols > 0:
            self._cols += cols
            self.fire(ACWidget.EVENT.COLS_CHANGED, self._cols)

    def remove_cols(self, cols: int):
        if cols < 0:
            self._cols += cols
            self.fire(ACWidget.EVENT.COLS_CHANGED, self._cols)

    def add_rows(self, rows: int):
        if rows > 0:
            self._rows += rows
            self.fire(ACWidget.EVENT.ROWS_CHANGED, self._rows)

    def remove_rows(self, rows: int):
        if 0 < rows <= self._rows:
            self._rows -= rows
            self.fire(ACWidget.EVENT.ROWS_CHANGED, self._rows)

    def child_at(self, x: int, y: int):
        if not (0 <= x < self.cols) or not (0 <= y < self.rows):
            return self._children[y * self._cols + x]
        return None

    def add(self, widget: ACWidget, x: int, y: int, w: int = 1, h: int = 1):
        if not (0 <= x < self.cols) or not (0 <= y < self.rows):
            return

        self._children.insert(y * self._cols + x, widget)
        self._indices[(x, y, w, h)] = widget
        widget.size = (self._cell_width * w, self._cell_height * h)
        widget.position = (self.position[0] + self._cell_width * x, self.position[1] + self._cell_height * y)


class ACMultiWidget(ACLayout):
    def __init__(self, parent: ACWidget):
        super().__init__(parent)

    def add(self, widget: ACWidget):
        self._children.append(widget)

    def _on_position_changed(self):
        x, y = self.position

        for c in self._children:
            c.position = (x, y)

    def _on_size_changed(self):
        w, h = self.size

        for c in self._children:
            c.size = (w, h)
