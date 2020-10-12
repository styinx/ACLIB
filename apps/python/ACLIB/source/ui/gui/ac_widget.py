import ac
from ui import gl
from ui.animation import Animation

from ui.color import Color
from ui.gui.font import Font, pt2px, px2pt
from ui.gui.defaults import WidgetStyle, WidgetConfig
from util.event import EventListener
from util.log import log, console, tb
from util.observer import Observer


class ACWidget(EventListener):
    """
    The ACWidget class is the base class for all UI elements that are used to display or draw something.
    """

    class EVENT:
        """
        The EVENT class inhabits all UI events that can occur.
        Note that also events form child classes are stored here.
        """
        ACTIVATED = 'Activated'
        ANIMATION_ADDED = 'Animation Added'
        ANIMATION_FINISHED = 'Animation Finished'
        BACKGROUND_CHANGED = 'Background Changed'
        CHILD_CHANGED = 'Child Changed'
        CLICK = 'Click'
        CONFIG_CHANGED = 'Config Changed'
        DISMISSED = 'Dismissed'
        PARENT_CHANGED = 'Parent Changed'
        PROGRESS_CHANGED = 'Progress Changed'
        POSITION_CHANGED = 'Position Changed'
        SIZE_CHANGED = 'Size Changed'
        STYLE_CHANGED = 'Style Changed'
        TEXT_CHANGED = 'Text Changed'
        VISIBILITY_CHANGED = 'Visibility Changed'

    class PROPERTY:
        """
        The PROPERTY class holds all members of a class that can be overwritten from a configuration file.
        """
        BACKGROUND = 'background'
        BACKGROUND_COLOR = 'background_color'
        BORDER = 'border'
        BORDER_COLOR = 'border_color'

    IDS = {}

    def __init__(self, parent=None):
        super().__init__()

        self._id = -1
        self._parent = parent
        self._child = None

        self._position = (0, 0)
        self._size = (0, 0)
        self._visible = True
        self._background = True
        self._border = False
        self._background_texture = ''
        self._background_color = Color(0.0, 0.0, 0.0, 0.0)
        self._border_color = Color(0.0, 0.0, 0.0, 0.0)

        self._active_animation = None
        self._animation_queue = []

        self.on(ACWidget.EVENT.PARENT_CHANGED, self._on_parent_changed)
        self.on(ACWidget.EVENT.POSITION_CHANGED, self._on_position_changed)
        self.on(ACWidget.EVENT.SIZE_CHANGED, self._on_size_changed)

        try:
            app_name = None if not self.app else self.app.__class__.__name__
            WidgetStyle.load_style_from_config(self, self.__class__.__name__, app_name)
        except Exception as e:
            console('Problems while loading style for class "{}"'.format(self.__class__.__name__))
            tb(e)

    def __str__(self):
        return '{} ({})'.format(self.__class__.__name__, self._id)

    # Private

    def _on_id(self):
        self.size = self.size
        self.position = self.position
        self.visible = self.visible
        self.background = self.background
        self.border = self.border
        self.background_texture = self.background_texture
        self.background_color = self.background_color
        self.border_color = self.border_color

        self.parent = self._parent

        if self.has_id:
            ac.addOnClickedListener(self.id, ACWidget._event_function(ACWidget.EVENT.CLICK, self))

    def _on_parent_changed(self):
        self.position = (0, 0) if isinstance(self.parent, ACApp) else self.parent.position
        self.size = self.parent.size

    def _on_position_changed(self):
        if self.child:
            self.child.position = self.position

    def _on_size_changed(self):
        if self.child:
            self.child.size = self.size

    @staticmethod
    def _event_function(event: str, widget):
        def func(*args):
            if widget.has_id:
                widget.fire(event, widget, *args)

        if widget.has_id:
            globals()['on{}_{}'.format(event.replace(' ', '_'), widget.id)] = func
        return func

    # Public

    @staticmethod
    def get_control(_id: int):
        if _id in ACWidget.IDS:
            return ACWidget.IDS[_id]
        return None

    @property
    def app(self):
        """
        :return:    Returns the id of the app (created with ac.newApp) in order to create new controls and
                    associate it with the app. If the current control is not an instance of ACApp the function
                    calls its parent control until an instance of ACApp is reached.
                    If a control does not have an associated app (should never occur since a control without an app
                    can not be instantiated) it returns its own id.
        """
        if isinstance(self, ACApp):
            return self._id

        if self.parent:
            return self.parent.app

        return self._id

    @property
    def has_id(self):
        return self.id != -1

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, _id: int):
        self._id = _id

        if _id != -1:
            ACWidget.IDS[self.id] = self

            self._on_id()
        else:
            console('{}: Id could not be set.'.format(self))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if isinstance(parent, ACWidget):
            if parent.child != self:
                self._parent = parent
                self.parent.child = self

                self.fire(ACWidget.EVENT.PARENT_CHANGED)

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, child):
        if isinstance(child, ACWidget):
            self._child = child
            self.child.parent = self

            self.fire(ACWidget.EVENT.CHILD_CHANGED)

    @property
    def position(self) -> tuple:
        if self.has_id:
            position = ac.getPosition(self.id)
            if position != -1:
                return position
        return self._position

    @position.setter
    def position(self, position: tuple):
        self._position = position

        if self.has_id and len(position) == 2:
            ac.setPosition(self.id, position[0], position[1])

            self.fire(ACWidget.EVENT.POSITION_CHANGED)

    @property
    def size(self) -> tuple:
        if self.has_id:
            size = ac.getSize(self.id)
            if size != -1:
                return size
        return self._size

    @size.setter
    def size(self, size: tuple):
        self._size = size

        if self.has_id and len(size) == 2:
            ac.setSize(self.id, size[0], size[1])

            self.fire(ACWidget.EVENT.SIZE_CHANGED)

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible

        if self.has_id:
            ac.setVisible(self.id, visible)

    @property
    def background(self) -> bool:
        return self._background

    @background.setter
    def background(self, background: bool):
        self._background = background

        if self.has_id:
            ac.drawBackground(self.id, 1 if background else 0)

    @property
    def border(self) -> bool:
        return self._border

    @border.setter
    def border(self, border: bool):
        self._border = border

        if self.has_id:
            ac.drawBorder(self.id, 1 if border else 0)

    @property
    def background_texture(self) -> str:
        return self._background_texture

    @background_texture.setter
    def background_texture(self, background_texture: str):
        self._background_texture = background_texture

        self.background = True if self.background_texture else False

        if self.background_texture:
            if self.has_id:
                self.background = True
                if ac.setBackgroundTexture(self.id, background_texture) == -1:
                    console('{}: Texture "{}" could not be set.'.format(self, background_texture))

    @property
    def background_color(self) -> Color:
        return self._background_color

    @background_color.setter
    def background_color(self, background_color: Color):
        self._background_color = background_color

        if not self.background:
            self.background = background_color.a > 0 or self.background_texture

        if self.has_id:
            c = background_color
            success = ac.setBackgroundColor(self.id, c.r, c.g, c.b) == 1 and ac.setBackgroundOpacity(self.id, c.a) == 1
            if not success:
                console('{}: Background color could not be set.'.format(self))

    @property
    def border_color(self) -> Color:
        return self._border_color

    @border_color.setter
    def border_color(self, border_color: Color):
        self._border_color = border_color

        self.border = border_color.a > 0

    @property
    def animation(self):
        return self._active_animation

    @animation.setter
    def animation(self, animation):
        self._active_animation = animation

    def add_animation(self, animation: Animation):
        self._animation_queue.append(animation)

        self.fire(ACWidget.EVENT.ANIMATION_ADDED)

    def update_animation(self):
        if self._active_animation is None:
            if len(self._animation_queue) > 0:
                self._active_animation = self._animation_queue.pop(0)
                self._active_animation.init()
        else:
            if not self._active_animation.is_finished():
                self._active_animation.update()
            else:
                self._active_animation = None
                self.fire(ACWidget.EVENT.ANIMATION_FINISHED)

    def update(self, delta: int):
        self.update_animation()

        if self.child:
            self.child.update(delta)

    def render(self, delta: int):
        if self.border or self.background:
            x, y = self.position
            w, h = self.size

            if self.border:
                gl.rect(x, y, w, h, self.border_color, False)

        if self.child:
            self.child.render(delta)


