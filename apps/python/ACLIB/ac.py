# Car Management


def getCarState(car: str, what: int) -> int:
    pass


def getDriverName(car: int) -> str:
    pass


def getTrackName(car: int) -> str:
    pass


def getTrackConfiguration(car: int) -> str:
    pass


def getCarName(car: int) -> str:
    pass


def getLastSplits(car: int) -> [float]:
    pass


def isCarInPitlane(car: int) -> int:
    pass


def isCarInPitline(car: int) -> int:
    pass


def isCarInPit(car: int) -> int:
    pass


def isCarConnected(car: int) -> int:
    pass


def getCarBallast(car: int) -> int:
    pass


def getCarMinHeigt(car: int) -> int:
    pass


def getServerName() -> str:
    pass


def getServerIP() -> str:
    pass


def getServerHttpPort() -> str:
    pass


def getCarsCount() -> int:
    pass


def getCarLeaderboardPosition(car: int) -> int:
    pass


def getCarRealTimeLeaderboardPosition(car: int) -> int:
    pass


def getCarFFB() -> int:
    pass


def setFFB(value: int):
    pass


# Camera


def setCameraMode(mode: str):
    pass


def getCameraMode() -> str:
    pass


def setCameraCar(camera: int, car: int) -> int:
    pass


def getCameraCarCount(car: int) -> int:
    pass


def focusCar(car: int) -> int:
    pass


def getFocusedCar() -> int:
    pass


# Debug


def console(text: str) -> int:
    pass


def log(text: str) -> int:
    pass


# General App Management


def newApp(name: str) -> int:
    pass


def setTitle(_id: int, title: str) -> int:
    pass


def setSize(_id: int, w: float, h: float) -> int:
    pass


def addLabel(_id: int, text: str) -> int:
    pass


def setPosition(_id: int, x: float, y: float) -> int:
    pass


def setIconPosition(_id: int, x: float, y: float) -> int:
    pass


def setTitlePosition(_id: int, x: float, y: float) -> int:
    pass


def getPosition(_id: int) -> tuple:
    pass


def setText(_id: int, text: str) -> int:
    pass


def getText(_id: int) -> str:
    pass


def setBackgroundOpacity(_id: int, a: float) -> int:
    pass


def drawBackground(_id: int, border: int) -> int:
    pass


def drawBorder(_id: int, border: int) -> int:
    pass


def setBackgroundTexture(_id: int, tex_path: str) -> int:
    pass


def setFontAlignment(_id: int, alignment: str) -> int:
    pass


def setBackgroundColor(_id: int, r: float, g: float, b: float) -> int:
    pass


def setVisible(_id: int, visible: int) -> int:
    pass


def addOnAppActivatedListener(_id: int, callback: callable) -> int:
    pass


def addOnAppDismissedListener(_id: int, callback: callable) -> int:
    pass


def addRenderCallback(_id: int, callback: callable) -> int:
    pass


def setFontColor(_id: int, r: float, g: float, b: float, a: float) -> int:
    pass


def setFontSize(_id: int, size: int) -> int:
    pass


def initFont(dummy: int, name: str, italic: int, bold: int) -> int:
    pass


def setCustomFont(_id: int, name: str, italic: int, bold: int) -> int:
    pass


# Specific Control Management


def addButton(_id: int, text: str) -> int:
    pass


def addOnClickedListener(_id: int, callback: callable) -> int:
    pass


def addGraph(_id: int, value: int) -> int:
    pass


def addSerieToGraph(_id: int, r: float, g: float, b: float) -> int:
    pass


def addValueToGraph(_id: int, series: int, value: int) -> int:
    pass


def setRange(_id: int, _min: int, _max: int, _max_points) -> int:
    pass


def addSpinner(_id: int, value: int) -> int:
    pass


def setRange(_id: int, _min: int, _max: int) -> int:
    pass


def setValue(_id: int, value: int) -> int:
    pass


def setSetp(_id: int, value: int) -> int:
    pass


def addOnValueChangeListener(_id: int, callback: callable) -> int:
    pass


def addProgressBar(_id: int, text: str) -> int:
    pass


def addInputText(_id: int, text: str) -> int:
    pass


def setFocus(_id: int, focus: int) -> int:
    pass


def addOnValidateListener(_id: int, callback: callable) -> int:
    pass


def addListBox(_id: int, name: str) -> int:
    pass


def addItem(_id: int, name: str) -> int:
    pass


def removeItem(_id: int, item: int) -> int:
    pass


def getItemCount(_id: int) -> int:
    pass


def setItemNumberPerPage(_id: int, number: int) -> int:
    pass


def highlightListBoxItem(_id: int, item: int) -> int:
    pass


def addOnListBoxSelectionListener(_id: int, callback: callable) -> int:
    pass


def addOnListBoxDeselectionListener(_id: int, callback: callable) -> int:
    pass


def setAllowDeselection(_id: int, allow: int) -> int:
    pass


def setAllowMultiSelection(_id: int, allow: int) -> int:
    pass


def getSelectedItems(_id: int) -> int:
    pass


def addCheckBox(_id: int, name: str) -> int:
    pass


def addOnCheckBoxChanged(_id: int, callback: callable) -> int:
    pass


def addTextBox(_id: int, name: str) -> int:
    pass


# Graphics and Rendering

def newTexture(tex_path: str) -> int:
    pass


def glBegin(what: int) -> int:
    pass


def glEnd() -> int:
    pass


def glVertex2f(x: float, y: float) -> int:
    pass


def glColor3f(r: float, g: float, b: float) -> int:
    pass


def glColor4f(r: float, g: float, b: float, a: float) -> int:
    pass


def glQuad(x: float, y: float, w: float, h: float) -> int:
    pass


def glQuadTextured(r: float, g: float, b: float, a: float, tex_id: int) -> int:
    pass
