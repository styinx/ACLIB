import ac
from ui import gl

from ui.color import Color, TRANSPARENT
from ui.gui.defaults import WidgetStyle, WidgetConfig
from util.util import log, console, tb


def pt2px(pt: int) -> float:
    return pt * 4/3

def px2pt(pt: int) -> float:
    return pt * 0.75


class GUI_EVENT:
    ON_POSITION_CHANGED = 0
    ON_SIZE_CHANGED = 1
    ON_CHILD_CHANGED = 2
    ON_PARENT_CHANGED = 3
    ON_VISIBILITY_CHANGED = 4
    ON_CLICK = 5
    ON_TEXT_CHANGED = 6
    ON_CONFIG_CHANGED = 7
    ON_STYLE_CHANGED = 8


class Observer:
    def update_observer(self, subject):
        raise NotImplementedError('Override this function!')

class Subject:
    def __init__(self):
        self._observers = []

    def remove_observer(self, observer: Observer):
        self._observers.remove(observer)

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify_observers(self):
        for o in self._observers:
            o.update_observer(self)



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


class ACWidget:
    def __init__(self, parent=None):
        self._id = 0
        self._parent = None
        self._child = None

        self._position = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._background = True
        self._border = True
        self._background_texture = ''
        self._background_color = Color(0, 0, 0, 0)
        self._border_color = Color(0, 0, 0, 0)

        self.visible = True
        self.background = False
        self.border = False
        self.background_color = Color(0, 0, 0, 0)
        self.border_color = Color(0, 1, 0, 1)

        if parent:
            self.parent = parent
            # todo child assignment

        try:
            app_name = None if not self.app else self.app.__class__.__name__
            WidgetStyle.load_style_from_config(self, self.__class__.__name__, app_name)
        except Exception as e:
            log('Problems while loading style for class "{}"'.format(self.__class__.__name__))
            tb(e)

    @property
    def app(self):
        if isinstance(self, ACApp):
            return self._id

        if self.parent:
            return self.parent.app

        return None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int):
        self._id = _id

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, ACWidget):
            self._parent = parent
            self.position = (0, 0) if isinstance(parent, ACApp) else self._parent.position
            self.size = self._parent.size

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        if isinstance(child, ACWidget):
            self._child = child
            self._child.position = (0, 0) if isinstance(self, ACApp) else self._parent.position
            self._child.size = self.size

    @property
    def position(self) -> tuple:
        if self.id:
            return ac.getPosition(self.id)
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

        if self.id and len(position) == 2:
            ac.setPosition(self.id, position[0], position[1])

    @property
    def size(self) -> tuple:
        return self._size

    @size.setter
    def size(self, size: tuple):
        self._size = size

        if self.id and len(size) == 2:
            ac.setSize(self.id, size[0], size[1])

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible

        if self.id:
            ac.setVisible(self.id, True)

    @property
    def background(self) -> bool:
        return self._background

    @background.setter
    def background(self, background: bool):
        self._background = background

        if self.id:
            ac.drawBackground(self.id, 1 if background else 0)

    @property
    def border(self) -> bool:
        return self._border

    @border.setter
    def border(self, border: bool):
        self._border = border

        if self.id:
            ac.drawBorder(self.id, 1 if border else 0)

    @property
    def background_texture(self) -> str:
        return self._background_texture

    @background_texture.setter
    def background_texture(self, background_texture: str):
        self._background_texture = background_texture

        self.background = True if background_texture else False

        if self.id:
            ac.drawBackground(self.id, 1)
            if ac.setBackgroundTexture(self.id, background_texture) == -1:
                console('Texture "{}" could not be set.'.format(background_texture))

    @property
    def background_color(self) -> Color:
        return self._background_color

    @background_color.setter
    def background_color(self, background_color: Color):
        self._background_color = background_color

        self.background = True if background_color.a > 0 or self.background_texture else False

        if self.id:
            c = background_color
            if ac.setBackgroundColor(self.id, c.r, c.g, c.b) == -1 or ac.setBackgroundOpacity(self.id, c.a) == -1:
                console('Background color could not be set.')

    @property
    def border_color(self) -> Color:
        return self.border_color

    @border_color.setter
    def border_color(self, border_color: Color):
        self._border_color = border_color

        self.border = True if border_color.a > 0 else False

        if self.id:
            ac.drawBorder(self.id, 1)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, delta: int):
        if self.child:
            self.child.update(delta)

    def render(self, delta: int):
        if self.border:
            x, y = self.position
            w, h = self.size
            gl.rect(x, y, w, h, self.border_color, False)

        if self.child:
            self.child.render(delta)


