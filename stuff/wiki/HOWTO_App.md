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
 |...
```

## Implementation

In the following, we implement an example app that shows the local time.
Please note that it shows only the most basic structure of an app.
If you are interested in more complex structures and how to get the shared memory data or metadata search in the wiki for the corresponding page.

```python
from time import time

from memory.ac_data import ACData                                           # Only import the first two modules if you care
from memory.ac_meta import ACMeta                                           # about proper typing signatures.
from ui.gui.widget import ACApp, ACLabel
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
        self._local_time = ACLabel('', parent=self)                         # An ACLabel takes a string as the initial text.
        self._session_time = ACLabel('', parent=self)                       # To work properly any AC widget needs to have
                                                                            # parent argument which allows to find the app id.
                                                                            # In this case app and parent are the same.
        self._grid.add(ACLabel('Local time:', parent=self), 0, 0)           # In order to add a widget to a grid you have
        self._grid.add(self._local_time, 1, 0)                              # to use the 'add' function and give it a widget
                                                                            # of type ACWidget and the x and y coordinates
        self._grid.add(ACLabel('Expired time:', parent=self), 0, 1)         # within the grid (starting from top left 0, 0).
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

## Additional

- configuration file
- style