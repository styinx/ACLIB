import ac
from source.color import Color
from source.gl import Texture, rect


class Font:
    def __init__(self, font_name, italic, bold):
        if ac.initFont(0, font_name, italic, bold) == -1:
            raise Exception("Could not load font " + font_name)

        self._font_name = font_name
        self._italic = italic
        self._bold = bold

    def getFontName(self):
        return self._font_name

    def isItalic(self):
        return self._italic > 0

    def isBold(self):
        return self._bold > 0


class ACWidget(object):
    def __init__(self, parent=None):
        self._ac_obj = None
        self._child = None
        self._parent = None
        self._pos = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._background_texture = None
        self._background = False
        self._background_color = Color(0, 0, 0, 0)
        self._background_opacity = 0
        self._border = True
        self._border_color = Color(1, 1, 1, 1)
        self._render_callback = None
        self._animation = None
        self._animation_queue = []

        if parent is not None:
            self._parent = parent
            parent._child = self

            if not isinstance(parent, ACApp):
                self.setPos(parent.getPos())
            else:
                self.setPos((0, 0))

            self.setSize(parent.getSize())

    @staticmethod
    def getPosition(obj):
        return ac.getPosition(obj)

    def obj(self):
        return self._ac_obj

    def getChild(self):
        return self._child

    def setChild(self, child):
        if self._child is not None:
            self._child.parent = None

        self._child = child

        if child is not None:
            child._parent = self

        return self

    def getParent(self):
        return self._parent

    def setParent(self, parent):
        if self._parent is not None:
            self._parent.child = None

        self._parent = parent

        if parent is not None:
            parent._child = self

        return self

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

        if self._ac_obj is not None:
            ac.setPosition(self._ac_obj, self._pos[0], self._pos[1])

        return self

    def getSize(self):
        return self._size

    def setSize(self, size):
        self._size = size

        if self._ac_obj is not None:
            ac.setSize(self._ac_obj, self._size[0], self._size[1])

        return self

    def isVisible(self):
        return self._visible

    def setVisible(self, visible):
        self._visible = visible

        if self._ac_obj is not None:
            ac.setVisible(visible)

        return self

    def getBackgroundTexture(self):
        return self._background_texture

    def setBackgroundTexture(self, tex):
        if isinstance(tex, Texture):
            self._background_texture = tex
        elif isinstance(tex, str):
            self._background_texture = ac.newTexture(tex)

        if self._ac_obj is not None:
            ac.setBackgroundTexture(self._ac_obj, self._background_texture.path)

        return self

    def getBackground(self):
        return self._background

    def setBackground(self, background):
        self._background = background

        if self._ac_obj is not None:
            ac.drawBackground(self._ac_obj, self._background)

        return self

    def getBackgroundColor(self):
        return self._background_color

    def setBackgroundColor(self, background_color):
        self._background_color = background_color

        if self._ac_obj is not None:
            col = self._background_color
            ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self._ac_obj, col.a)

        return self

    def getBackgroundOpacity(self):
        return self._background_opacity

    def setBackgroundOpacity(self, background_opacity):
        self._background_opacity = background_opacity

        if self._ac_obj is not None:
            ac.setBackgroundOpacity(self._ac_obj, background_opacity)

        return self

    def isBorderDrawn(self):
        return self._border

    def drawBorder(self, border):
        if isinstance(border, bool):
            self._border = border

        if self._ac_obj is not None:
            ac.drawBorder(self._ac_obj, self._border)

    def getBorderColor(self):
        return self._border_color

    def setBorderColor(self, border_color):
        if isinstance(border_color, Color):
            self._border_color = border_color

        return self

    def show(self):
        if self._ac_obj is not None:
            ac.setVisible(self._ac_obj, True)

    def hide(self):
        if self._ac_obj is not None:
            ac.setVisible(self._ac_obj, False)

    def addAnimation(self, var, start, middle, stop, step, loops=0):
        if self._animation is None:
            self._animation = {"var": var, "start": start, "middle": middle, "stop": stop, "step": step}
        else:
            self._animation_queue.append({"var": var, "start": start, "middle": middle, "stop": stop, "step": step})

    def update(self):
        if self._animation is None:
            if len(self._animation_queue) > 0:
                self._animation = self._animation_queue.pop(0)

        else:
            anim = self._animation
            var = getattr(self, anim["var"])

            if var < anim["stop"]:
                setattr(self, anim["var"], var + anim["step"])
            else:
                if len(self._animation_queue) > 0:
                    self._animation = self._animation_queue.pop(0)
                else:
                    self._animation = None

        if self._child is not None:
            self._child.update()

        if self._background:
            col = self._background_color
            if self._ac_obj is not None:
                ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
                ac.setBackgroundOpacity(self._ac_obj, self._background_opacity)

    def render(self):
        if self._child is not None:
            self._child.render()

        if self._border:
            rect(self._pos[0], self._pos[1], self._size[0], self._size[1], self._border_color, False)


