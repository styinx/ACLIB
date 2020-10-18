from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.color import RED, TRANSPARENT, BLACK, WHITE, YELLOW
from ui.gui.font import Font
from ui.gui.layout import ACGrid
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget

from util.log import console


class Debug(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Debug', 200, 200, 400, 100)

        self.hide_decoration()
        self.background_color = BLACK

        self._data = data
        self._widget = None
        self._widget_bg = None
        self._chain = []

        self._font = Font('Roboto Mono')
        self._font.color = WHITE

        self._grid = ACGrid(4, 4, self)

        self._widget_label = ACLabel(self._grid, 'Widget:', font=self._font)
        self._widget_text = ACLabel(self._grid, '', font=self._font)

        self._position_label = ACLabel(self._grid, 'Position:', font=self._font)
        self._position_text = ACLabel(self._grid, '', font=self._font)

        self._size_label = ACLabel(self._grid, 'Size:', font=self._font)
        self._size_text = ACLabel(self._grid, '', font=self._font)

        self._chain_label = ACLabel(self._grid, 'Chain:', font=self._font)
        self._chain_text = ACLabel(self._grid, '', font=self._font)

        self._grid.add(self._widget_label, 0, 0)
        self._grid.add(self._widget_text, 1, 0)
        self._grid.add(self._position_label, 0, 1)
        self._grid.add(self._position_text, 1, 1)
        self._grid.add(self._size_label, 0, 2)
        self._grid.add(self._size_text, 1, 2)
        self._grid.add(self._chain_label, 0, 3)
        self._grid.add(self._chain_text, 1, 3)

        self._data.on(ACData.EVENT.READY, self.init)
        self.on(ACWidget.EVENT.DISMISSED, self.dismissed)

    def init(self):
        for _id, widget in ACWidget.IDS.items():
            widget.on(ACWidget.EVENT.CLICK, self.get_info)

    def get_info(self, widget: ACWidget, *args):
        if self.active:
            if self._widget and self._widget == widget:
                self._widget.border_color = self._widget_bg

            elif self._widget and widget == self._widget.parent:
                self._chain.append(widget)
                widget.border_color = YELLOW
                self._chain_text.text = self._chain_text.text + str(widget) + ' -> '

            else:
                self._chain_text = ''
                for w in self._chain:
                    w.border_color = TRANSPARENT
                self._chain = []

                if self._widget:
                    self._widget.border_color = self._widget_bg
                self._widget = widget
                self._widget_bg = self._widget.border_color
                self._widget.border_color = RED

                self._widget_text.text = str(self._widget)
                self._position_text.text = str(self._widget.position)
                self._size_text.text = str(self._widget.size)

            console(widget, 'clicked')

    def dismissed(self, widget: ACWidget, *args):
        if self._widget:
            self._widget.border_color = self._widget_bg
