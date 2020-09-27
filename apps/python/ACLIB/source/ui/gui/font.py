import ac
from ui.color import Color
from util.observer import Subject


class Font(Subject):
    def __init__(self, font_name: str):
        super().__init__()

        self._name = font_name
        self._size = 0
        self._is_italic = False
        self._is_bold = False

        self._color = Color(0, 0, 0, 0)

        if ac.initFont(0, font_name, 0, 0) == -1:
            raise Exception('Could not load font {}'.format(font_name))

        self.color = Color(1, 1, 1)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name
        self.notify_observers()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size
        self.notify_observers()

    @property
    def italic(self):
        return 1 if self._is_italic else 0

    @italic.setter
    def italic(self, italic: bool):
        self._is_italic = italic
        self.notify_observers()

    @property
    def bold(self):
        return 1 if self._is_bold else 0

    @bold.setter
    def bold(self, bold: bool):
        self._is_bold = bold
        self.notify_observers()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, text_color: Color):
        self._color = text_color
        self.notify_observers()


def pt2px(pt: int) -> float:
    return pt * 4/3


def px2pt(pt: int) -> float:
    return pt * 0.75