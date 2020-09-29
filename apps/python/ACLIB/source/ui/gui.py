from os import stat, path
import functools
import ac

from ui.color import Color
from ui.gl import Texture, rect, texture_rect
from ui.animation import Animation
from storage.config import loadAppConfig, Config
from util.math import Rect, Point
from util.windows import *


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


class Font:
    def __init__(self, font_name, italic, bold):
        if ac.initFont(0, font_name, italic, bold) == -1:
            raise Exception('Could not load font ' + font_name)

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
    def __init__(self, parent=None, app=None):
        self.ac_obj = None
        self.app = app
        self.child = None
        self.parent = None
        self.ac_size = (0, 0)
        self.ac_pos = (0, 0)
        self.pos_changed = False
        self.global_geometry = Rect()
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
        self.animation = None
        self.animation_queue = []

        if parent is not None:
            self.parent = parent
            parent.child = self

            if parent.app is not None:
                self.app = parent.app

            if isinstance(parent, ACApp):
                self.app = parent
                self.setPos((0, 0))
            elif isinstance(parent, ACWidget):
                self.setPos(parent.getPos())

            self.ac_size = parent.getSize()
            self.setSize(parent.getSize())
        else:
            self.setPos((0, 0))

        self.on_click = None

    def getGlobalGeometry(self):
        return self.global_geometry

    def getGlobalPos(self):
        return self.global_geometry.x, self.global_geometry.y

    @staticmethod
    def getPosition(obj):
        return ac.getPosition(obj)

    def loadStyle(self):
        if self.app is not None:
            if self.app.style:
                d = self.app.style.dictionary
                name = self.__class__.__name__
                if name in d:
                    for option in d[name]:
                        if hasattr(self, option):
                            setattr(self, option, d[name][option])
        if self.child is not None:
            self.child.loadStyle()
        return self

    def onClick(self, func, params):
        self.on_click = functools.partial(func, param=params)
        ac.addOnClickedListener(self.ac_obj, self.on_click)

    def getObj(self):
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
        if event in self.event_callback:
            self.event_callback[event].append(callback)
        else:
            self.event_callback[event] = []
            self.event_callback[event].append(callback)

    def dispatchEvent(self, event):
        if event in self.event_callback:
            for callback in self.event_callback[event]:
                callback()

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

        if self.parent is not None:
            self.global_geometry = self.parent.global_geometry + Rect(self.geometry.x, self.geometry.y, 0, 0)
        else:
            self.global_geometry = self.geometry

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
            ac.setVisible(self.ac_obj, visible)

        self.dispatchEvent(GUI_EVENT.ON_VISIBILITY_CHANGED)
        return self

    def getBackgroundTexture(self):
        return self.background_texture

    def setBackgroundTexture(self, tex):
        if isinstance(tex, Texture):
            self.background_texture = tex
        elif isinstance(tex, str):
            self.background_texture = ac.newTexture(tex)

        if self.ac_obj is not None and isinstance(self.background_texture, Texture):
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
        if isinstance(animation, Animation) and animation.is_valid():
            self.animation_queue.append(animation)
        return self

    def hasAnimation(self):
        return self.animation is not None

    def updateSize(self):
        if self.child is not None:
            self.child.updateSize()
        return self

    def update(self, delta):
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
            if not self.animation.is_finished():
                self.animation.update(delta)
            else:
                self.animation = None

        if self.child is not None:
            self.child.update(delta)
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


