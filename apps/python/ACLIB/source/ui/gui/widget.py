import ac
from ui import gl
from ui.animation import Animation

from ui.color import Color, TRANSPARENT
from ui.gui.font import Font, pt2px
from ui.gui.defaults import WidgetStyle, WidgetConfig
from util.log import log, console, tb
from util.observer import Observer


class ACAnimation:
    class EVENT:
        POSITION_CHANGED = 0
        SIZE_CHANGED = 1
        CHILD_CHANGED = 2
        PARENT_CHANGED = 3
        VISIBILITY_CHANGED = 4
        CLICK = 5
        TEXT_CHANGED = 6
        CONFIG_CHANGED = 7
        STYLE_CHANGED = 8

    class PROPERTY:
        BACKGROUND = 'background'
        BACKGROUND_COLOR = 'background_color'
        BORDER = 'border'
        BORDER_COLOR = 'border_color'

    def __init__(self):
        self._active = None
        self._queue = []

    @property
    def animation(self):
        return self._active

    @animation.setter
    def animation(self, animation):
        self._active = animation

    def add_animation(self, animation: Animation):
        self._queue.append(animation)

    def update_animation(self):
        if self._active is None:
            if len(self._queue) > 0:
                self._active = self._queue.pop(0)
                self._active.init()
        else:
            if not self._active.is_finished():
                self._active.update()
            else:
                self._active = None


class ACWidget(ACAnimation):
    def __init__(self, parent=None):
        super().__init__()

        self._id = -1
        self._parent = parent
        self._child = None

        self._position = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._background = True
        self._border = True
        self._background_texture = ''
        self._background_color = Color(0.0, 0.0, 0.0, 0.0)
        self._border_color = Color(0.0, 0.0, 0.0, 0.0)

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

        return self._id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int):
        self._id = _id

        # Properties like color, text, ... can only be applied when the id is available.
        self.size = self.size
        self.position = self.position
        self.visible = self.visible
        self.background = self.background
        self.border = self.border
        self.background_texture = self.background_texture
        self.background_color = self.background_color
        self.border_color = self.border_color

        # Overwrite position and size if parent is available.
        self.parent = self._parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, ACWidget):
            if parent.child != self:
                self._parent = parent
                self.size = self._parent.size
                self.position = (0, 0) if isinstance(parent, ACApp) else self._parent._position
                self.parent.child = self

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        if isinstance(child, ACWidget):
            self._child = child
            self.child.size = self._size
            self.child.position = (0, 0) if isinstance(self, ACApp) else self._position
            self.child.parent = self

    @property
    def position(self) -> tuple:
        if self.id != -1:
            position = ac.getPosition(self.id)
            if position != -1:
                return position
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

        if self.id != -1 and len(position) == 2:
            ac.setPosition(self.id, position[0], position[1])

    @property
    def size(self) -> tuple:
        if self.id != -1:
            size = ac.getSize(self.id)
            if size != -1:
                return size
        return self._size

    @size.setter
    def size(self, size: tuple):
        self._size = size

        if self.id != -1 and len(size) == 2:
            ac.setSize(self.id, size[0], size[1])

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible

        if self.id != -1:
            ac.setVisible(self.id, True)

    @property
    def background(self) -> bool:
        return self._background

    @background.setter
    def background(self, background: bool):
        self._background = background

        if self.id != -1:
            ac.drawBackground(self.id, 1 if background else 0)

    @property
    def border(self) -> bool:
        return self._border

    @border.setter
    def border(self, border: bool):
        self._border = border

        if self.id != -1:
            ac.drawBorder(self.id, 1 if border else 0)

    @property
    def background_texture(self) -> str:
        return self._background_texture

    @background_texture.setter
    def background_texture(self, background_texture: str):
        self._background_texture = background_texture

        self.background = True if background_texture else False

        if self.id != -1:
            ac.drawBackground(self.id, 1)
            if background_texture is not '' and ac.setBackgroundTexture(self.id, background_texture) == -1:
                console('Texture "{}" could not be set.'.format(background_texture))

    @property
    def background_color(self) -> Color:
        return self._background_color

    @background_color.setter
    def background_color(self, background_color: Color):
        self._background_color = background_color

        if self.id != -1:
            c = background_color
            success = ac.setBackgroundColor(self.id, c.r, c.g, c.b) != -1
            success &= ac.setBackgroundOpacity(self.id, c.a) != -1
            self.background = True if c.a > 0 or self.background_texture != '' else False
            if not success:
                console('Background color could not be set.')

    @property
    def border_color(self) -> Color:
        return self._border_color

    @border_color.setter
    def border_color(self, border_color: Color):
        self._border_color = border_color

        self.border = True if border_color.a > 0 else False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, delta: int):
        self.update_animation()

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

        if self.id != -1:
            ac.setTitle(self.id, title)

    @property
    def title_pos(self) -> tuple:
        return self._title_pos

    @title_pos.setter
    def title_pos(self, title_pos: tuple):
        self._title_pos = title_pos

        if self.id != -1 and len(title_pos) == 2:
            ac.setTitlePosition(self.id, title_pos[0], title_pos[1])

    @property
    def icon_pos(self) -> tuple:
        return self._icon_pos

    @icon_pos.setter
    def icon_pos(self, icon_pos: tuple):
        self._icon_pos = icon_pos

        if self.id != -1 and len(icon_pos) == 2:
            ac.setIconPosition(self.id, icon_pos[0], icon_pos[1])

    @property
    def render_callback(self):
        return self._render_callback

    @render_callback.setter
    def render_callback(self, render_callback: callable):
        self._render_callback = render_callback

        if self.id != -1:
            ac.addRenderCallback(self.id, render_callback)

    @property
    def activation_callback(self):
        return self._activation_callback

    @activation_callback.setter
    def activation_callback(self, activation_callback: callable):
        self._activation_callback = activation_callback

        if self.id != -1:
            ac.addOnAppActivatedListener(self.id, activation_callback)

    @property
    def shutdown_callback(self):
        return self._shutdown_callback

    @shutdown_callback.setter
    def shutdown_callback(self, shutdown_callback: callable):
        self._shutdown_callback = shutdown_callback

        if self.id != -1:
            ac.addOnAppDismissedListener(self.id, shutdown_callback)

    def hide_decoration(self):
        self.title_pos = (-100000, -100000)
        self.icon_pos = (-100000, -100000)

    def update(self, delta: int):
        super().update(delta)

        # Required since an app movement will draw the default background again.
        self.background_color = self.background_color

    def shutdown(self):
        self._write_config()