class ACApp(ACWidget):
    """
    This class represents an application that holds a collection of controls and layouts.
    It is used for relative positioning of controls and is responsible for storing configurations.
    """
    def __init__(self, app_name: str, x: int, y: int, w: int, h: int):
        super().__init__()

        self._cfg = None
        self._title = ''
        self._active = False

        self._title_pos = (0, 0)
        self._icon_pos = (0, 0)
        self._icon = False

        self._activation_callback = None
        self._dismiss_callback = None
        self._render_callback = None

        self.id = ac.newApp(app_name)
        self.title = app_name
        self.position = (x, y)
        self.size = (w, h)

        self.render_callback = self.render

        self.on(ACWidget.EVENT.ACTIVATED, self._on_activate)
        self.on(ACWidget.EVENT.DISMISSED, self._on_dismiss)

        self._load_config()

        self.visible = self.active

    # Private

    def _on_id(self):
        super()._on_id()

        if self.has_id:
            if ac.addOnAppActivatedListener(self.id, ACWidget._event_function(ACWidget.EVENT.ACTIVATED, self)) == -1:
                console('Failed to add activation listener for {}.'.format(self.title))
            if ac.addOnAppDismissedListener(self.id, ACWidget._event_function(ACWidget.EVENT.DISMISSED, self)) == -1:
                console('Failed to add dismissed listener for {}.'.format(self.title))

    def _on_activate(self, widget: ACWidget, *args):
        self.active = True

    def _on_dismiss(self, widget: ACWidget, *args):
        self.active = False

    def _load_config(self):
        log('Load config for app "{}"'.format(self.title))
        self._cfg = WidgetConfig.load_app_config(self, self.title)

    def _write_config(self):
        log('Write config for app "{}"'.format(self.title))
        self._cfg.set('position', self.position, 'DEFAULT')
        self._cfg.set('active', self.active, 'DEFAULT')
        self._cfg.write()

    # Public

    @property
    def cfg(self):
        return self._cfg

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active: bool):
        self._active = active

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

        if self.has_id:
            ac.setTitle(self.id, title)

    @property
    def title_pos(self) -> tuple:
        return self._title_pos

    @title_pos.setter
    def title_pos(self, title_pos: tuple):
        self._title_pos = title_pos

        if self.has_id and len(title_pos) == 2:
            ac.setTitlePosition(self.id, title_pos[0], title_pos[1])

    @property
    def icon_pos(self) -> tuple:
        return self._icon_pos

    @icon_pos.setter
    def icon_pos(self, icon_pos: tuple):
        self._icon_pos = icon_pos

        if self.has_id and len(icon_pos) == 2:
            ac.setIconPosition(self.id, icon_pos[0], icon_pos[1])

    @property
    def render_callback(self):
        return self._render_callback

    @render_callback.setter
    def render_callback(self, render_callback: callable):
        self._render_callback = render_callback

        if self.has_id:
            ac.addRenderCallback(self.id, render_callback)

    def hide_decoration(self):
        self.title_pos = (-100000, -100000)
        self.icon_pos = (-100000, -100000)

    def update(self, delta: int):
        super().update(delta)

        # Required since an app movement will draw the default background again.
        self.background_color = self.background_color

    def render(self, delta: int):
        if self.border or self.background:
            w, h = self.size

            if self.border:
                gl.rect(0, 0, w, h, self.border_color, False)

        if self.child:
            self.child.render(delta)

    def shutdown(self):
        self._write_config()