class ACApp(ACWidget):
    def __init__(self, app_name, x, y, w, h):
        super().__init__()

        self.ac_obj = ac.newApp(app_name)
        self.app_name = app_name
        self.title = False
        self.title_position = (0, 0)
        self.icon = False
        self.icon_position = (0, 0)
        self.position_changed = False
        self.suspended = False
        self.attached = False
        self.attached_apps = []
        self._is_init = False
        self._render_callback = None
        self._activated_callback = None
        self._dismissed_callback = None
        self.update_timer = 0
        self.update_time = 0.005
        self.render_timer = 0
        self.render_time = 0
        self.config_file = ''
        self.config_time = 0
        self.style = None
        self.style_file = ''
        self.style_time = 0

        self._activated = self.activate
        self._dismissed = self.dismiss
        self._render = self.render

        a_x, a_y = ac.getPosition(self.ac_obj)
        if a_x != -1:
            self.setPos((a_x, a_y))
        else:
            self.setPos((x, y))
        self.setSize((int(w), int(h)))

        self._activated_callback = self._activated
        self._dismissed_callback = self._dismissed
        self._render_callback = self._render

        self.drawBorder(0)
        self.setRenderCallback(self._render_callback)

        self.readConfig('apps/python/ACLIB/config/' + self.app_name + '.ini')
        self.readStyle('apps/python/ACLIB/style/' + self.app_name + '.ini')

    def readConfig(self, filename):
        if path.exists(filename):
            self.config_file = filename
            self.config_time = stat(self.config_file).st_mtime
            loadAppConfig(self, self.app_name, filename)
        return self

    def readStyle(self, filename):
        if path.exists(filename):
            self.style_file = filename
            self.style_time = stat(self.style_file).st_mtime
            self.style = Config(filename)
            self.loadStyle()
        return self

    def configChanged(self):
        if self.config_file != '':
            last_changed = stat(self.config_file).st_mtime

            if last_changed != self.config_time:
                self.config_time = last_changed
                self.dispatchEvent(GUI_EVENT.ON_CONFIG_CHANGED)
                return True
        return False

    def styleChanged(self):
        if self.style_file != '':
            last_changed = stat(self.style_file).st_mtime

            if last_changed != self.style_time:
                self.style_time = last_changed
                self.dispatchEvent(GUI_EVENT.ON_STYLE_CHANGED)
                return True
        return False

    def getRenderCallback(self):
        return self._render_callback

    def setRenderCallback(self, render_callback):
        self._render_callback = render_callback

        if self.ac_obj is not None:
            ac.addRenderCallback(self.ac_obj, self._render_callback)

        return self

    def getActivatedCallback(self):
        return self._activated_callback

    def setActivatedCallback(self, activated_callback):
        self._activated_callback = activated_callback

        if self.ac_obj is not None:
            ac.addOnAppActivatedListener(self.ac_obj, self._activated_callback)

        return self

    def getDismissedCallback(self):
        return self._dismissed_callback

    def setDismissedCallback(self, dismissed_callback):
        self._dismissed_callback = dismissed_callback

        if self.ac_obj is not None:
            ac.addOnAppDismissedListener(self.ac_obj, self._dismissed_callback)

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

    def getApp(self):
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

    def init(self):
        pass

    def update(self, delta):
        super().update(delta)

        if not self._is_init:
            self.init()
            self._is_init = True

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

        if self.styleChanged():
            self.readStyle(self.style_file)

        return self

    def render(self, delta):
        super().render(delta)

        if self.border:
            s = self.getSize()
            rect(0, 0, s[0], s[1], self.border_color, False)

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

    def loadStyle(self):
        super().loadStyle()

        for c in self.children:
            if isinstance(c, ACWidget):
                c.loadStyle()

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

    def loadStyle(self):
        super().loadStyle()

        for row in self.children:
            for cell in row:
                if isinstance(cell, ACWidget):
                    cell.loadStyle()
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