class ACApp(ACWidget):
    def __init__(self, app_name, x, y, w, h, main=None):
        super().__init__()

        self._ac_obj = ac.newApp(app_name)
        self._app_name = app_name
        self._title = False
        self._title_position = (0, 0)
        self._icon = False
        self._icon_position = (0, 0)
        self._position_changed = False
        self._suspended = False
        self._main_app = False
        self._attached = False
        self._attached_apps = []
        self._render_callback = None
        self._activated_callback = None
        self._dismissed_callback = None

        self._activated = self.activate
        self._dismissed = self.dismiss

        a_x, a_y = ac.getPosition(self._ac_obj)
        if a_x != -1:
            self.setPos((a_x, a_y))
        else:
            self.setPos((x, y))
        self.setSize((int(w), int(h)))

        if main is not None:
            main.attach(self)

        self.activated_callback = self._activated
        self.dismissed_callback = self._dismissed

        self.update()

    def isMainApp(self):
        return self._main_app

    def getRenderCallback(self):
        return self._render_callback

    def setRenderCallback(self, render_callback):
        self._render_callback = render_callback

        if self._ac_obj is not None:
            ac.addRenderCallback(self._ac_obj, self._render_callback)

        return self

    def getActivatedCallback(self):
        return self._activated_callback

    def setActivatedCallback(self, activated_callback):
        self._activated_callback = activated_callback

        if self._ac_obj is not None:
            ac.addOnAppActivatedListener(self._ac_obj, self._activated_callback)

        return self

    def getDismissedCallback(self):
        return self._dismissed_callback

    def setDismissedCallback(self, dismissed_callback):
        self._dismissed_callback = dismissed_callback

        if self._ac_obj is not None:
            ac.addOnAppDismissedListener(self._ac_obj, self._dismissed_callback)

        return self

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title

        if self._ac_obj is not None:
            ac.setTitle(self._ac_obj, self._title)

        return self

    def getTitlePosition(self):
        return

    def setTitlePosition(self, title_position):
        self._title_position = title_position

        if self._ac_obj is not None:
            ac.setTitlePosition(self._ac_obj, 0, -10000)

        return self

    def getIcon(self):
        return

    def setIcon(self, icon):
        self._icon = icon

        return self

    def getIconPosition(self):
        return self._icon_position

    def setIconPosition(self, icon_position):
        self._icon_position = icon_position

        if self._ac_obj is not None:
            ac.setIconPosition(self._ac_obj, 0, -10000)

        return self

    def isSuspended(self):
        return self._suspended

    def getPositionChanged(self):
        return self._position_changed

    def app(self):
        return self._ac_obj

    def attach(self, app):
        self._attached_apps.append(app)

        if not app._attached:

            x, y = app.getPos()
            w, h = app.getSize()

            ax, ay = self._pos
            aw, ah = self._size

            # horizontal
            if ax - x <= ay - y or ax + aw - x <= ay + ah - y:
                # left
                if x <= ax + aw / 2:
                    app.setPos((ax - w - 1, ay))
                # right
                elif x > ax + aw / 2:
                    app.setPos((ax + aw + 1, ay))
            # vertical
            else:
                # top
                if y <= ay + ah / 2:
                    app.setPos((ax, ay - h - 1))
                # bottom
                elif y > ay + ah / 2:
                    app.setPos((ax, ay + ah + 1))

            app._attached = True

        return self

    def dettach(self, app):
        if isinstance(app, ACApp):
            self._attached_apps.remove(app)
            app._attached = False
        elif isinstance(app, int) and app < len(self._attached_apps):
            app_obj = self._attached_apps[app]
            app_obj._attached = False
            self._attached_apps[app] = None

        return self

    def hideDecoration(self):
        if self._ac_obj is not None:
            ac.setTitlePosition(self._ac_obj, 0, -10000)
            ac.setIconPosition(self._ac_obj, 0, -10000)

        return self

    def run(self):
        return self._app_name

    def activate(self, val):
        self._suspended = False

    def dismiss(self, val):
        self._suspended = True

    def update(self):
        super().update()

        self._position_changed = False
        col = self._background_color

        if self._ac_obj is not None:
            ac.setBackgroundColor(self._ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self._ac_obj, col.a)

            x, y = ACWidget.getPosition(self._ac_obj)

            if self._pos[0] != x or self._pos[1] != y:
                self.setPos((x, y))
                self._position_changed = True

        return self

    def render(self):
        if self._border:
            rect(0, 0, self._size[0], self._size[1], self._border_color, False)

        return self


