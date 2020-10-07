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

    def __init__(self, parent: ACWidget, target: ACWidget, scale: float = 1, absolute: bool = False):
        super().__init__(1, 2, parent)

        self._target = target
        self._scale = scale
        self._absolute = absolute

        self._plus = ACLabel(self)
        self._minus = ACLabel(self)

        self._plus.background_texture = ACLIBScaler.TEXTURES['plus']
        self._plus.background_color = GREEN
        self._minus.background_texture = ACLIBScaler.TEXTURES['minus']
        self._minus.background_color = RED

        self.add(self._plus, 0, 0)
        self.add(self._minus, 0, 1)

        self._plus.on(ACWidget.EVENT.CLICK, self.on_plus)
        self._minus.on(ACWidget.EVENT.CLICK, self.on_minus)

    def on_plus(self, _id: int):
        w, h = self._target.size
        if self._absolute:
            self._target.size = (w + self._scale, h + self._scale)
        else:
            self._target.size = (w * (1 + self._scale), h * (1 + self._scale))

    def on_minus(self, _id: int):
        w, h = self._target.size
        if self._absolute:
            self._target.size = (w - self._scale, h - self._scale)
        else:
            self._target.size = (w * (1 - self._scale), h * (1 - self._scale))
