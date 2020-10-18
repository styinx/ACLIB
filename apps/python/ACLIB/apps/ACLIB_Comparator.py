import ac
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from settings import path, TEXTURE_DIR
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget, ACButton
from ui.gui.aclib_widget import ACLIBIcon
from ui.gui.font import Font
from ui.gui.layout import ACGrid, ACHBox, ACMultiWidget

from ui.color import Color, LIGHTGRAY, RED, WHITE, BLACK, PURPLE
from util.format import Format


class Comparator(ACApp):
    TEXTURES = {
        'left':  path(TEXTURE_DIR, 'arrow-left-slim.png'),
        'right': path(TEXTURE_DIR, 'arrow-right-slim.png')
    }

    MODE = [
        'Lap Time',
        'Sector Time'
    ]

    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Comparator', 200, 200, 300, 55)

        self.hide_decoration()
        self.background_color = Color(0.1, 0.1, 0.1, 0.5)

        self._data = data
        self._meta = meta

        self._mode = 0
        self._opponents = []

        self._big_font = Font('Roboto Mono')
        self._big_font.color = WHITE
        self._big_font.bold = True
        self._small_font = Font('Roboto Mono')
        self._small_font.color = BLACK

        self._grid = ACGrid(12, 11, self)
        self._header = ACLabel(self._grid, 'Lap Time', 'center', self._big_font)
        self._header.background_color = RED
        self._left = ACLIBIcon(self._grid, Comparator.TEXTURES['left'])
        self._left.background_color = LIGHTGRAY
        self._right = ACLIBIcon(self._grid, Comparator.TEXTURES['right'])
        self._right.background_color = LIGHTGRAY

        self._add = ACButton(self._grid, 'Add Opponent', 'center', self._small_font)
        self._add.background_color = LIGHTGRAY
        self._remove = ACLabel(self._grid, 'Remove Opponent', 'center', self._small_font)
        self._remove.background_color = LIGHTGRAY

        self._grid.add(self._left, 0, 0, 1, 6)
        self._grid.add(self._header, 1, 0, 10, 6)
        self._grid.add(self._right, 11, 0, 1, 6)
        self._grid.add(self._add, 0, 6, 6, 5)
        self._grid.add(self._remove, 6, 6, 6, 5)

        self._left.on(ACWidget.EVENT.CLICK, self._on_left)
        self._right.on(ACWidget.EVENT.CLICK, self._on_right)
        #self._add.on(ACWidget.EVENT.CLICK, self._on_add)
        #self._remove.on(ACWidget.EVENT.CLICK, self._on_remove)

        self._add_opponent(0)
        self._add_opponent(1)

    def _add_opponent(self, i):
        w, h = self.size

        opponent = ComparatorRow(self._grid, self._data, self._meta)
        opponent.position = 0, h + i * 50
        opponent.size = w, 50
        self._opponents.append(opponent)

        # self._grid.add_rows(2)
        # w, h = self.size
        # self.size = w, h + 40
        # self._grid.add(opponent, 0, 4 + len(self._opponents) * 2, 12, 2)

    def _on_mode_changed(self):
        for opponent in self._opponents:
            opponent.change_mode(self._mode)

    def _on_left(self, *args):
        if self._mode > 0:
            self._mode -= 1
        else:
            self._mode = len(Comparator.MODE) - 1
        self._header.text = Comparator.MODE[self._mode]

        self._on_mode_changed()

    def _on_right(self, *args):
        if self._mode < len(Comparator.MODE) - 1:
            self._mode += 1
        else:
            self._mode = 0
        self._header.text = Comparator.MODE[self._mode]

        self._on_mode_changed()

    def _on_add(self, *args):
        self._grid.add_rows(2)
        w, h = self.size
        self.size = w, h + 40

    def _on_remove(self, *args):
        if len(self._opponents) > 0:
            self._grid.remove_rows(2)
            w, h = self.size
            self.size = w, h - 40

    def update(self, delta: int):
        super().update(delta)

        for o in self._opponents:
            o.update(delta)


