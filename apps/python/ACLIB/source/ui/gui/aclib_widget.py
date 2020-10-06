from ui.color import *
from ui.gui.ac_widget import ACWidget, ACButton, ACLabel
from ui.gui.font import Font, px2pt


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

    def _on_size_changed(self):
        super()._on_size_changed()

        if hasattr(self, '_progress'):
            self._progress.size = self.size
            self._text.size = self.size
            self._text.font.size = px2pt(self.size[1])

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