class ACLayout(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._children = None


class ACBox(ACLayout):
    def __init__(self, parent=None, orientation=0):
        super().__init__(parent)

        self._children = []
        self._children_count = 0
        self._orientation = orientation

    def addWidget(self, widget):
        self._children.append(widget)
        self._children_count += 1

    def update(self):
        super().update()

        for child in self._children:
            child.update()

    def render(self):
        super().render()

        for child in self._children:
            child.render()


class ACHBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 0)

    def addWidget(self, widget):
        super().addWidget(widget)

        x = self._pos[0]
        w = round(self._size[0] / self._children_count)
        h = self._size[1]

        for c in self._children:
            c.setPos((x, self._pos[1]))
            c.setSize((w, h))
            x += w


class ACVBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 1)

    def addWidget(self, widget):
        super().addWidget(widget)

        y = self._pos[1]
        w = self._size[0]
        h = round(self._size[1] / self._children_count)

        for child in self._children:
            child.setPos((self._pos[0], y))
            child.setSize((w, h))
            y += h


class ACGrid(ACLayout):
    def __init__(self, parent, cols, rows):
        super().__init__(parent)

        self._children = [x[:] for x in [[0] * cols] * rows]
        self._cols = cols
        self._rows = rows
        self._cell_width = round(self._size[0] / self._cols)
        self._cell_height = round(self._size[1] / self._rows)

        if isinstance(parent, ACApp):
            self.setPos((0, 0))

    def getWidget(self, x, y):
        return self._children[y][x]

    def addWidget(self, widget, x, y, w=1, h=1):
        self._children[y][x] = widget

        widget.setPos((round(self._pos[0] + x * self._cell_width), round(self._pos[1] + y * self._cell_height)))
        widget.setSize((round(w * self._cell_width), round(h * self._cell_height)))

        return self

    def updateSize(self):
        self._cell_width = round(self._size[0] / self._cols)
        self._cell_height = round(self._size[1] / self._rows)

        return self

    def update(self):
        for row in self._children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.update()

        return self

    def render(self):
        for row in self._children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.update()

        return self


