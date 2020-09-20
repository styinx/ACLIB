# Helps with the original signatures of ac functions

# Available functions in ac module:
# addButton
# addCheckBox 
# addGraph 
# addItem 
# addLabel 
# addListBox 
# addOnAppActivatedListener 
# addOnAppDismissedListener 
# addOnChatMessageListener 
# addOnCheckBoxChanged 
# addOnClickedListener 
# addOnListBoxDeselectionListener 
# addOnListBoxSelectionListener 
# addOnValidateListener 
# addOnValueChangeListener 
# addProgressBar 
# addRenderCallback 
# addSerieToGraph 
# addSpinner 
# addTextBox 
# addTextInput 
# addValueToGraph 
# console 
# drawBackground 
# drawBorder 
# ext_applyTrackConfig 
# ext_chaserCameraDebugText 
# ext_currentPpFilter 
# ext_debugFn 
# ext_debugLights 
# ext_debugWiperSoundState 
# ext_getAltitude 
# ext_getAmbientMult 
# ext_getAngleSpeed 
# ext_getBaseAltitude 
# ext_getCameraFov 
# ext_getCameraMatrix 
# ext_getCameraPos 
# ext_getCameraProj 
# ext_getCameraView 
# ext_getCarLightsMirrorVisible 
# ext_getCarLightsNum 
# ext_getCarLightsVisible 
# ext_getHeadlights 
# ext_getLightsMirrorVisible 
# ext_getLightsNum 
# ext_getLightsVisible 
# ext_getTrackLightsMirrorVisible 
# ext_getTrackLightsNum 
# ext_getTrackLightsVisible 
# ext_getTyreBlister 
# ext_getTyreFlatSpot 
# ext_getTyreGrain 
# ext_getTyreVirtualKM 
# ext_glSetTexture 
# ext_glTexCoord2f 
# ext_isG27Available 
# ext_isVaoPatchLoaded 
# ext_mirrorAspectRatioDown 
# ext_mirrorAspectRatioUp 
# ext_mirrorCurrent 
# ext_mirrorDebug 
# ext_mirrorDown 
# ext_mirrorFovDown 
# ext_mirrorFovUp 
# ext_mirrorLeft 
# ext_mirrorNext 
# ext_mirrorParams 
# ext_mirrorPrev 
# ext_mirrorRight 
# ext_mirrorToggleMon 
# ext_mirrorUp 
# ext_patchVersion 
# ext_patchVersionCode 
# ext_pauseFsWatching 
# ext_rainParams 
# ext_rainParamsAdjust 
# ext_rainParamsSet 
# ext_resetCar 
# ext_resumeFsWatching 
# ext_setCameraFov 
# ext_setClipboardData 
# ext_setDoorsOpen 
# ext_setDriverVisible 
# ext_setG27Thresholds 
# ext_setTrackConditionInput 
# ext_setVaoActive 
# ext_takeAStepBack 
# ext_vaoDisable 
# ext_vaoNormal 
# ext_vaoNormalDebug 
# ext_vaoOnly 
# ext_weatherDebugText 
# ext_weatherFxActive 
# ext_weatherTimeOffset 
# focusCar 
# freeCameraMoveForward 
# freeCameraMoveRight 
# freeCameraMoveUpWorld 
# freeCameraRotateHeading 
# freeCameraRotatePitch 
# freeCameraRotateRoll 
# freeCameraSetClearColor 
# getCameraCarCount 
# getCameraMode 
# getCarBallast 
# getCarEngineBrakeCount 
# getCarFFB 
# getCarLeaderboardPosition 
# getCarMinHeight 
# getCarName 
# getCarPowerControllerCount 
# getCarRealTimeLeaderboardPosition 
# getCarRestrictor 
# getCarSkin 
# getCarState 
# getCarTyreCompound 
# getCarsCount 
# getCurrentSplits 
# getDriverName 
# getDriverNationCode 
# getFocusedCar 
# getItemCount 
# getLastSplits 
# getPosition 
# getSelectedItems 
# getServerHttpPort 
# getServerIP 
# getServerName 
# getServerSlotsCount 
# getSize 
# getText 
# getTrackConfiguration 
# getTrackLength 
# getTrackName 
# getValue 
# getWindDirection 
# getWindSpeed 
# glBegin 
# glColor3f 
# glColor4f 
# glEnd 
# glQuad 
# glQuadTextured 
# glVertex2f 
# highlightListBoxItem 
# initFont 
# isAIControlled 
# isAcLive 
# isCameraOnBoard 
# isCarInPit 
# isCarInPitlane 
# isCarInPitline 
# isConnected 
# log 
# newApp 
# newTexture 
# removeItem 
# restart 
# sendChatMessage 
# setAllowDeselection 
# setAllowMultiSelection 
# setBackgroundColor 
# setBackgroundOpacity 
# setBackgroundTexture 
# setCameraCar 
# setCameraMode 
# setCarFFB 
# setCustomFont 
# setFocus 
# setFont 
# setFontAlignment 
# setFontColor 
# setFontSize 
# setIconPosition 
# setItemNumberPerPage 
# setPosition 
# setRange 
# setSize 
# setStep 
# setText 
# setTitle 
# setTitlePosition 
# setValue 
# setVisible 
# shutdown 


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
