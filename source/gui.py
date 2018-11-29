from os import stat
import functools
import ac
from source.color import Color
from source.config import loadAppConfig
from source.gl import Texture, rect, texture_rect
from source.event import GUI_EVENT
from source.math import Rect
from source.animation import Animation


class Font:
    def __init__(self, font_name, italic, bold):
        if ac.initFont(0, font_name, italic, bold) == -1:
            raise Exception("Could not load font " + font_name)

        self.font_name = font_name
        self.italic = italic
        self.bold = bold

    def getFontName(self):
        return self.font_name

    def isItalic(self):
        return self.italic > 0

    def isBold(self):
        return self.bold > 0


class ACWidget(object):
    def __init__(self, parent=None):
        self.ac_obj = None
        self.child = None
        self.parent = None
        self.ac_size = (0, 0)
        self.geometry = Rect()
        self.visible = True
        self.background_texture = None
        self.colored_texture = False
        self.texture_color = Color(1, 1, 1, 1)
        self.background = 0
        self.background_color = Color(0, 0, 0, 0)
        self.border = 0
        self.border_color = Color(1, 1, 1, 1)
        self.event_callback = {}
        self.render_callback = None
        self.animation = None
        self.animation_queue = []

        if parent is not None:
            self.parent = parent
            parent.child = self

            if isinstance(parent, ACApp):
                self.setPos((0, 0))
            elif isinstance(parent, ACWidget):
                self.setPos(parent.getPos())

            self.ac_size = parent.getSize()
            self.setSize(parent.getSize())
        else:
            self.setPos((0, 0))

        self.on_click = None
        self.func = None
        self.param = None

    @staticmethod
    def getPosition(obj):
        return ac.getPosition(obj)

    def onClick(self, func, params):
        self.on_click = functools.partial(func, param=params)
        ac.addOnClickedListener(self.ac_obj, self.on_click)

    def obj(self):
        return self.ac_obj

    def getChild(self):
        return self.child

    def setChild(self, child):
        if self.child is not None:
            self.child.parent = None

        self.child = child

        if child is not None:
            child.parent = self

        self.dispatchEvent(GUI_EVENT.ON_CHILD_CHANGED)

        return self

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        if self.parent is not None:
            self.parent.child = None

        self.parent = parent

        if parent is not None:
            parent.child = self

        self.dispatchEvent(GUI_EVENT.ON_PARENT_CHANGED)

        return self

    def setEvent(self, event, callback):
        self.event_callback[event] = callback

    def dispatchEvent(self, event):
        if event in self.event_callback:
            self.event_callback[event]()

    def getGeometry(self):
        return self.geometry

    def setGeometry(self, r):
        self.geometry = r
        self.setPos((r.x, r.y))
        self.setSize((r.w, r.h))
        return self

    def getPos(self):
        return self.geometry.x, self.geometry.y

    def setPos(self, pos):
        self.geometry.x = pos[0]
        self.geometry.y = pos[1]

        if self.ac_obj is not None:
            ac.setPosition(self.ac_obj, self.geometry.x, self.geometry.y)

        self.dispatchEvent(GUI_EVENT.ON_POSITION_CHANGED)

        return self

    def getSize(self):
        return self.geometry.w, self.geometry.h

    def setSize(self, size):
        self.geometry.w = size[0]
        self.geometry.h = size[1]

        self.ac_size = (self.geometry.w, self.geometry.h)

        if self.ac_obj is not None:
            ac.setSize(self.ac_obj, self.geometry.w, self.geometry.h)

        self.dispatchEvent(GUI_EVENT.ON_SIZE_CHANGED)

        return self

    def isVisible(self):
        return self.visible

    def setVisible(self, visible):
        self.visible = visible

        if self.ac_obj is not None:
            ac.setVisible(visible)

        self.dispatchEvent(GUI_EVENT.ON_VISIBILITY_CHANGED)

        return self

    def getBackgroundTexture(self):
        return self.background_texture

    def setBackgroundTexture(self, tex):
        if isinstance(tex, Texture):
            self.background_texture = tex
        elif isinstance(tex, str):
            self.background_texture = ac.newTexture(tex)

        if self.ac_obj is not None:
            ac.setBackgroundTexture(self.ac_obj, self.background_texture.path)

        return self

    def isBackgroundDrawn(self):
        return self.background

    def drawBackground(self, background):
        self.background = background

        if self.ac_obj is not None:
            ac.drawBackground(self.ac_obj, self.background)

        return self

    def getBackgroundColor(self):
        return self.background_color

    def setBackgroundColor(self, background_color):
        self.background_color = background_color
        self.drawBackground(1)

        if self.ac_obj is not None:
            col = self.background_color
            ac.setBackgroundColor(self.ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self.ac_obj, col.a)

        return self

    def getBackgroundOpacity(self):
        return self.background_color.a

    def setBackgroundOpacity(self, background_opacity):
        self.background_color.a = background_opacity

        if self.ac_obj is not None:
            ac.setBackgroundOpacity(self.ac_obj, self.background_color.a)

        return self

    def isBorderDrawn(self):
        return self.border

    def drawBorder(self, border):
        self.border = border

        if self.ac_obj is not None:
            ac.drawBorder(self.ac_obj, self.border)

        return self

    def getBorderColor(self):
        return self.border_color

    def setBorderColor(self, border_color):
        self.border_color = border_color

        self.drawBorder(1)

        return self

    def coloredTexture(self):
        return self.colored_texture

    def setColoredTexture(self, colored):
        self.colored_texture = colored

    def setTextureColor(self, color):
        self.texture_color = color

    def show(self):
        if self.ac_obj is not None:
            ac.setVisible(self.ac_obj, True)

    def hide(self):
        if self.ac_obj is not None:
            ac.setVisible(self.ac_obj, False)

    def addAnimation(self, animation):
        if isinstance(animation, Animation) and animation.isValid():
            self.animation_queue.append(animation)
        return self

    def hasAnimation(self):
        return self.animation is not None

    def updateSize(self):
        pass

    def update(self, delta):
        if self.child is not None:
            self.child.update(delta)

        if self.background:
            col = self.background_color
            if self.ac_obj is not None:
                ac.setBackgroundColor(self.ac_obj, col.r, col.g, col.b)
                ac.setBackgroundOpacity(self.ac_obj, col.a)

        if self.ac_obj is not None:
            # if (self.geometry.x, self.geometry.y) != ac.getPosition(self.ac_obj):
            #     self.dispatchEvent(GUI_EVENT.ON_POSITION_CHANGED)
            #     if self.ac_obj is not None:
            #         x, y = self.getPos()
            #         ac.setPosition(self.ac_obj, x, y)

            if (self.geometry.w, self.geometry.h) != self.ac_size:
                self.dispatchEvent(GUI_EVENT.ON_SIZE_CHANGED)
                self.ac_size = self.getSize()
                if self.ac_obj is not None:
                    ac.setSize(self.ac_obj, self.ac_size[0], self.ac_size[1])

        if self.animation is None:
            if len(self.animation_queue) > 0:
                self.animation = self.animation_queue.pop(0)
                self.animation.init()

        else:
            if not self.animation.isFinished():
                self.animation.update(delta)
            else:
                self.animation = None

        return self

    def render(self, delta):
        r = self.geometry
        if self.border:
            rect(r.x, r.y, r.w, r.h, self.border_color, False)

        if self.colored_texture:
            texture_rect(r.x, r.y, r.w, r.h, self.background_texture, self.texture_color)

        if self.child is not None:
            self.child.render(delta)

        return self