class ACApp(ACWidget):
    def __init__(self, app_name: str, x: int, y: int, w: int, h: int):
        super().__init__()

        self._cfg = None
        self._title = ''

        self._title_pos = (0, 0)
        self._icon_pos = (0, 0)
        self._icon = False

        self._activation_callback = None
        self._shutdown_callback = None
        self._render_callback = None

        self.id = ac.newApp(app_name)
        self.title = app_name
        self.position = (x, y)
        self.size = (w, h)

        self.render_callback = self.render

        self._load_config()

    def _load_config(self):
        log('Load config for app "{}"'.format(self.title))
        self._cfg = WidgetConfig.load_app_config(self, self.title)

    def _write_config(self):
        log('Write config for app "{}"'.format(self.title))
        self._cfg.set('position', self.position, 'DEFAULT')
        self._cfg.write()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

        if self.id:
            ac.setTitle(self.id, title)

    @property
    def title_pos(self) -> tuple:
        return self._title_pos

    @title_pos.setter
    def title_pos(self, title_pos: tuple):
        self._title_pos = title_pos

        if self.id and len(title_pos) == 2:
            ac.setTitlePosition(self.id, title_pos[0], title_pos[1])

    @property
    def icon_pos(self) -> tuple:
        return self._icon_pos

    @icon_pos.setter
    def icon_pos(self, icon_pos: tuple):
        self._icon_pos = icon_pos

        if self.id and len(icon_pos) == 2:
            ac.setIconPosition(self.id, icon_pos[0], icon_pos[1])

    @property
    def render_callback(self):
        return self._render_callback

    @render_callback.setter
    def render_callback(self, render_callback: callable):
        self._render_callback = render_callback

        if self.id:
            ac.addRenderCallback(self.id, render_callback)

    @property
    def activation_callback(self):
        return self._activation_callback

    @activation_callback.setter
    def activation_callback(self, activation_callback: callable):
        self._activation_callback = activation_callback

        if self.id:
            ac.addOnAppActivatedListener(self.id, activation_callback)

    @property
    def shutdown_callback(self):
        return self._shutdown_callback

    @shutdown_callback.setter
    def shutdown_callback(self, shutdown_callback: callable):
        self._shutdown_callback = shutdown_callback

        if self.id:
            ac.addOnAppDismissedListener(self.id, shutdown_callback)

    def hide_decoration(self):
        self.title_pos = (-100000, -100000)
        self.icon_pos = (-100000, -100000)

    def update(self, delta: int):
        super().update(delta)

        # Required since an app movement will draw the default background again.
        self.background_color = self.background_color

    def render(self, delta: int):
        super().update(delta)

    def shutdown(self):
        self._write_config()


class ACTextWidget(ACWidget, Observer):
    def __init__(self, parent: ACWidget = None):
        super().__init__(parent)

        self._text = ''
        self._font = None
        self._h_alignment = 'left'
        self._v_alignment = 'top'
        self._alignment_offset = 0

    def update_observer(self, subject):
        if isinstance(subject, Font):
            self.font = subject

    @ACWidget.position.setter
    def position(self, position: tuple):
        self._position = position

        if self.id and len(position) == 2:
            ac.setPosition(self.id, position[0], position[1] + self._alignment_offset)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

        if self.id:
            ac.setText(self.id, text)

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, font: Font):
        if font:
            if self._font:
                self._font.remove_observer(self)

            self._font = font
            self._font.add_observer(self)

            if self.id:
                ac.setFontSize(self.id, font.size)
                ac.setFontColor(self.id, font.color.r, font.color.g, font.color.b, font.color.a)
                ac.setCustomFont(self.id, font.name, font.italic, font.bold)

                self.v_alignment = self._v_alignment

    @property
    def h_alignment(self):
        return self._h_alignment

    @h_alignment.setter
    def h_alignment(self, h_alignment: str):
        self._h_alignment = h_alignment

        if self.id:
            ac.setFontAlignment(self.id, self._h_alignment)

        self._set_text_alignment()

    @property
    def v_alignment(self):
        return self._v_alignment

    @v_alignment.setter
    def v_alignment(self, v_alignment: str):
        self._v_alignment = v_alignment

        if self.font and pt2px(self.font.size) < self.size[1]:
            if self._v_alignment == 'top':
                self._alignment_offset = 0
            elif self._v_alignment == 'middle':
                self._alignment_offset = round(self.size[1] / 2 - pt2px(self.font.size) / 2)
            elif self._v_alignment == 'bottom':
                self._alignment_offset = self.size[1] - pt2px(self.font.size)

        self._set_text_alignment()

    def _set_text_alignment(self):
        x, y = self.position

        if self._h_alignment == 'left':
            x = self.position[0]
        elif self._h_alignment == 'center':
            x = int(self.position[0] + self.size[0] / 2)
        elif self._h_alignment == 'right':
            x = self.position[0] + self.size[0]

        self.position = (x, y)


class ACLabel(ACTextWidget):
    def __init__(self, text: str, font: Font = None, h_alignment: str = 'left', v_alignment: str = 'top',
                 parent: ACWidget = None):
        super().__init__(parent)

        self.id = ac.addLabel(self.app, text)
        self.font = font
        self.text = text
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment


class ACButton(ACTextWidget):
    def __init__(self, text: str, font: Font = None, h_alignment: str = 'left', v_alignment: str = 'top',
                 parent: ACWidget = None):
        super().__init__(parent)

        self.id = ac.addButton(self.app, text)
        self.font = font
        self.text = text
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment


class ACInput(ACTextWidget):
    def __init__(self, text: str = '', parent: ACWidget = None):
        super().__init__(parent)

        self.id = ac.addInputText(self.app, text)
        self.text = text


class ACIcon(ACButton):
    def __init__(self, file: str, parent: ACWidget = None):
        super().__init__('', parent=parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False
