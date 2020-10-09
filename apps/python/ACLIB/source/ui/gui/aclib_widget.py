from settings import TEXTURE_DIR, path
from ui.color import *
from ui.gui.ac_widget import ACWidget, ACButton, ACLabel
from ui.gui.font import Font, px2pt
from ui.gui.layout import ACGrid


class ACLIBIcon(ACButton):
    def __init__(self, file: str, parent: ACWidget = None):
        super().__init__(parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False


# todo range checking
class ACLIBProgressBar(ACLabel):
    def __init__(self, parent: ACWidget, value: float, start: float = 0, stop: float = 1):
        super().__init__(parent)

        font = Font('Roboto Mono')
        font.size = 14
        font.bold = 1
        font.color = BLACK

        self._progress = ACLabel(self)
        self._text = ACLabel(self, '', 'center')
        self._show_progress = False
        self._range = (min(start, stop), max(start, stop))
        self._value = value if start <= value <= stop else start

        self._progress.background_color = GREEN

        self._text.font = font

    def _on_position_changed(self):
        super()._on_position_changed()

        if hasattr(self, '_progress'):
            self._progress.position = self.position
            self._text.position = self.position
            self.value = self.value

    def _on_size_changed(self):
        super()._on_size_changed()

        if hasattr(self, '_progress'):
            self._progress.size = self.size
            self._text.size = self.size
            self._text.font.size = px2pt(self.size[1])
            self.value = self.value

    @property
    def show_progress(self):
        return self._show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self._show_progress = show_progress

        self.value = self.value

    @property
    def progress_color(self):
        return self._progress.background_color

    @progress_color.setter
    def progress_color(self, progress_color: Color):
        self._progress.background_color = progress_color

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, _range: tuple):
        self._range = min(_range[0], _range[1]), max(_range[0], _range[1])
        if not (self._range[0] <= self._value <= self._range[1]):
            self._value = self._range[0]

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value if self._range[0] <= value <= self._range[1] else self._range[0]

        progress = (self._value - self._range[0]) / (self._range[1] - self._range[0])

        if progress >= 0.5:
            self._text.font.color = BLACK
        else:
            self._text.font.color = WHITE

        if self._show_progress:
            self._text.text = '{} %'.format(round(progress * 100, 1))

        w, h = self.size

        self._progress.size = w * progress, h


class ACLIBScaler(ACGrid):
    """
    Use this widget to get a plus and minus button that scales another widget.
    Use 'absolute = True' to have an absolute scale to increase/decrease the widget with pixel size.
    'scale = 1' means that the target will scale 1 pixel in width and height.
    Using 'absolute = False' will scale the target relative.
    'scale = 0.1' will increase/decrease the target by 10%.
    """

    TEXTURES = {
        'plus': path(TEXTURE_DIR, 'plus.png'),
        'minus': path(TEXTURE_DIR, 'minus.png')
    }

    def __init__(self, parent: ACWidget, target: ACWidget, step: float = 1, absolute: bool = False):
        super().__init__(1, 2, parent)

        self._target = target
        self._absolute = absolute
        self._step = abs(step)
        self._scale = 0 if self._absolute else 1
        self._original_size = target.size
        self._current_size = target.size

        self._plus = ACLabel(self)
        self._minus = ACLabel(self)

        self._plus.background_color = WHITE
        self._plus.background_texture = ACLIBScaler.TEXTURES['plus']
        self._minus.background_color = WHITE
        self._minus.background_texture = ACLIBScaler.TEXTURES['minus']

        self.add(self._plus, 0, 0)
        self.add(self._minus, 0, 1)

        self._plus.on(ACWidget.EVENT.CLICK, self.on_plus)
        self._minus.on(ACWidget.EVENT.CLICK, self.on_minus)

    def initial_size(self, size: tuple):
        self._target.size = size
        self._original_size = size

    def on_plus(self, widget: ACWidget):
        self._scale += self._step

        if self._absolute:
            w, h = self._original_size
            self._target.size = (w + self._scale, h + self._scale)
        else:
            w, h = self._original_size
            self._target.size = (round(w * self._scale), round(h * self._scale))

    def on_minus(self, widget: ACWidget):
        if self._absolute:
            self._scale -= self._step
            w, h = self._original_size
            self._target.size = (w - self._scale, h - self._scale)
        else:
            self._scale = max(self._step, self._scale - self._step)
            w, h = self._original_size
            self._target.size = (round(w * self._scale), round(h * self._scale))


class ACLIBCollapsable(ACWidget):
    TEXTURES = {
        'plus':  path(TEXTURE_DIR, 'plus.png'),
        'minus': path(TEXTURE_DIR, 'minus.png')
    }

    def __init__(self, parent: ACWidget, target: ACWidget):
        super().__init__(parent)

        self._collapsed = False

        self._grid = ACGrid(3, 2, self)
        self._button = ACButton(self._grid)
        self._content = ACLabel(self._grid)

        self._button.background_color = WHITE
        self._button.background_texture = ACLIBCollapsable.TEXTURES['plus']

        self._grid.add(self._button, 0, 0)
        self._grid.add(self._content, 0, 1)

        self.content = target

    @property
    def content(self):
        return self._content.child

    @content.setter
    def content(self, content: ACWidget):
        self._content.child = content

    @property
    def collapsed(self) -> bool:
        return self._collapsed

    @collapsed.setter
    def collapsed(self, collapsed: bool):
        self._collapsed = collapsed

        if collapsed:
            self._button.background_texture = ACLIBCollapsable.TEXTURES['minus']
            self._content.visible = False
        else:
            self._button.background_texture = ACLIBCollapsable.TEXTURES['plus']
            self._content.visible = True


class ACLIBListBox(ACWidget):
    TEXTURES = {
        'up':  path(TEXTURE_DIR, 'triangle_up.png'),
        'down': path(TEXTURE_DIR, 'triangle_down.png')
    }

    def __init__(self, parent: ACWidget, elements: int = 5):
        super().__init__(parent)

        self._elements = elements
        self._index = 0
        self._widgets = []

        self._grid = ACGrid(5, elements, self)
        self._up = ACButton(self._grid)
        self._down = ACButton(self._grid)

        self._up.background_texture = ACLIBListBox.TEXTURES['up']
        self._up.background_color = WHITE
        self._down.background_texture = ACLIBListBox.TEXTURES['down']
        self._down.background_color = WHITE

        self._grid.add(self._up, 4, 0)
        self._grid.add(self._down, 4, elements - 1)

        self._up.on(ACWidget.EVENT.CLICK, self._up)
        self._down.on(ACWidget.EVENT.CLICK, self._down)

        self._reposition()

    def _reposition(self):
        x, y = self.position
        w, h = self._grid.cell_size
        for i in range(self._index, min(len(self._widgets), self._index + 5)):
            self._widgets[i].position = x, y
            y += h

    def _up(self, widget: ACWidget):
        if self._index > 0:
            self._index -= 1
        self._reposition()

    def _down(self, widget: ACWidget):
        if self._index < len(self._widgets) - 5:
            self._index += 1
        self._reposition()

    def add(self, widget: ACWidget):
        self._widgets.append(widget)

        self._reposition()
