from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.color import *
from ui.gui.aclib_widget import ACLIBListBox
from ui.gui.layout import *
from ui.gui.ac_widget import *

# Get properties from string
def get_property(obj, prop: str):
    if prop.find('.') > -1:
        objects = prop.split('.')
        return get_property(getattr(obj, objects[0]), '.'.join(objects[1:]))
    elif prop:
        return getattr(obj, prop)
    else:
        return obj


class CPValue(ACVLabel):
    FONT = Font('Roboto Mono', WHITE, size=12)

    def __init__(self, parent: ACWidget):
        super().__init__(parent, '', 'center', 'middle', CPValue.FONT)


class CarProperties(ACApp):
    class Priority:
        NONE = -1
        LOW = 10.0      # 10s
        MEDIUM = 1.0    # 1s
        HIGH = 0.5      # 500ms
        HIGHER = 0.3    # 300ms
        HIGHEST = 0.1   # 100ms

    PROPERTIES = [
        # Name in ListBox, Number of values, ac_data category, format, update interval (s), modifier
        ['ABS', 1, 'car.abs', '{:1.0f}', Priority.HIGH, None],
        ['Brake Bias', 1, 'tyres.brake_bias', '{:3.0f}', Priority.HIGH, lambda x : x * 100],
        ['Brake Temp', 4, 'tyres.brake_temperature', '{:3.2f}°C', Priority.HIGH, None],
        ['Camber', 4, 'tyres.camber', '{:3.2f}', Priority.HIGH, None],
        ['Compound', 1, 'tyres.compound', '{:s}', Priority.MEDIUM, None],
        ['Compound Name', 1, 'tyres.compound_name', '{:s}', Priority.MEDIUM, None],
        ['Compound Symbol', 1, 'tyres.compound_symbol', '{:s}', Priority.MEDIUM, None],
        ['Fuel', 1, 'car.fuel', '{:3.2f} l', Priority.HIGHER, None],
        ['Road Grip', 1, 'environment.surface_grip', '{:3.0f}', Priority.NONE, lambda x : x * 100],
        ['Road Temp', 1, 'environment.road_temperature', '{:3.2f}°C', Priority.NONE, None],
        ['Suspension Travel', 4, 'tyres.suspension_travel', '{:3.2f}', Priority.MEDIUM, None],
        ['TC', 1, 'car.tc', '{:1.0f}', Priority.HIGH, None],
        ['Tyre Load', 4, 'tyres.load', '{:3.2f}', Priority.HIGHER, None],
        ['Tyre Slip', 4, 'tyres.slip', '{:3.2f}', Priority.HIGHER, None],
        ['Tyre Pressure', 4, 'tyres.pressure', '{:3.2f} psi', Priority.HIGHEST, None],
        ['Tyre Temp inner', 4, 'tyres.inner_temperature', '{:3.2f}°C', Priority.HIGHEST, None],
        ['Tyre Temp center', 4, 'tyres.center_temperature', '{:3.2f}°C', Priority.HIGHEST, None],
        ['Tyre Temp core', 4, 'tyres.core_temperature', '{:3.2f}°C', Priority.HIGHEST, None],
        ['Tyre Temp outer', 4, 'tyres.outer_temperature', '{:3.2f}°C', Priority.HIGHEST, None],
        ['Tyre Wear', 4, 'tyres.wear', '{:3.2f}%', Priority.HIGHEST, None],
        ['', 0, '', '', Priority.NONE, None],
        ['', 0, '', '', Priority.NONE, None],
    ]

    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB Car Properties', 200, 200, 300, 66, True)

        self.hide_decoration()
        self.background_color = Color(0, 0, 0, 0.5)

        self._data = data

        self._main_layout = ACHBox(self)
        self._properties = ACLIBListBox(self._main_layout, 3)
        self._value_content = ACMultiWidget(self._main_layout)

        self._main_layout.add(self._properties)
        self._main_layout.add(self._value_content)

        # Layout that stores 1 value
        self._single = ACVBox(self._value_content)
        self._single.add(CPValue(self._single))
        self._single.visible = False

        # Layout that stores 2 values
        self._dual = ACVBox(self._value_content)
        self._dual.add(CPValue(self._dual))
        self._dual.add(CPValue(self._dual))
        self._dual.visible = False

        # Layout that stores 3 values
        self._triple = ACVBox(self._value_content)
        self._triple.add(CPValue(self._dual))
        self._triple.add(CPValue(self._dual))
        self._triple.add(CPValue(self._dual))
        self._triple.visible = False

        # Layout that stores 4 values
        self._quad = ACGrid(2, 2, self._value_content)
        self._quad.add(CPValue(self._quad), 0, 0)
        self._quad.add(CPValue(self._quad), 1, 0)
        self._quad.add(CPValue(self._quad), 0, 1)
        self._quad.add(CPValue(self._quad), 1, 1)
        self._quad.visible = False

        # Store all properties in the listbox
        for el in CarProperties.PROPERTIES:
            self._properties.add(ACLabel(self._properties, el[0], font=CPValue.FONT))

        # Store the layouts in the same position
        self._value_content.add(self._single)
        self._value_content.add(self._dual)
        self._value_content.add(self._triple)
        self._value_content.add(self._quad)

        # Set initial values
        self._selected = CarProperties.PROPERTIES[0]
        self._active_layout = self._value_content.children[self._selected[1] - 1]

        # ACDATA events
        self._data.on(ACData.EVENT.READY, self._on_ready)

    def _on_ready(self):
        self._properties.on(ACWidget.EVENT.INDEX_CHANGED, self._on_index_changed)
        self._properties.index = self.cfg.get('index') or 0

    def _update_property_value(self):
        values = get_property(self._data, self._selected[2])
        if self._selected[1] == 1:
            values = [get_property(self._data, self._selected[2])]

        for i, value in enumerate(values):
            # Modifier?
            if self._selected[5]:
                value = self._selected[5](value)
            self._active_layout.children[i].text = self._selected[3].format(value)

    def _on_index_changed(self, index: int):
        self._selected = CarProperties.PROPERTIES[index]
        prop = self._selected

        # Hide non active layouts
        self._single.visible = False
        self._dual.visible = False
        self._triple.visible = False
        self._quad.visible = False

        # Select the fitting layout
        self._active_layout = self._value_content.children[prop[1] - 1]
        self._active_layout.visible = True

        self._update_property_value()

    def update(self, delta: float):
        super().update(delta)

        # Update based on properties priority.
        if self._selected[4] != -1:
            if self.update_timer > self._selected[4]:
                self.reset_update_timer()
                self._update_property_value()

    def shutdown(self):
        self.cfg.set('index', self._properties.index)

        super().shutdown()
