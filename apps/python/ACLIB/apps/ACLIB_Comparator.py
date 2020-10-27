import ac
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from settings import path, TEXTURE_DIR
from ui.gui.ac_widget import ACApp, ACLabel, ACWidget, ACButton
from ui.gui.aclib_widget import ACLIBIcon
from ui.gui.font import Font
from ui.gui.layout import ACGrid, ACHBox, ACMultiWidget

from ui.color import Color, BLACK, PURPLE
from util.format import Format


class CR_Header(ACLabel):
    FONT = Font("Roboto Mono", Color(1.0, 1.0, 1.0), True)

    def __init__(self, parent: ACWidget, text: str):
        super().__init__(parent, text, 'center', CR_Header.FONT)


class CR_Name(ACLabel):
    FONT = Font("Roboto Mono", Color(1.0, 0.0, 0.0, 0.75), True)

    def __init__(self, parent: ACWidget, text: str):
        super().__init__(parent, text, 'center', CR_Name.FONT)


class CR_Label(ACLabel):
    BRIGHT = Font("Roboto Mono", Color(1.0, 1.0, 1.0))
    DARK = Font("Roboto Mono", Color(0.0, 0.0, 0.0))

    def __init__(self, parent: ACWidget, text: str):
        super().__init__(parent, text, 'center', CR_Label.BRIGHT)


class CR_Button(ACButton):
    FONT = Font("Roboto Mono", Color(0, 0, 0))

    def __init__(self, parent: ACWidget, text: str):
        super().__init__(parent, text, 'center', CR_Button.FONT)


class CR_Icon(ACLIBIcon):
    def __init__(self, parent: ACWidget, texture: str):
        super().__init__(parent, texture)


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
        super().__init__('ACLIB Comparator', 200, 200, 300, 55)

        self.no_render = True
        self.hide_decoration()
        self.background_color = Color(0.1, 0.1, 0.1, 0.5)

        self._data = data
        self._meta = meta

        self._mode = 0
        self._opponents = []

        self._grid = ACGrid(12, 11, self)
        self._header = CR_Header(self._grid, 'Lap Time')
        self._left = CR_Icon(self._grid, Comparator.TEXTURES['left'])
        self._right = CR_Icon(self._grid, Comparator.TEXTURES['right'])
        self._add = CR_Button(self._grid, 'Add Opponent')
        self._remove = CR_Button(self._grid, 'Remove Opponent')

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
        self._player = self._data.players[self._index]
        self._server = self._data.server
        self._sec_format = '{s:02d}.{ms:03d}'
        self._on_player_lap_changed_callback_id = None

        self._label = CR_Name(self, self._player.name)
        self._label.on(ACWidget.EVENT.CLICK, self._focus_player)
        self._multi = ACMultiWidget(self)

        self._laps = ACHBox(self)
        self._bst = CR_Label(self._laps, 'BST: --:--:---')
        self._lst = CR_Label(self._laps, 'LST: --:--:---')

        self._sector_box = ACHBox(self)
        self._sectors = []
        self._sectors.append(CR_Label(self._sector_box, 'S1: --:---'))
        self._sectors.append(CR_Label(self._sector_box, 'S2: --:---'))
        self._sectors.append(CR_Label(self._sector_box, 'S3: --:---'))

        self._left = CR_Icon(self, ComparatorRow.TEXTURES['left'])
        self._right = CR_Icon(self, ComparatorRow.TEXTURES['right'])

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

    def update_best_last_lap(self, lap: int):
        # todo add multiplayer events
        pass

    def update(self, delta: int):
        super().update(delta)

        # Update every 300 ms
        if (self.update_timer * 100) % 3 == 0:

            if self._mode == 1:
                player = self._player[self._index]

                for i in range(0, 3):
                    self._sectors[i].text = 'S{}: {}'.format(i + 1, Format.duration(player.sector_time(i),
                                                                                form=self._sec_format))

                    if i != player.sector_index and player.sector_time(i) > 0:
                        if player.sector_time(i) == player.gb_sector_time(i):
                            self._sectors[i].font = CR_Label.BRIGHT
                            self._sectors[i].background_color = ComparatorRow.COLORS['gb']
                        elif player.sector_time(i) == player.pb_sector_time(i):
                            self._sectors[i].font = CR_Label.DARK
                            self._sectors[i].background_color = ComparatorRow.COLORS['pb']
                        else:
                            self._sectors[i].font = CR_Label.DARK
                            self._sectors[i].background_color = ComparatorRow.COLORS['pw']
                    else:
                        self._sectors[i].font = CR_Label.BRIGHT
                        self._sectors[i].background_color = BLACK

        if self._update_timer > 0.1:
            self.reset_update_timer()

            if self._mode == 0:
                player = self._player[self._index]

                self._bst.text = 'BST: ' + Format.duration(player.best_lap)
                self._lst.text = 'LST: ' + Format.duration(player.last_lap)

                if player.last_lap > 0 and player.last_lap == player.gb_lap_time:
                    self._lst.font = CR_Label.BRIGHT
                    self._lst.background_color = ComparatorRow.COLORS['gb']
                elif player.last_lap == player.pb_lap_time:
                    self._lst.font = CR_Label.DARK
                    self._lst.background_color = ComparatorRow.COLORS['pb']
                else:
                    self._lst.font = CR_Label.BRIGHT
                    self._lst.background_color = BLACK

                if player.best_lap > 0 and player.best_lap == player.gb_lap_time:
                    self._bst.font = CR_Label.BRIGHT
                    self._bst.background_color = ComparatorRow.COLORS['gb']
                elif player.best_lap == player.pb_lap_time:
                    self._bst.font = CR_Label.DARK
                    self._bst.background_color = ComparatorRow.COLORS['pb']
                else:
                    self._bst.font = CR_Label.BRIGHT
                    self._bst.background_color = BLACK