class ACDragableWidget(ACWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.mouse_hover = False
        self.mouse_focus = False
        self.last_pos = (0, 0)

    def update(self, delta):
        super().update(delta)

        m_x, m_y = System.getMousePosition()

        if self.mouse_focus:
            p_x, p_y = self.getPos()
            x, y = p_x + self.last_pos[0] - m_x, p_y + self.last_pos[1] - m_y
            self.setPos((x, y))

        self.mouse_hover = Rect.pointInRect(Point(m_x, m_y), self.global_geometry)

        if self.mouse_hover and System.keyPressed(KEY.LEFT_MOUSE):
            self.last_pos = System.getMousePosition()
            self.mouse_focus = True
        else:
            self.mouse_focus = False

        return self


class ACDockingWidget(ACDragableWidget):
    DockingWidgets = []

    def __init__(self, parent, space=5):
        super().__init__(parent=parent)

        self.space = space
        self.ratio = 0.5
        self.attachable = True
        self.attached = False
        self.docking_area = Rect()

        self.setDockingSpace(self.space)

        ACDockingWidget.DockingWidgets.append(self)

    def setAttachable(self, attachable):
        self.attachable = attachable
        return self

    def isAttached(self):
        return self.attached

    def setDockingSpace(self, space):
        self.space = space
        self.docking_area = self.geometry + Rect(-self.space, -self.space, self.space, self.space)
        return self

    def update(self, delta):
        super().update(delta)

        if self.attachable:
            if len(ACDockingWidget.DockingWidgets) > 1 and self.pos_changed:
                self.setDockingSpace(self.space)
                for w in ACDockingWidget.DockingWidgets:
                    if w != self:
                        if Rect.rectOverlapping(self.docking_area, w.geometry):
                            pass

        return self


class ACTextWidget(ACWidget):
    def __init__(self, parent=None, app=None):
        super().__init__(parent, app)

        self.text = ''
        self.text_h_alignment = 'center'
        self.text_v_alignment = 'middle'
        self.text_color = Color(1, 1, 1, 1)
        self.font_size = 10
        self.font_family = 'Roboto Mono'
        self.font_italic = 0
        self.font_bold = 0

        self.loadStyle()

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

    def setTextHAlignment(self, text_h_alignment='left'):
        self.text_h_alignment = text_h_alignment

        self.setTextAlignment()
        return self

    def getTextVAlignment(self):
        return self.text_v_alignment

    def setTextVAlignment(self, text_v_alignment='top'):
        self.text_v_alignment = text_v_alignment

        self.setTextAlignment()
        return self

    def setTextAlignment(self):
        x, y = self.getPos()

        # if self.text_h_alignment == 'left':  # or self.text_h_alignment == 'l':
        #     x = self.pos[0]
        # elif self.text_h_alignment == 'center':  # or self.text_h_alignment == 'c':
        #     x = int(self.pos[0] + self.size[0] / 2)
        # elif self.text_h_alignment == 'right':  # or self.text_h_alignment == 'r':
        #     x = self.pos[0] + self.size[0]

        # if self.text_v_alignment == 'top':  # or self.text_v_alignment == 't':
        #     y = self.pos[1]
        # elif self.text_v_alignment == 'middle':  # or self.text_v_alignment == 'm':
        #     y = int(self.pos[1] + self.size[1] / 2 - self.font_size / 2)
        # elif self.text_v_alignment == 'bottom':  # or self.text_v_alignment == 'b':
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
                 text_h_alignment='left', text_v_alignment='top',
                 text_color=Color(1, 1, 1, 1), background_color=Color(0, 0, 0, 0)):
        super().__init__(parent, app)

        self.ac_obj = ac.addLabel(app.getApp(), text)
        self.text = text
        self.font_size = font_size
        self.font_bold = bold
        self.font_italic = italic
        self.text_h_alignment = text_h_alignment
        self.text_v_alignment = text_v_alignment
        self.text_color = text_color
        self.background_color = background_color

        self.loadStyle()

        self.setBackgroundColor(self.background_color)
        self.setTextAlignment()
        self.setTextColor(self.text_color)
        self.setFontSize(self.font_size)
        self.setFontFamily(self.font_family)
        self.setFontItalic(self.font_italic)
        self.setFontBold(self.font_bold)