class ACTextWidget(ACWidget, Observer):
    def __init__(self, parent: ACWidget, text: str = '', h_alignment: str = 'left', font: Font = None):
        super().__init__(parent)

        self._text = text
        self._font = font
        self._h_alignment = h_alignment

    def update_observer(self, subject):
        if isinstance(subject, Font):
            self.font = subject

    def _on_id(self):
        self.h_alignment = self.h_alignment
        self.font = self.font

        super()._on_id()

    def _on_size_changed(self):
        super()._on_size_changed()

        if self.font:
            ac.setFontSize(self.id, px2pt(self.size[1]) * 0.75)

    @property
    def text(self) -> str:
        if self.has_id:
            return ac.getText(self.id)
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

        if self.has_id:
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

            if self.has_id:
                ac.setFontSize(self.id, font.size)
                ac.setFontColor(self.id, font.color.r, font.color.g, font.color.b, font.color.a)
                ac.setCustomFont(self.id, font.name, font.italic, font.bold)

    @property
    def h_alignment(self):
        return self._h_alignment

    @h_alignment.setter
    def h_alignment(self, h_alignment: str):
        self._h_alignment = h_alignment

        if self.has_id:
            ac.setFontAlignment(self.id, self._h_alignment)


class ACLabel(ACTextWidget):
    def __init__(self, parent: ACWidget, text: str = '', h_alignment: str = 'left', font: Font = None):
        super().__init__(parent, text, h_alignment, font)

        self.id = ac.addLabel(self.app, text)