class DockingWidget(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.attachable = True
        self.attached = False
        self.docking_area = Rect()

    def setAttachable(self, attachable):
        self.attachable = attachable
        return self

    def isAttached(self):
        return self.attached

    def setDockingArea(self, area):
        self.docking_area = area
        return self


class ACApp(ACWidget):
    def __init__(self, app_name, x, y, w, h, main=None):
        super().__init__()

        self.ac_obj = ac.newApp(app_name)
        self.app_name = app_name
        self.title = False
        self.title_position = (0, 0)
        self.icon = False
        self.icon_position = (0, 0)
        self.position_changed = False
        self.suspended = False
        self.main_app = False
        self.attached = False
        self.attached_apps = []
        self.render_callback = None
        self.activated_callback = None
        self.dismissed_callback = None
        self.config_file = ""
        self.config_time = 0

        self.activated = self.activate
        self.dismissed = self.dismiss
        self._render = self.render

        a_x, a_y = ac.getPosition(self.ac_obj)
        if a_x != -1:
            self.setPos((a_x, a_y))
        else:
            self.setPos((x, y))
        self.setSize((int(w), int(h)))

        if main is not None:
            main.attach(self)

        self.activated_callback = self.activated
        self.dismissed_callback = self.dismissed
        self.render_callback = self._render

        self.drawBorder(0)
        self.setRenderCallback(self.render_callback)

    def readConfig(self, filename):
        try:
            self.config_file = filename
            self.config_time = stat(self.config_file).st_mtime
            loadAppConfig(self, self.app_name, filename)
        except IOError:
            ac.console("Config file " + filename + " not found.")

        return self

    def configChanged(self):
        if self.config_file != "":
            last_changed = stat(self.config_file).st_mtime

            if last_changed != self.config_time:
                self.config_time = last_changed
                self.dispatchEvent(GUI_EVENT.ON_CONFIG_CHANGED)
                return True
        return False

    def isMainApp(self):
        return self.main_app

    def getRenderCallback(self):
        return self.render_callback

    def setRenderCallback(self, render_callback):
        self.render_callback = render_callback

        if self.ac_obj is not None:
            ac.addRenderCallback(self.ac_obj, self.render_callback)

        return self

    def getActivatedCallback(self):
        return self.activated_callback

    def setActivatedCallback(self, activated_callback):
        self.activated_callback = activated_callback

        if self.ac_obj is not None:
            ac.addOnAppActivatedListener(self.ac_obj, self.activated_callback)

        return self

    def getDismissedCallback(self):
        return self.dismissed_callback

    def setDismissedCallback(self, dismissed_callback):
        self.dismissed_callback = dismissed_callback

        if self.ac_obj is not None:
            ac.addOnAppDismissedListener(self.ac_obj, self.dismissed_callback)

        return self

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

        if self.ac_obj is not None:
            ac.setTitle(self.ac_obj, self.title)

        return self

    def getTitlePosition(self):
        return

    def setTitlePosition(self, title_position):
        self.title_position = title_position

        if self.ac_obj is not None:
            ac.setTitlePosition(self.ac_obj, 0, -10000)

        return self

    def getIcon(self):
        return

    def setIcon(self, icon):
        self.icon = icon

        return self

    def getIconPosition(self):
        return self.icon_position

    def setIconPosition(self, icon_position):
        self.icon_position = icon_position

        if self.ac_obj is not None:
            ac.setIconPosition(self.ac_obj, 0, -10000)

        return self

    def isSuspended(self):
        return self.suspended

    def getPositionChanged(self):
        return self.position_changed

    def init(self):
        pass

    def app(self):
        return self.ac_obj

    def attach(self, app):
        self.attached_apps.append(app)

        if not app.attached:

            x, y = app.getPos()
            w, h = app.getSize()

            ax, ay = self.getPos()
            aw, ah = self.getSize()

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

            app.attached = True

        return self

    def dettach(self, app):
        if isinstance(app, ACApp):
            self.attached_apps.remove(app)
            app.attached = False
        elif isinstance(app, int) and app < len(self.attached_apps):
            app_obj = self.attached_apps[app]
            app_obj.attached = False
            self.attached_apps[app] = None

        return self

    def hideDecoration(self):
        if self.ac_obj is not None:
            ac.setTitlePosition(self.ac_obj, 0, -10000)
            ac.setIconPosition(self.ac_obj, 0, -10000)

        return self

    def run(self):
        return self.app_name

    def activate(self, val):
        self.suspended = False

    def dismiss(self, val):
        self.suspended = True

    def update(self, delta):
        super().update(delta)

        self.position_changed = False
        col = self.background_color

        if self.ac_obj is not None:
            ac.setBackgroundColor(self.ac_obj, col.r, col.g, col.b)
            ac.setBackgroundOpacity(self.ac_obj, col.a)

            x, y = ACWidget.getPosition(self.ac_obj)
            nx, ny = self.getPos()

            if nx != x or ny != y:
                self.setPos((x, y))
                self.position_changed = True

        if self.configChanged():
            self.readConfig(self.config_file)

        return self

    def render(self, delta):
        if self.border:
            s = self.getSize()
            rect(0, 0, s[0], s[1], self.border_color, False)

        if self.child is not None:
            self.child.render(delta)

        return self


class ACLayout(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.children = None

    def getChildren(self):
        return self.children


class ACBox(ACLayout):
    def __init__(self, parent=None, orientation=0):
        super().__init__(parent)

        self.children = []
        self.children_count = 0
        self.orientation = orientation

    def addWidget(self, widget):
        self.children.append(widget)
        self.children_count += 1

    def update(self, delta):
        super().update(delta)

        for child in self.children:
            child.update(delta)

    def render(self, delta):
        super().render(delta)

        for child in self.children:
            child.render(delta)


class ACHBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 0)

    def addWidget(self, widget):
        super().addWidget(widget)

        x, y = self.getPos()
        w, h = self.getSize()
        nw = round(w / self.children_count)

        for c in self.children:
            c.setPos((x, h))
            c.setSize((nw, h))
            x += nw


class ACVBox(ACBox):
    def __init__(self, parent=None):
        super().__init__(parent, 1)

    def addWidget(self, widget):
        super().addWidget(widget)

        x, y = self.getSize()
        w, h = self.getSize()
        nh = round(h / self.children_count)

        for child in self.children:
            child.setPos((x, y))
            child.setSize((w, nh))
            y += nh


class ACGrid(ACLayout):
    def __init__(self, parent, cols, rows):
        super().__init__(parent)

        self.cols = max(cols, 1)
        self.rows = max(rows, 1)
        self.children = [x[:] for x in [[0] * self.cols] * self.rows]
        self.dimension = [x[:] for x in [[(0, 0)] * self.cols] * self.rows]
        self.cell_width = round(self.geometry.w / self.cols)
        self.cell_height = round(self.geometry.h / self.rows)

    def getWidget(self, x, y):
        return self.children[y][x]

    def addWidget(self, widget, x, y, w=1, h=1):
        if isinstance(widget, ACWidget):
            self.children[y][x] = widget
            self.dimension[y][x] = (w, h)

            widget.setPos((round(self.geometry.x + x * self.cell_width),
                           round(self.geometry.y + y * self.cell_height)))
            widget.setSize((round(w * self.cell_width), round(h * self.cell_height)))

            widget.updateSize()

        return self

    def updateSize(self):
        self.cell_width = round(self.geometry.w / self.cols)
        self.cell_height = round(self.geometry.h / self.rows)

        for y, row in enumerate(self.children):
            for x, cell in enumerate(row):
                if isinstance(cell, ACWidget):
                    cell.setPos(
                        (round(self.geometry.x + x * self.cell_width),
                         round(self.geometry.y + y * self.cell_height)))
                    cell.setSize((round(self.dimension[y][x][0] * self.cell_width),
                                  round(self.dimension[y][x][1] * self.cell_height)))
                    cell.updateSize()
        return self

    def update(self, delta):
        super().update(delta)

        for row in self.children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.update(delta)

        return self

    def render(self, delta):
        super().render(delta)

        for row in self.children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.render(delta)

        return self


class ACLabelPair(ACGrid):
    def __init__(self, app, parent=None, label=None, widget=None, label_pos="left"):
        if label_pos == "left" or label_pos == "right":
            super().__init__(parent, 2, 1)
        elif label_pos == "top" or label_pos == "bottom":
            super().__init__(parent, 1, 2)

        self.label_widget = label
        self.pair_widget = widget
        self.label_position = label_pos

        self.addLabelWidget(label)
        self.addPairWidget(widget)

    def addLabelWidget(self, label):
        if isinstance(label, ACLabel):
            self.label_widget = label

            if self.label_position == "left" or self.label_position == "top":
                self.addWidget(self.label_widget, 0, 0)
            elif self.label_position == "right":
                self.addWidget(self.label_widget, 1, 0)
            elif self.label_position == "bottom":
                self.addWidget(self.label_widget, 0, 1)

        return self

    def addPairWidget(self, widget):
        if isinstance(widget, ACWidget):
            self.pair_widget = widget

            if self.label_position == "left":
                self.addWidget(self.pair_widget, 1, 0)
            elif self.label_position == "right" or self.label_position == "bottom":
                self.addWidget(self.pair_widget, 0, 0)
            elif self.label_position == "top":
                self.addWidget(self.pair_widget, 0, 1)
        return self

    def render(self, delta):
        if self.label_widget:
            self.label_widget.render(delta)
        if self.pair_widget:
            self.pair_widget.render(delta)
        return self


class ACTextWidget(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.text = ""
        self.text_h_alignment = "center"
        self.text_v_alignment = "middle"
        self.text_color = Color(1, 1, 1, 1)
        self.font_size = 10
        self.font_family = "Roboto Mono"
        self.font_italic = 0
        self.font_bold = 0

    def getText(self):
        return self.text

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        self.text = text

        if self.ac_obj is not None:
            ac.setText(self.ac_obj, text)
        return self

    def getTextHAlignment(self):
        return self.text_h_alignment

    def setTextHAlignment(self, text_h_alignment="left"):
        self.text_h_alignment = text_h_alignment

        self.setTextAlignment()
        return self

    def getTextVAlignment(self):
        return self.text_v_alignment

    def setTextVAlignment(self, text_v_alignment="top"):
        self.text_v_alignment = text_v_alignment

        self.setTextAlignment()
        return self

    def setTextAlignment(self):
        x, y = self.getPos()

        # if self.text_h_alignment == "left":  # or self.text_h_alignment == "l":
        #     x = self.pos[0]
        # elif self.text_h_alignment == "center":  # or self.text_h_alignment == "c":
        #     x = int(self.pos[0] + self.size[0] / 2)
        # elif self.text_h_alignment == "right":  # or self.text_h_alignment == "r":
        #     x = self.pos[0] + self.size[0]

        # if self.text_v_alignment == "top":  # or self.text_v_alignment == "t":
        #     y = self.pos[1]
        # elif self.text_v_alignment == "middle":  # or self.text_v_alignment == "m":
        #     y = int(self.pos[1] + self.size[1] / 2 - self.font_size / 2)
        # elif self.text_v_alignment == "bottom":  # or self.text_v_alignment == "b":
        #     y = self.pos[1] + self.size[1]

        if self.ac_obj is not None:
            ac.setFontAlignment(self.ac_obj, self.text_h_alignment)
            # self.setPos((x, y))
        return self

    def getTextColor(self):
        return self.text_color

    def setTextColor(self, text_color):
        self.text_color = text_color

        if self.ac_obj is not None:
            ac.setFontColor(self.ac_obj, self.text_color.r, self.text_color.g, self.text_color.b,
                            self.text_color.a)
        return self

    def getFontSize(self):
        return self.font_size

    def setFontSize(self, font_size):
        self.font_size = font_size  # min(font_size, self.size[1])

        if self.ac_obj is not None:
            ac.setFontSize(self.ac_obj, self.font_size)
        return self

    def isItalic(self):
        return self.font_italic > 0

    def setFontItalic(self, font_italic):
        self.font_italic = font_italic

        if self.ac_obj is not None:
            ac.setCustomFont(self.ac_obj, self.font_family, self.font_italic, self.font_bold)
        return self

    def isBold(self):
        return self.font_bold > 0

    def setFontBold(self, font_bold):
        self.font_bold = font_bold

        if self.ac_obj is not None:
            ac.setCustomFont(self.ac_obj, self.font_family, self.font_italic, self.font_bold)
        return self

    def setFontStyle(self, family, bold, italic):
        self.font_family = family
        self.font_bold = bold
        self.font_italic = italic

        if self.ac_obj is not None:
            ac.setCustomFont(self.ac_obj, self.font_family, self.font_italic, self.font_bold)
        return self

    def getFontFamily(self):
        return self.font_family

    def setFontFamily(self, font_family):
        if isinstance(font_family, str):
            self.font_family = font_family

            if self.ac_obj is not None:
                ac.setCustomFont(self.ac_obj, self.font_family, self.font_italic, self.font_bold)

        elif isinstance(font_family, Font):
            self.font_family = font_family.getFontName()

            if self.ac_obj is not None:
                ac.setCustomFont(self.ac_obj, self.font_family, self.font_italic, self.font_bold)
        return self

    def updateSize(self):
        self.setTextAlignment()


class ACLabel(ACTextWidget):
    def __init__(self, text, app, parent=None, font_size=12, bold=0, italic=0,
                 text_h_alignment="left", text_v_alignment="top",
                 text_color=Color(1, 1, 1, 1), background_color=Color(0, 0, 0, 0)):
        super().__init__(parent)

        self.ac_obj = ac.addLabel(app.app(), text)
        self.text = text
        self.font_size = font_size
        self.font_bold = bold
        self.font_italic = italic
        self.text_h_alignment = text_h_alignment
        self.text_v_alignment = text_v_alignment
        self.text_color = text_color
        self.background_color = background_color

        self.setBackgroundColor(self.background_color)
        self.setTextAlignment()
        self.setTextColor(self.text_color)
        self.setFontSize(self.font_size)
        self.setFontFamily(self.font_family)
        self.setFontItalic(self.font_italic)
        self.setFontBold(self.font_bold)


class ACButton(ACTextWidget):
    def __init__(self, text, app, parent=None, font_size=12, bold=0, italic=0,
                 text_h_alignment="left", text_v_alignment="top",
                 text_color=Color(1, 1, 1, 1), background_color=Color(0, 0, 0, 0)):
        super().__init__(parent)

        self.ac_obj = ac.addButton(app.app(), text)
        self.text = text
        self.font_size = font_size
        self.font_bold = bold
        self.font_italic = italic
        self.text_h_alignment = text_h_alignment
        self.text_v_alignment = text_v_alignment
        self.text_color = text_color
        self.background_color = background_color

        self.setBackgroundColor(self.background_color)
        self.setTextAlignment()
        self.setTextColor(self.text_color)
        self.setFontSize(self.font_size)
        self.setFontFamily(self.font_family)
        self.setFontItalic(self.font_italic)
        self.setFontBold(self.font_bold)


class ACIcon(ACLabel):
    def __init__(self, path, app, parent=None):
        super().__init__("", app, parent)

        self.background_texture = path


class ACProgressBar(ACLabel):
    def __init__(self, app, orientation=0, value=0, min_val=0, max_val=100, parent=None):
        super().__init__("", app, parent)

        self.orientation = orientation
        self.border = 1
        self.color = self.background_color
        self.h_margin = 1
        self.v_margin = 0.05
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

        if orientation == 1:
            self.h_margin = 0.05
            self.v_margin = 1

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()

        if self.orientation == 0:
            v_margin = h * self.v_margin
            ratio = w * (self.value / self.max_val)
            rect(x, y + v_margin, ratio, h - 2 * v_margin, self.color)

            if self.border:
                rect(x, y + v_margin, w, h - 2 * v_margin, self.border_color, False)
        else:
            h_margin = h * self.h_margin
            ratio = h * (self.value / self.max_val)
            rect(x + h_margin, y + h - ratio, w - 2 * h_margin, ratio, self.color)

            if self.border:
                rect(x + h_margin, y, w - 2 * h_margin, h, self.border_color, False)

        return self


class ACSpinner(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)


class ACInput(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)


class ACGraph(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