class ACLabelPair(ACGrid):
    def __init__(self, app, parent=None, label=None, widget=None, label_pos='left'):
        if label_pos == 'left' or label_pos == 'right':
            super().__init__(parent, 2, 1)
        elif label_pos == 'top' or label_pos == 'bottom':
            super().__init__(parent, 1, 2)

        self.label_widget = label
        self.pair_widget = widget
        self.label_position = label_pos

        self.loadStyle()

        self.addLabelWidget(label)
        self.addPairWidget(widget)

    def addLabelWidget(self, label):
        if isinstance(label, ACLabel):
            self.label_widget = label

            if self.label_position == 'left' or self.label_position == 'top':
                self.addWidget(self.label_widget, 0, 0)
            elif self.label_position == 'right':
                self.addWidget(self.label_widget, 1, 0)
            elif self.label_position == 'bottom':
                self.addWidget(self.label_widget, 0, 1)
        return self

    def addPairWidget(self, widget):
        if isinstance(widget, ACWidget):
            self.pair_widget = widget

            if self.label_position == 'left':
                self.addWidget(self.pair_widget, 1, 0)
            elif self.label_position == 'right' or self.label_position == 'bottom':
                self.addWidget(self.pair_widget, 0, 0)
            elif self.label_position == 'top':
                self.addWidget(self.pair_widget, 0, 1)
        return self

    def render(self, delta):
        if self.label_widget:
            self.label_widget.render(delta)
        if self.pair_widget:
            self.pair_widget.render(delta)
        return self


class ACButton(ACTextWidget):
    def __init__(self, text, app, parent=None, font_size=12, bold=0, italic=0,
                 text_h_alignment='left', text_v_alignment='top',
                 text_color=Color(1, 1, 1, 1), background_color=Color(0, 0, 0, 0)):
        super().__init__(parent)

        self.ac_obj = ac.addButton(app.getApp(), text)
        self.text = text
        self.font_size = font_size
        self.font_bold = bold
        self.font_italic = italic
        self.text_h_alignment = text_h_alignment
        self.text_v_alignment = text_v_alignment
        self.text_color = text_color
        self.background_color = background_color

        self.loadStyle()

        self.setBackgroundColor(self.background_color)
        self.setTextAlignment()
        self.setTextColor(self.text_color)
        self.setFontSize(self.font_size)
        self.setFontFamily(self.font_family)
        self.setFontItalic(self.font_italic)
        self.setFontBold(self.font_bold)


class ACIcon(ACLabel):
    def __init__(self, path, app, parent=None):
        super().__init__('', app, parent)

        self.background_texture = path

        self.loadStyle()


class ACProgressBar(ACLabel):
    def __init__(self, app, orientation=0, value=0, min_val=0, max_val=100, parent=None):
        super().__init__('', app, parent)

        self.orientation = orientation
        self.border = 1
        self.color = Color(1, 0, 0)
        self.h_margin = 1
        self.v_margin = 0.05
        self.value = value
        self.min_val = min_val
        self.max_val = max(max_val, 1)

        if orientation == 1:
            self.h_margin = 0.05
            self.v_margin = 1

        self.loadStyle()

    def render(self, delta):
        x, y = self.getPos()
        w, h = self.getSize()

        if self.orientation == 0:
            v_margin = h * self.v_margin
            ratio = w * (self.value / self.max_val)
            rect(x, y + v_margin, ratio, h - 2 * v_margin, self.color)

            if self.border:
                rect(x, y + v_margin, w, h - 2 * v_margin, self.border_color, False)
        # elif self.orientation == 1:
        #     h_margin = h * self.h_margin
        #     ratio = h * (self.value / self.max_val)
        #     rect(x + h_margin, y + h - ratio, w - 2 * h_margin, ratio, self.color)
        #
        #     if self.border:
        #         rect(x + h_margin, y, w - 2 * h_margin, h, self.border_color, False)
        return self


class ACSpinner(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)


class ACInput(ACWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)


