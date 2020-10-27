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
    PROPERTIES = [
        # Name in ListBox, Number of values, ac_data category, format
        ['ABS', 1, 'car.abs', '{:1d}'],
        ['Brake Bias', 1, 'tyres.brake_bias', '{:1.2f}'],
        ['Brake Temp', 4, 'tyres.brake_temperature', '{:3.2f}°C'],
        ['Camber', 4, 'tyres.camber', '{:3.2f}'],
        ['Compound', 1, 'tyres.compound', '{:s}'],
        ['Compound Name', 1, 'tyres.compound_name', '{:s}'],
        ['Compound Symbol', 1, 'tyres.compound_symbol', '{:s}'],
        ['Fuel', 1, 'car.fuel', '{:3.2f} l'],
        ['Road Grip', 1, 'environment.surface_grip', '{:3.2f}'],
        ['Road Temp', 1, 'environment.road_temperature', '{:3.2f}'],
        ['Suspension Travel', 4, 'tyres.suspension_travel', '{:3.2f}'],
        ['TC', 1, 'car.tc', '{:1d}'],
        ['Tyre Load', 4, 'tyres.load', '{:3.2f}'],
        ['Tyre Slip', 4, 'tyres.slip', '{:3.2f}'],
        ['Tyre Pressure', 4, 'tyres.pressure', '{:3.2f} psi'],
        ['Tyre Temp inner', 4, 'tyres.inner_temperature', '{:3.2f}°C'],
        ['Tyre Temp center', 4, 'tyres.center_temperature', '{:3.2f}°C'],
        ['Tyre Temp core', 4, 'tyres.core_temperature', '{:3.2f}°C'],
        ['Tyre Temp outer', 4, 'tyres.outer_temperature', '{:3.2f}°C'],
        ['Tyre Wear', 4, 'tyres.wear', '{:3.2f}%'],
        ['', 0, '', ''],
        ['', 0, '', ''],
    ]

    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB Car Properties', 200, 200, 300, 66)

        self.hide_decoration()
        self.background_color = Color(0, 0, 0, 0.5)
        self.no_render = True

        self._data = data
        self._timer = 0

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

        # ACDATA events
        self._data.on(ACData.EVENT.READY, self._on_ready)

    def _on_ready(self):
        self._properties.on(ACWidget.EVENT.INDEX_CHANGED, self._on_index_changed)
        self._properties.index = self.cfg.get('index') or 0

    def _on_index_changed(self, index: int):
        prop = CarProperties.PROPERTIES[index]

        # Hide non active layouts
        self._single.visible = False
        self._dual.visible = False
        self._triple.visible = False
        self._quad.visible = False

        # Select the fitting layout
        element = self._value_content.children[prop[1] - 1]
        element.visible = True

        # Fill property values
        if prop[1] == 1:
            element.children[0].text = prop[3].format(get_property(self._data, prop[2]))
        else:
            for i, value in enumerate(get_property(self._data, prop[2])):
                element.children[i].text = prop[3].format(value)

    def update(self, delta: int):
        super().update(delta)

        # Update every 5 seconds
        if self.update_timer > 0.5:
            self.reset_update_timer()
            self._on_index_changed(self._properties.index)

    def shutdown(self):
        self.cfg.set('index', self._properties.index)

        super().shutdown()