class ACTextWidget(ACWidget, Observer):
    def __init__(self, text: str = '', h_alignment: str = 'left', v_alignment: str = 'top', font: Font = None,
                 parent: ACWidget = None):
        super().__init__(parent)

        self._text = text
        self._font = font
        self._h_alignment = h_alignment
        self._v_alignment = v_alignment
        self._v_offset = 0
        self._h_offset = 0

    def update_observer(self, subject):
        if isinstance(subject, Font):
            self.font = subject

    @ACWidget.id.setter
    def id(self, _id: int):
        self._id = _id

        # Properties like color, text, ... can only be applied when the id is available.
        self.size = self.size
        self.position = self.position
        self.visible = self.visible
        self.background = self.background
        self.border = self.border
        self.background_texture = self.background_texture
        self.background_color = self.background_color
        self.border_color = self.border_color
        self.font = self.font
        self.text = self.text

        self.h_alignment = self.h_alignment
        self.v_alignment = self.v_alignment

        # Overwrite position and size if parent is available.
        self.parent = self._parent

    @ACWidget.position.setter
    def position(self, position: tuple):
        self._position = position

        if self.id != -1 and len(position) == 2:
            ac.setPosition(self.id, position[0], position[1] + self._v_offset)

    @ACWidget.size.setter
    def size(self, size: tuple):
        self._size = size

        if self.id != -1 and len(size) == 2:
            ac.setSize(self.id, size[0], size[1])

        self.v_alignment = self._v_alignment

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

        if self.id != -1:
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

            if self.id != -1:
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

        if self.id != -1:
            ac.setFontAlignment(self.id, self._h_alignment)

    @property
    def v_alignment(self):
        return self._v_alignment

    @v_alignment.setter
    def v_alignment(self, v_alignment: str):
        self._v_alignment = v_alignment

        self._v_offset = 0
        used_height = pt2px(12) if self.font is None else pt2px(self.font.size)

        if used_height < self.size[1]:
            if self._v_alignment == 'top':
                self._v_offset = 0
            elif self._v_alignment == 'middle':
                self._v_offset = round(self.size[1] / 2 - used_height / 2)
            elif self._v_alignment == 'bottom':
                self._v_offset = self.size[1] - used_height


class ACLabel(ACTextWidget):
    def __init__(self, text: str = '', h_alignment: str = 'left', v_alignment: str = 'top', font: Font = None,
                 parent: ACWidget = None):
        super().__init__(text, h_alignment, v_alignment, font, parent)

        self.id = ac.addLabel(self.app, text)


class ACButton(ACTextWidget):
    def __init__(self, text: str = '', h_alignment: str = 'left', v_alignment: str = 'top', font: Font = None,
                 parent: ACWidget = None):
        super().__init__(text, h_alignment, v_alignment, font, parent)

        self.id = ac.addButton(self.app, text)


class ACInput(ACTextWidget):
    def __init__(self, text: str = '', h_alignment: str = 'left', v_alignment: str = 'top', font: Font = None,
                 parent: ACWidget = None):
        super().__init__(text, h_alignment, v_alignment, font, parent)

        self.id = ac.addInputText(self.app, text)


class ACIcon(ACButton):
    def __init__(self, file: str, parent: ACWidget = None):
        super().__init__('', parent=parent)

        self.background_texture = file
        self.background_color = TRANSPARENT
        self.border = False


class ACGraph(ACWidget):
    def __init__(self, parent: ACWidget = None):
        super().__init__(parent)

        self.id = ac.addGraph(self.app, '')

        self._range = (0, 0)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value_range: tuple):
        self._range = value_range
        if self.id != -1:
            ac.setRange(self.id, self._range[0], self._range[1])

    def add_series(self, color: Color):
        if self.id != -1:
            ac.addSerieToGraph(self.id, color.r, color.g, color.b)

    def add_value(self, value: float, series: int):
        if self.id != -1:
            ac.addValueToGraph(self.id, series, value)
