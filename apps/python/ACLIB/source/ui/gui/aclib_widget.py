from ui.color import *
from ui.gui.ac_widget import ACWidget, ACButton, ACLabel
from ui.gui.font import Font


class ACLIBIcon(ACButton):
    def __init__(self, file: str, parent: ACWidget = None):
        super().__init__(parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False


# todo range checking
class ACLIBProgressBar(ACLabel):
    def __init__(self, parent: ACWidget, value: float, start: float = 0, stop: float = 1):
        super().__init__(parent, '', 'center', 'middle')

        self._font = Font('Roboto Mono')
        self._font.size = 12
        self._font.bold = 1
        self._font.color = BLACK

        self._progress = ACLabel(self)
        self._text = ACLabel(self, '', 'center', 'middle', self._font)
        self._show_progress = False
        self._range = (start, stop)
        self._value = value

    @property
    def show_progress(self):
        return self._show_progress

    @show_progress.setter
    def show_progress(self, show_progress: bool):
        self._show_progress = show_progress

        self.value = self.value

    @property
    def progress_texture(self):
        return self._progress.background_texture

    @progress_texture.setter
    def progress_texture(self, progress_texture: str):
        self._progress.background_texture = progress_texture

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, _range: tuple):
        self._range = _range

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

        if self._range[1] > 0:
            progress = self._value / self._range[1]
        else:
            progress = 0

        if progress >= 0.5:
            self._font.color = BLACK
        else:
            self._font.color = WHITE

        if self._show_progress:
            self._text.text = '{} %'.format(round(progress * 100, 1))

        w, h = self.size

        self._progress.position = self.position
        self._progress.size = w * progress, h
