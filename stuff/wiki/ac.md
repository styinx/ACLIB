## AC Python Functions

### General

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| console | | |
| isAcLive | | Returns if the simulation is running or nor. |
| log | msg: str | Logs a message to the default log file. |
| restart | | |
| shutdown | | |

### Control Creation

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| addButton | id: int <br> text: str | Creates a button and returns it's id. |
| addCheckBox | | |
| addGraph | | |
| addLabel | | |
| addListBox | | |
| addProgressBar | | |
| addSpinner | | |
| addTextBox | | |
| addTextInput | | |
| initFont | | |
| newApp | | |

### Control Modification

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| addItem | | |
| addSerieToGraph | | |
| addValueToGraph | | |
| drawBackground | | |
| drawBorder | | |
| getItemCount | | |
| getPosition | | |
| getSelectedItems | | |
| getSize | | |
| getText | | |
| getValue | | |
| highlightListBoxItem | | |
| removeItem | | |
| setAllowDeselection | | |
| setAllowMultiSelection | | |
| setBackgroundColor | | |
| setBackgroundOpacity | | |
| setBackgroundTexture | | |
| setCustomFont | | |
| setFocus | | |
| setFont | | |
| setFontAlignment | | |
| setFontColor | | |
| setFontSize | | |
| setIconPosition | | |
| setItemNumberPerPage | | |
| setPosition | | |
| setRange | | |
| setSize | | |
| setStep | | |
| setText | | |
| setTitle | | |
| setTitlePosition | | |
| setValue | | |
| setVisible | | |

### Rendering

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| glBegin | | |
| glColor3f | | |
| glColor4f | | |
| glEnd | | |
| glQuad | | |
| glQuadTextured | | |
| glVertex2f | | |
| newTexture | | |

### Control EventListeners and Callbacks

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| addOnAppActivatedListener | | |
| addOnAppDismissedListener | | |
| addOnChatMessageListener | a <br> b | |
| addOnCheckBoxChanged | | |
| addOnClickListener | | |
| addOnListBoxDeselectionListener | | |
| addOnListBoxSelectionListener | | |
| addOnValidateListener | | |
| addOnValueChangeListener | | |
| addRenderCallback | | |

### Camera

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| focusCar  | | |
| freeCameraMoveForward | a <br> b <br> args | |
| freeCameraMoveRight | | |
| freeCameraMoveUpWorld | | |
| freeCameraRotateHeading | | |
| freeCameraRotatePitch | a <br> b <br> c <br> d | |
| freeCameraRotateRoll | | |
| freeCameraSetClearColor | | |
| getCameraCarCount | | |
| getCameraMode | | |
| getFocusedCar | | |
| isCameraOnboard | | |
| setCameraCar | | |
| setCameraMode | | |

### Car Functions

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| getCarBallast | | |
| getCarEngineBrakeCount | | |
| getCarFFB | | |
| getCarLeaderboardPosition | | |
| getCarMinHeight | | |
| getCarName | | |
| getCarPowerControllerCount | | |
| getCarRealTimeLeaderboardPosition | | |
| getCarRestrictor | a <br> b | |
| getCarSkin | | |
| getCarState | | |
| getCarTyreCompound | | |
| getCarTyreCompound | | |
| isAIControlled | | |
| isCarInPit | | |
| isCarInPitlane | | |
| isCarInPitline | | |
| setCarFFB | | |

### Driver Functions

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| getDriverName | | |
| getDriverNationCode | | |
| getCurrentSplits | | |
| getLastSplits | | |
| isConnected | | |

### Server Functions

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| getCarsCount | | |
| getServerHttpPort | | |
| getServerIP | | |
| getServerName | | |
| getServerSlotsCount | | |
| sendChatMessage | msg: str | |

### Environment Functions

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| getTrackConfiguration | | |
| getTrackLength | | |
| getTrackName | | |
| getWindDirection | | |
| getWindSpeed | a <br> b | |

### External Functions

| Function Name | Arguments | Description |
| :--- | :--- | :--- |
| ext_applyTrackConfig | a | |
| ext_chaserCameraDebugText | | |
| ext_currentPpFilter | a <br> b | |
| ext_debugFn | a <br> b | |
| ext_debugLights | | |
| ext_debugWiperSoundState | | |
| ext_getAltitude | | |
| ext_getAmbientMult | | |
| ext_getAngleSpeed | | |
| ext_getBaseAltitude | | |
| ext_getCameraFov | | |
| ext_getCameraMatrix | a | |
| ext_getCameraPos| a | |
| ext_getCameraProj | a <br> args | |
| ext_getCameraView | | |
| ext_getCarLightsMirrorVisible | | |
| ext_getCarLightsNum | | |
| ext_getCarLightsVisible(a) | | |
| ext_getHeadlights | a <br> b <br> c <br> d <br> e | |
| ext_getLightsMirrorVisible | | |
| ext_getLightsNum | a | |
| ext_getLightsVisible | a | |
| ext_getTrackLightsMirrorVisible | | |
| ext_getTrackLightsNum | a | |
| ext_getTrackLightsVisible | | |
| ext_getTyreBlister | a <br> b | |
| ext_getTyreFlatSpot | a <br> b | |
| ext_getTyreGrain | a | |
| ext_getTyreVirtualKM | | |
| ext_glSetTexture | a <br> b | |
| ext_glTexCoord2f | | |
| ext_isG27Available | | |
| ext_isVaoPatchLoaded | | |
| ext_mirrorAspectRatioDown | a <br> b | |
| ext_mirrorAspectRatioUp | a | |
| ext_mirrorCurrent | | |
| ext_mirrorDebug | a | |
| ext_mirrorDown | | |
| ext_mirrorFovDown | | |
| ext_mirrorFovUp | | |
| ext_mirrorLeft | | |
| ext_mirrorNext | a <br> b | |
| ext_mirrorParams | a <br> b | |
| ext_mirrorPrev | a | |
| ext_mirrorRight | a | |
| ext_mirrorToggleMon | a <br> b | |
| ext_mirrorUp | | |
| ext_patchVersion | | |
| ext_patchVersionCode | | |
| ext_pauseFsWatching | | |
| ext_rainParams | | |
| ext_rainParamsAdjust | | |
| ext_rainParamsSet | | |
| ext_resetCar | | |
| ext_resumeFsWatching | a <br> b <br> c <br> d | |
| ext_setCameraFov | | |
| ext_setClipboardData | | |
| ext_setDoorsOpen | | |
| ext_setDriverVisible | a <br> b | |
| ext_setG27Thresholds | a <br> b <br> c <br> args | |
| ext_setTrackConditionInput | | |
| ext_setVaoActive | | |
| ext_takeAStepBack | a | |
| ext_vaoDisable | a <br> b <br> c <br> d | |
| ext_vaoNormal | | |
| ext_vaoNormalDebug | a <br> b | |
| ext_vaoOnly | | |
| ext_weatherDebugText | | |
| ext_weatherFxActive | | |
| ext_weatherTimeOffset | a <br> b | |
