from time import sleep

from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.color import RED, TRANSPARENT, DARKGRAY, BLACK, WHITE, YELLOW, LIGHTGRAY
from ui.gui.font import Font
from ui.gui.layout import ACGrid
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget, ACTextWidget, ACInput, ACButton
from util.format import Format

from util.log import console


class Console(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Console', 200, 200, 400, 200)

        self.hide_decoration()
        self.background_color = BLACK

        self._data = data

        self._font = Font('Roboto Mono')
        self._font.color = WHITE

        self._grid = ACGrid(4, 10, self)
        self._input = ACInput(self._grid)
        self._button = ACButton(self._grid, 'Execute', 'center')
        self._text = ACLabel(self._grid)

        self._grid.add(self._input, 0, 0, 3, 1)
        self._grid.add(self._button, 3, 0)
        self._grid.add(self._text, 0, 1, 4, 9)

        self._button.background_color = LIGHTGRAY
        self._data.on(ACData.EVENT.READY, self.on_ready)
        self._button.on(ACWidget.EVENT.CLICK, self.on_ok)

    def on_ready(self):
        exec('from ui.gui.ac_widget import ACWidget')

    def on_ok(self, widget: ACWidget, *args):
        try:
            text = self._input.text
            console(eval('ACWidget.get_control(1)'))

            if text.startswith('ev:'):
                self._text.text = str(eval(text[text.find('ev:') + 3:]))
                self._input.text = ""
            elif text.startswith('ex:'):
                exec(text[text.find('ex:') + 3:])
                self._input.text = ""
            else:
                self._text.text = 'Expression must start with "ev:" or "ex:"!'

        except Exception as e:
            self._text.text = '{}: Expression "{}" not recognized!'.format(Format.time(), self._input.text)
