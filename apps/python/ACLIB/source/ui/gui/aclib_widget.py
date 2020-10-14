from settings import TEXTURE_DIR, path
from ui.color import *
from ui.gui.ac_widget import ACWidget, ACButton, ACLabel
from ui.gui.font import Font, px2pt
from ui.gui.layout import ACGrid, ACLayout


class ACLIBIcon(ACButton):
    def __init__(self, parent: ACWidget, file: str):
        super().__init__(parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False


# todo range checking
class ACLIBProgressBar(ACLabel):
    def __init__(self, parent: ACWidget, value: float, start: float = 0, stop: float = 1, progress: bool = False):
        super().__init__(parent)

        font = Font('Roboto Mono')
        font.size = 14
        font.bold = 1
        font.color = BLACK

        self._progress = ACLabel(self)
        self._text = ACLabel(self, '', 'center')
        self._show_progress = progress
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

        self._plus = ACButton(self)
        self._minus = ACButton(self)

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

    def on_plus(self, widget: ACWidget, *args):
        self._scale += self._step

        if self._absolute:
            w, h = self._original_size
            self._target.size = (w + self._scale, h + self._scale)
        else:
            w, h = self._original_size
            self._target.size = (round(w * self._scale), round(h * self._scale))

    def on_minus(self, widget: ACWidget, *args):
        if self._absolute:
            self._scale -= self._step
            w, h = self._original_size
            self._target.size = (w - self._scale, h - self._scale)
        else:
            self._scale = max(self._step, self._scale - self._step)
            w, h = self._original_size
            self._target.size = (round(w * self._scale), round(h * self._scale))


class ACLIBCollapsable(ACLabel):
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


class ACLIBListBox(ACLayout):
    """
    This widget enables scrolling on a list of items. Items must inherit from ACWidget.
    The widget has a scrollbar and two buttons. One arrow scrolls the list upwards, the other arrow scrolls downwards.
    The number of elements that are shown is configurable. Items that are not inside the item range are hidden.
    """

    TEXTURES = {
        'up':  path(TEXTURE_DIR, 'triangle_up.png'),
        'down': path(TEXTURE_DIR, 'triangle_down.png')
    }

    def __init__(self, parent: ACWidget, elements: int = 5):
        super().__init__(parent)

        self._elements = elements
        self._bar_width = 10
        self._index = 0
        self._widgets = []

        self._bar = ACButton(self)
        self._up = ACButton(self)
        self._down = ACButton(self)

        self._bar.background_color = WHITE
        self._up.background_texture = ACLIBListBox.TEXTURES['up']
        self._up.background_color = LIGHTGRAY
        self._up.size = self._bar_width, self._bar_width
        self._down.background_texture = ACLIBListBox.TEXTURES['down']
        self._down.background_color = LIGHTGRAY
        self._down.size = self._bar_width, self._bar_width

        self._up.on(ACWidget.EVENT.CLICK, self._on_up)
        self._down.on(ACWidget.EVENT.CLICK, self._on_down)

    # Private

    def _on_position_changed(self):
        if hasattr(self, '_up'):
            x, y = self.position
            w, h = self.size
            right = w - self._bar_width
            self._bar.position = right, y + self._bar_width
            self._up.position = right, y
            self._down.position = right, y + h - self._bar_width

    def _on_size_changed(self):
        if hasattr(self, '_up'):
            x, y = self.position
            w, h = self.size
            right = w - self._bar_width
            self._bar.size = self._bar_width, h - self._bar_width * 2
            self._bar.position = right, y + self._bar_width
            self._up.position = right, y
            self._down.position = right, y + h - self._bar_width

    def _reposition(self):
        x, y = self.position
        w, h = self.size

        element_height = h / self._elements

        # Hide items that are out of range.
        for i in range(0, self._index):
            self._widgets[i].visible = False
        for i in range(self._index + self._elements, max(self._index + self._elements, len(self._widgets))):
            self._widgets[i].visible = False

        # Set the position and size of the items inside the list.
        for i in range(self._index, min(len(self._widgets), self._index + self._elements)):
            self._widgets[i].position = x, y
            self._widgets[i].size = w - self._bar_width, element_height
            self._widgets[i].visible = True
            y += element_height

    def _on_up(self, widget: ACWidget, *args):
        if self._index > 0:
            self._index -= 1
        self._reposition()

    def _on_down(self, widget: ACWidget, *args):
        if self._index < len(self._widgets) - self._elements:
            self._index += 1
        self._reposition()

    # Public

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index: int):
        if 0 <= index < len(self._widgets):
            self.index = index
            self._reposition()

    @property
    def count(self):
        return self._elements

    @count.setter
    def count(self, count: int):
        self._elements = count
        self._reposition()

    def add(self, widget: ACWidget):
        self._widgets.append(widget)

        self._reposition()

    def remove(self, widget: ACWidget = None, index: int = -1):
        if widget:
            self._widgets.remove(widget)
        elif 0 <= index < len(self._widgets):
            del self._widgets[index]

        self._reposition()