class ACGraph(ACWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.points = {}
        self.key = 0

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')

        self.x_dist = 0
        self.x_ratio = 0
        self.y_dist = 0
        self.y_ratio = 0

        self.x_axis = True
        self.x_axis_size = 3
        self.border = 1

        self.draw_colors = [Color(1, 1, 1)]
        self.background_colors = [Color(0, 0, 0, 0.5)]

    def __iter__(self):
        return iter(self.points)

    def __iadd__(self, other):
        if isinstance(other, tuple):
            self.x_max = max(self.x_max, other[0])
            self.x_min = min(self.x_min, other[0])
            self.y_max = max(self.y_max, other[1])
            self.y_min = min(self.y_min, other[1])
            self.points[other[0]] = other[1]
            self.key = other[0] + 1
        elif isinstance(other, list):
            for i in other:
                self.x_max = max(self.x_max, self.key)
                self.x_min = min(self.x_min, self.key)
                self.y_max = max(self.y_max, i)
                self.y_min = min(self.y_min, i)
                self.points[self.key] = i
                self.key += 1
        else:
            self.x_max = max(self.x_max, self.key)
            self.x_min = min(self.x_min, self.key)
            self.y_max = max(self.y_max, other)
            self.y_min = min(self.y_min, other)
            self.points[self.key] = other
            self.key += 1

        self.calc()
        return self

    def __setitem__(self, key, value):
        self.x_max = max(self.x_max, key)
        self.x_min = min(self.x_min, key)
        self.y_max = max(self.y_max, value)
        self.y_min = min(self.y_min, value)
        self.points[key] = value
        self.key = key + 1

        self.calc()
        return self

    def setDrawColors(self, colors):
        if isinstance(colors, list):
            self.draw_colors = colors

    def setBackgroundColors(self, colors):
        if isinstance(colors, list):
            self.background_colors = colors

    def setPoints(self, points):
        for k in points:
            self[k] = points[k]

    def setColor(self, c):
        ac.glColor4f(c.r, c.g, c.b, c.a)

    def calc(self):
        if len(self.points) > 0:
            self.x_dist = self.x_max - self.x_min
            if self.x_dist > 0:
                self.x_ratio = self.geometry.w / self.x_dist
            else:
                self.x_ratio = self.geometry.w / 100

            # self.x_ratio = self.geometry.w / max(self.key, 1)

            self.y_dist = self.y_max - self.y_min
            if self.y_dist > 0:
                self.y_ratio = self.geometry.h / self.y_dist
            else:
                self.y_ratio = self.geometry.h / 100

    def reset(self):
        self.points = {}
        self.key = 0

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')

        self.x_dist = 0
        self.x_ratio = 0
        self.y_dist = 0
        self.y_ratio = 0

    def update(self, delta):
        super().update(delta)

    def render(self, delta):
        super().update(delta)

    def paint(self):
        x, y = self.getPos()
        w, h = self.getSize()

        step = w * (1 / len(self.background_colors))
        current = x

        for c in self.background_colors:
            rect(current, y, step, h, c)
            current += step

        if len(self.points) > 0 and self.x_axis and self.y_max != float('-inf'):
            rect(x, y + self.y_max * self.y_ratio - 1, w, self.x_axis_size)


class ACLineGraph(ACGraph):
    def __init__(self, parent=None):
        super().__init__(parent)

    def render(self, delta):
        super().render(delta)

        self.paint()

        x, y = self.getPos()
        w, h = self.getSize()
        current = 0

        ac.glBegin(1)

        self.setColor(self.draw_colors[0])

        for p in sorted(self.points):
            if p * self.x_ratio > w / len(self.draw_colors) * current:
                c = self.draw_colors[current]
                self.setColor(c)
                current = min(current + 1, len(self.draw_colors) - 1)

            ac.glVertex2f(x + p * self.x_ratio, y + self.y_max * self.y_ratio - self.points[p] * self.y_ratio)

        ac.glEnd()

        return self


class ACAreaGraph(ACGraph):
    def __init__(self, parent=None):
        super().__init__(parent)

    def render(self, delta):
        super().render(delta)

        x, y = self.getPos()
        w, h = self.getSize()
        current = 0

        self.paint()
        self.setColor(self.draw_colors[current])

        ac.glBegin(1)

        for p in sorted(self.points):
            if p * self.x_ratio > w / len(self.draw_colors) * current:
                c = self.draw_colors[current]
                self.setColor(c)
                current = min(current + 1, len(self.draw_colors) - 1)

            ac.glVertex2f(x + p * self.x_ratio, y + self.y_max * self.y_ratio - self.points[p] * self.y_ratio)

        ac.glEnd()

        return self