class ACVLabel(ACLabel):
    def __init__(self, parent: ACWidget, text: str = '', h_alignment: str = 'left', v_alignment: str = 'middle',
                 font: Font = None):
        super().__init__(parent, text, h_alignment, font)

        self._v_alignment = v_alignment
        self._v_offset = 0

    @property
    def size(self) -> tuple:
        if self.has_id:
            size = ac.getSize(self.id)
            if size != -1:
                return size
        return self._size

    @size.setter
    def size(self, size: tuple):
        self._size = size

        if self.has_id and len(size) == 2:
            ac.setSize(self.id, size[0], size[1] + self._v_offset)

            self.fire(ACWidget.EVENT.SIZE_CHANGED)

    @ACWidget.background.setter
    def background(self, background: bool):
        pass

    @ACWidget.border.setter
    def border(self, border: bool):
        pass

    @property
    def v_alignment(self):
        return self._v_alignment

    @v_alignment.setter
    def v_alignment(self, v_alignment: str):
        self._v_alignment = v_alignment

        self.position = self.position

        if v_alignment == 'top':
            pass
        elif v_alignment == 'middle':
            self._v_offset = (self.size[1] - pt2px(self.font.size)) / 2
        elif v_alignment == 'bottom':
            self._v_offset = (self.size[1] - pt2px(self.font.size))


class ACButton(ACTextWidget):
    def __init__(self, parent: ACWidget, text: str = '', h_alignment: str = 'left', font: Font = None):
        super().__init__(parent, text, h_alignment, font)

        self.id = ac.addButton(self.app, text)


class ACInput(ACTextWidget):
    def __init__(self, parent: ACWidget, text: str = '', h_alignment: str = 'left', font: Font = None):
        super().__init__(parent, text, h_alignment, font)

        self._focus = False
        self._validation_callback = None

        self.id = ac.addTextInput(self.app, text)
        self.text = text

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, focus: bool):
        if self.has_id:
            if ac.setFocus(self.id, 1 if focus else 0) != -1:
                self._focus = focus

    @property
    def validation_callback(self):
        return self._validation_callback

    @validation_callback.setter
    def validation_callback(self, validation_callback: callable):
        self._validation_callback = validation_callback

        if self.has_id:
            ac.addOnValidateListener(self.id, validation_callback)


# todo check if documentation is right that this does not work
class ACTextBox(ACTextWidget):
    def __init__(self, parent: ACWidget, text: str = ''):
        super().__init__(parent, text)

        self.id = ac.addTextBox(self.app, text)


class ACValueWidget(ACWidget):
    def __init__(self, parent: ACWidget, value: float = 0, _min: float = 0, _max: float = 0, points: int = -1):
        super().__init__(parent)

        self._value = value
        self._range = (_min, _max, points)

    def _on_id(self):
        super()._on_id()

        self.value = self.value
        self.range = self.range

    @property
    def value(self):
        if self.has_id:
            return ac.getValue(self.id)
        return self._value

    @value.setter
    def value(self, value: float):
        if self.range[0] <= value <= self.range[1]:
            self._value = value

            if self.has_id:
                ac.setValue(self.id, value)

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value_range: tuple):
        self._range = value_range
        if self.has_id:
            if self._range[2] > 0:
                ac.setRange(self.id, self._range[0], self._range[1], self._range[2])
            else:
                ac.setRange(self.id, self._range[0], self._range[1])