class ACTextWidget(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._text = ""
        self._text_h_alignment = "center"
        self._text_v_alignment = "middle"
        self._text_color = Color(1, 1, 1, 1)
        self._font_size = 10
        self._font_family = "Roboto Mono"
        self._font_italic = 0
        self._font_bold = 0

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

        if self._ac_obj is not None:
            ac.setText(self._ac_obj, text)

        return self

    def getTextHAlignment(self):
        return self._text_h_alignment

    def setTextHAlignment(self, text_h_alignment="left"):
        self._text_h_alignment = text_h_alignment

        self.setTextAlignment(self._text_h_alignment, self._text_v_alignment)

        return self

    def getTextVAlignment(self):
        return self._text_v_alignment

    def setTextVAlignment(self, text_v_alignment="top"):
        self._text_v_alignment = text_v_alignment

        self.setTextAlignment(self._text_h_alignment, self._text_v_alignment)

        return self

    def setTextAlignment(self, text_h_alignment, text_v_alignment):
        x, y = self._pos

        if text_h_alignment == "left":
            x = self._pos[0]
        elif text_h_alignment == "center":
            x = int(self._pos[0] + self._size[0] / 2)
        elif text_h_alignment == "right":
            x = self._pos[0] + self._size[0]

        if text_v_alignment == "top":
            y = self._pos[1]
        elif text_v_alignment == "middle":
            y = int(self._pos[1] + self._size[1] / 2)
        elif text_v_alignment == "bottom":
            y = self._pos[1] + self._size[1]

        if self._ac_obj is not None:
            ac.setPosition(self._ac_obj, x, y)
            ac.setFontAlignment(self._ac_obj, text_h_alignment)

        return self

    def getTextColor(self):
        return self._text_color

    def setTextColor(self, text_color):
        self._text_color = text_color

        if self._ac_obj is not None:
            ac.setFontColor(self._ac_obj, self._text_color.r, self._text_color.g, self._text_color.b,
                            self._text_color.a)

        return self

    def getFontSize(self):
        return self._font_size

    def setFontSize(self, font_size):
        self._font_size = font_size

        if self._ac_obj is not None:
            ac.setFontSize(self._ac_obj, self._font_size)

        return self

    def isItalic(self):
        return self._font_italic > 0

    def setFontItalic(self, font_italic):
        self._font_italic = font_italic

        if self._ac_obj is not None:
            ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        return self

    def isBold(self):
        return self._font_bold > 0

    def setFontBold(self, font_bold):
        self._font_bold = font_bold

        if self._ac_obj is not None:
            ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        return self

    def setFontStyle(self, family, bold, italic):
        self._font_family = family
        self._font_bold = bold
        self._font_italic = italic

        if self._ac_obj is not None:
            ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        return self

    def getFontFamily(self):
        return self._font_family

    def setFontFamily(self, font_family):
        if isinstance(font_family, str):
            self._font_family = font_family

            if self._ac_obj is not None:
                ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        elif isinstance(font_family, Font):
            self._font_family = font_family.getFontName()

            if self._ac_obj is not None:
                ac.setCustomFont(self._ac_obj, self._font_family, self._font_italic, self._font_bold)

        return self


class ACLabel(ACTextWidget):
    def __init__(self, text, app, parent=None):
        super().__init__(parent)

        self._ac_obj = ac.addLabel(app.app(), text)
        self._text = text

        self.setTextAlignment(self._text_h_alignment, self._text_h_alignment)
        self.setTextColor(self._text_color)
        self.setFontSize(self._font_size)
        self.setFontFamily(self._font_family)
        self.setFontItalic(self._font_italic)
        self.setFontBold(self._font_bold)


class ACIcon(ACLabel):
    def __init__(self, path, app, parent=None):
        super().__init__("", app, parent)

        self.background_texture = path


class ACProgressBar(ACLabel):
    def __init__(self, app, orientation=0, value=0, min_val=0, max_val=100, parent=None):
        super().__init__("", app, parent)

        self._orientation = orientation
        self._border = True
        self._color = self._background_color
        self._h_margin = 1
        self._v_margin = 0.05
        self._value = value
        self._min_val = min_val
        self._max_val = max_val

        if orientation == 1:
            self.h_margin = 0.05
            self.v_margin = 1

    def render(self):
        if self._orientation == 0:
            v_margin = self._size[1] * self.v_margin
            ratio = self._size[0] * (self._value / self._max_val)
            rect(self._pos[0], self._pos[1] + v_margin, ratio, self._size[1] - 2 * v_margin, self._color)

            if self._border:
                rect(self._pos[0], self._pos[1] + v_margin, self._size[0], self._size[1] - 2 * v_margin,
                     self._border_color,
                     False)
        else:
            h_margin = self._size[1] * self.h_margin
            ratio = self._size[1] * (self._value / self._max_val)
            rect(self._pos[0] + h_margin, self._pos[1] + self._size[1] - ratio, self._size[0] - 2 * h_margin, ratio,
                 self._color)

            if self._border:
                rect(self._pos[0] + h_margin, self._pos[1], self._size[0] - 2 * h_margin, self._size[1],
                     self._border_color,
                     False)

        return self