class ComparatorRow(ACGrid):
    TEXTURES = {
        'left': path(TEXTURE_DIR, 'arrow-left-slim.png'),
        'right': path(TEXTURE_DIR, 'arrow-right-slim.png')
    }
    COLORS = {
        'gb': PURPLE,
        'pb': Color(0.0, 0.75, 0, 1.0),
        'pw': Color(0.7, 0.7, 0, 1.0)
    }

    def __init__(self, parent: ACWidget, data: ACData, meta: ACMeta):
        super().__init__(12, 2, parent)

        self.background_color = Color(0, 0, 0, 0.5)

        self._data = data
        self._meta = meta

        self._mode = 0
        self._index = 0
        self._timer = 0
        self._player = self._data.players[self._index]
        self._server = self._data.server
        self._sec_format = '{s:02d}.{ms:03d}'

        self._header_font = Font("Roboto Mono")
        self._header_font.color = Color(0.9, 0.2, 0.2)
        self._header_font.bold = True

        self._bright_font = Font("Roboto Mono")
        self._bright_font.color = WHITE
        self._dark_font = Font("Roboto Mono")
        self._dark_font.color = BLACK

        self._label = ACLabel(self, self._player.name, 'center', self._header_font)
        self._label.background_color = BLACK
        self._label.on(ACWidget.EVENT.CLICK, self._focus_player)
        self._multi = ACMultiWidget(self)

        self._laps = ACHBox(self)
        self._bst = ACLabel(self._laps, 'BST: --:--:---', 'center', self._bright_font)
        self._lst = ACLabel(self._laps, 'LST: --:--:---', 'center', self._bright_font)

        self._sector_box = ACHBox(self)
        self._sectors = []
        self._sectors.append(ACLabel(self._sector_box, 'S1: --:---', 'center', self._bright_font))
        self._sectors.append(ACLabel(self._sector_box, 'S2: --:---', 'center', self._bright_font))
        self._sectors.append(ACLabel(self._sector_box, 'S3: --:---', 'center', self._bright_font))

        self._left = ACLIBIcon(self, ComparatorRow.TEXTURES['left'])
        self._left.background_color = LIGHTGRAY
        self._right = ACLIBIcon(self, ComparatorRow.TEXTURES['right'])
        self._right.background_color = LIGHTGRAY

        self._laps.add(self._bst)
        self._laps.add(self._lst)

        self._sector_box.add(self._sectors[0])
        self._sector_box.add(self._sectors[1])
        self._sector_box.add(self._sectors[2])

        self._multi.add(self._laps)
        self._multi.add(self._sector_box)

        self.add(self._left, 0, 0)
        self.add(self._label, 1, 0, 10, 1)
        self.add(self._right, 11, 0)
        self.add(self._multi, 0, 1, 12, 1)

        self.change_mode(self._mode)

        self._left.on(ACWidget.EVENT.CLICK, self._on_left)
        self._right.on(ACWidget.EVENT.CLICK, self._on_right)

    def _focus_player(self, *args):
        ac.focusCar(self._index)

    def _update_index(self):
        self._player = self._data.players[self._index]
        self._label.text = self._player.name

    def _on_left(self, *args):
        if self._index > 0:
            self._index -= 1
        else:
            self._index = self._server.cars - 1

        self._update_index()

    def _on_right(self, *args):
        if self._index < self._server.cars - 1:
            self._index += 1
        else:
            self._index = 0

        self._update_index()

    def change_mode(self, mode: int):
        self._mode = mode

        if self._mode == 0:
            self._laps.visible = True
            self._sector_box.visible = False
        elif self._mode == 1:
            self._laps.visible = False
            self._sector_box.visible = True

    def update(self, delta: int):
        super().update(delta)

        self._timer += delta

        # Update every 100 ms
        if self._timer > 0.1:
            self._timer = 0

            player = self._player[self._index]

            if self._mode == 0:
                self._bst.text = 'BST: ' + Format.duration(player.best_lap)
                self._lst.text = 'LST: ' + Format.duration(player.last_lap)

                if player.last_lap > 0 and player.last_lap == player.gb_lap_time:
                    self._lst.font = self._bright_font
                    self._lst.background_color = ComparatorRow.COLORS['gb']
                elif player.last_lap == player.pb_lap_time:
                    self._lst.font = self._dark_font
                    self._lst.background_color = ComparatorRow.COLORS['pb']
                else:
                    self._lst.font = self._bright_font
                    self._lst.background_color = BLACK

                if player.best_lap > 0 and player.best_lap == player.gb_lap_time:
                    self._bst.font = self._bright_font
                    self._bst.background_color = ComparatorRow.COLORS['gb']
                elif player.best_lap == player.pb_lap_time:
                    self._bst.font = self._dark_font
                    self._bst.background_color = ComparatorRow.COLORS['pb']
                else:
                    self._bst.font = self._bright_font
                    self._bst.background_color = BLACK

            elif self._mode == 1:
                for i in range(0, 3):
                    self._sectors[i].text = 'S{}: {}'.format(i + 1, Format.duration(player.sector_time(i),
                                                                                form=self._sec_format))

                    if i != player.sector_index and player.sector_time(i) > 0:
                        if player.sector_time(i) == player.gb_sector_time(i):
                            self._sectors[i].font = self._bright_font
                            self._sectors[i].background_color = ComparatorRow.COLORS['gb']
                        elif player.sector_time(i) == player.pb_sector_time(i):
                            self._sectors[i].font = self._dark_font
                            self._sectors[i].background_color = ComparatorRow.COLORS['pb']
                        else:
                            self._sectors[i].font = self._dark_font
                            self._sectors[i].background_color = ComparatorRow.COLORS['pw']
                    else:
                        self._sectors[i].font = self._bright_font
                        self._sectors[i].background_color = BLACK

