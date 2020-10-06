## Setup

Before you start to implement anything make sure that ACLIB works properly.
Start AC and check the console by hitting the `HOME` key (`Pos1` for german keyboards).
Check that there are no warnings on `ACLIB`.
Close AC again and make sure that ACLIB did create a `log.txt` file in the directory `C:/Users/<yourname>/Documents/Assetto Corsa/ACLIB/`.
If there are no warnings or errors you are good to go.

## Prerequisites 

By default, ACLIB will only look for **certain files** in **certain directories** so make sure you get it correct.
Any new app must be implemented in a separate file with the name `ACLIB_<app_name>.py`.
This file must be placed in the `apps` directory in the ACLIB installation folder `C:/Program Files (x86)/Steam/steamapps/common/assettocorsa/apps/python/ACLIB/apps/`

The file structure should look like this:
```
apps/
 |- ACLIB_SuperApp.py
 |- ACLIB_Time.py
 |- ACLIB_Stats.py
 |...
```

## ACLIB_Time Implementation

In the following, we implement an example app that shows the local time.
Please note that it shows only the most basic structure of an app.

```python
from time import time

from memory.ac_data import ACData                                           # Only import the first two modules if you care
from memory.ac_meta import ACMeta                                           # about proper typing signatures.
from ui.gui.ac_widget import ACApp, ACLabel
from ui.gui.layout import ACGrid
from util.format import Format


class Time(ACApp):                                                          # Any new app must inherit from ACApp.
    def __init__(self, data: ACData = None, meta: ACMeta = None):           # Any app takes an ACData and ACMeta object.
        super().__init__('My local Time', 200, 200, 160, 80)                # Here you can specify the name of the app
                                                                            # that is displayed in the in-game taskbar
                                                                            # and the initial position and size (x, y, w, h).
        
        self._start = time()                                                # We memorize the timestamp when the app was started.

        self._grid = ACGrid(2, 2, self)                                     # A grid manages the positioning of labels/buttons/...
                                                                            # This grid has 4 cells (2x2) and fills the size 
                                                                            # of the app (160px width 80px height).
        self._local_time = ACLabel(self, '')                                # An ACLabel takes a string as the initial text.
        self._session_time = ACLabel(self, '')                              # To work properly any AC widget needs to have
                                                                            # parent argument which allows to find the app id.
                                                                            # In this case app and parent are the same.
        self._grid.add(ACLabel(self, 'Local time:'), 0, 0)                  # In order to add a widget to a grid you have
        self._grid.add(self._local_time, 1, 0)                              # to use the 'add' function and give it a widget
                                                                            # of type ACWidget and the x and y coordinates
        self._grid.add(ACLabel(self, 'Expired time:' ), 0, 1)               # within the grid (starting from top left 0, 0).
        self._grid.add(self._session_time, 1, 1)

        self.hide_decoration()                                              # This function hides the AC symbol and
                                                                            # the title of the app.
    def update(self, delta: int):                                           # In the update function we set the values that
        self._local_time.text = Format.time()                               # have changed since the last iteration.
        self._session_time.text = Format.duration(time() - self._start)     # In our case we keep the current time and the
                                                                            # time that has expired up to date.
```

It is **important** that the name of the class must match the suffix after the underscore (`ACLIB_`) of the filename `<app_name>`.
That is all!
You can now start AC and activate the Time app in the app taskbar.


## ACLIB_Stats Implementation

In the following, we implement a more complex app that uses events and ACData/ACMeta.

```python
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.ac_widget import ACApp, ACLabel
from ui.gui.layout import ACGrid
from util.format import Format


class Stats(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('My Stats App', 200, 200, 200, 100)
    
        # We store the ACData and ACMeta module for later.
        self._data = data
        self._meta = meta
        
        # Again we use a grid as layout and bind it to the size of the app (200x100).
        # We get 16 cells, each cell will have a size of 50x25. 
        self._grid = ACGrid(4, 4, self)

        # We attach the labels of the values to the grid.
        # Since we do not modify the labels we can simply call the constructors of ACLabel inline.
        self._grid.add(ACLabel(self._grid, 'Lap'), 0, 0)
        self._grid.add(ACLabel(self._grid, 'Compound'), 0, 1)

        # We create the values and attach it to the grid.
        self._lap = ACLabel(self._grid)
        self._compound = ACLabel(self._grid)

        self._grid.add(self._lap, 1, 0)
        self._grid.add(self._compound, 1, 1)
    
        # We add an a callback function that is called when the ACData module is ready.
        # Some values from the shared memory might not be set when the App is initialized.
        self._data.on(ACData.EVENT.READY, self.on_ready)

    def on_ready(self):
        # When the ACData module is ready we can be sure that the values exists and safely request them.
        
        # For a list of available categories take a look at the wiki:
        # https://github.com/styinx/ACLIB/wiki/ACData, https://github.com/styinx/ACLIB/wiki/ACMeta

        # The current lap starting from 0.
        self._lap.text = self._data.timing.lap
        # Full name of the tire compound. 
        self._compound.text = self._data.tyres.compound 
 
        # Since the value of the lap and the compound do not change that often we can simply get 
        # notified when they do and react to it.
        self._data.on(ACData.EVENT.LAP_CHANGED, self.on_lap_changed)
        self._data.on(ACData.EVENT.COMPOUND_CHANGED, self.on_compound_changed)

    def on_lap_changed(self, lap: int):
        self._lap.text = lap

    def on_compound_changed(self, compound: str):
        self._compound.text = compound
```

## Additional

- configuration file
- style