class ACCheckbox(ACValueWidget):
    def __init__(self, parent: ACWidget, value: float = 0):
        super().__init__(parent, value)

        self._checked_callback = None

        self.id = ac.addCheckBox(self.app, '')

    @property
    def checked_callback(self):
        return self._checked_callback

    @checked_callback.setter
    def checked_callback(self, checked_callback: callable):
        self._checked_callback = checked_callback

        if self.has_id:
            ac.addOnCheckBoxChanged(self.id, checked_callback)


class ACProgressBar(ACValueWidget):
    def __init__(self, parent: ACWidget, value: float = 0, start: float = 0, stop: float = 1):
        super().__init__(parent, value, start, stop)

        self.id = ac.addProgressBar(self.app, '')


class ACSpinner(ACValueWidget):
    def __init__(self, parent: ACWidget, start: float = 0, step: float = 0.1, stop: float = 1, value: float = 0):
        super().__init__(parent, value, start, stop)

        self._step = step
        self._value_change_callback = None

        self.id = ac.addSpinner(self.app, '')

        self.step = self.step

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step: float):
        self._step = step

        if self.has_id:
            ac.setStep(self.id, step)

    @property
    def value_change_callback(self):
        return self._value_change_callback

    @value_change_callback.setter
    def value_change_callback(self, value_callback: callable):
        self._value_change_callback = value_callback

        if self.has_id:
            ac.addOnValueChangeListener(self.id, value_callback)


class ACGraph(ACValueWidget):
    def __init__(self, parent: ACWidget, _min: float = 0, _max: float = 0, points: int = 0):
        super().__init__(parent, _min, _max, points)

        self.id = ac.addGraph(self.app, '')

    def add_series(self, color: Color):
        if self.has_id:
            ac.addSerieToGraph(self.id, color.r, color.g, color.b)

    def add_value(self, value: float, series: int):
        if self.has_id:
            ac.addValueToGraph(self.id, series, value)


class ACListBox(ACWidget):
    def __init__(self, parent: ACWidget):
        super().__init__(parent)

        self._multi_selection = False
        self._deselection = False
        self._items_per_page = 0

        self._selection_callback = None
        self._deselection_callback = None

        self.id = ac.addListBox(self.app, '')

        self.multi_selection = False
        self.items_per_page = 5

    @property
    def count(self):
        if self.has_id:
            return ac.getItemCount(self.id)
        return 0

    @property
    def multi_selection(self):
        return self._multi_selection

    @multi_selection.setter
    def multi_selection(self, multi_selection: bool):
        self._multi_selection = multi_selection

        if self.has_id:
            ac.setAllowMultiSelection(self.id, 1 if multi_selection else 0)

    @property
    def deselection(self):
        return self._deselection

    @deselection.setter
    def deselection(self, deselection: bool):
        self._deselection = deselection

        if self.has_id:
            ac.setAllowDeselection(self.id, 1 if deselection else 0)

    @property
    def items_per_page(self):
        return self._items_per_page

    @items_per_page.setter
    def items_per_page(self, items_per_page: int):
        self._items_per_page = items_per_page

        if self.id:
            ac.setItemNumberPerPage(self.id, items_per_page)

    @property
    def selection_callback(self):
        return self._selection_callback

    @selection_callback.setter
    def selection_callback(self, selection_callback: callable):
        self._selection_callback = selection_callback

        if self.has_id:
            ac.addOnListBoxSelectionListener(self.id, selection_callback)

    @property
    def deselection_callback(self):
        return self._deselection_callback

    @deselection_callback.setter
    def deselection_callback(self, deselection_callback: callable):
        self._deselection_callback = deselection_callback

        if self.has_id:
            ac.addOnListBoxDeselectionListener(self.id, deselection_callback)

    def add(self, name: str):
        if self.has_id:
            ac.addItem(self.id, name)

    def remove(self, name: str):
        if self.has_id:
            ac.addItem(self.id, name)

    def highlight(self, name: str):
        if self.has_id:
            ac.highlightListBoxItem(self.id, name)
