## GUI

```python
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.ac_widget import ACApp, ACLabel
from ui.gui.layout import ACGrid


class Time(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('Time', 200, 200, 98, 160)

        self._grid = ACGrid(2, 2, self)

        self._label = ACLabel(self)
        self._time = ACLabel(self)

        self._grid.add(self._label, 0, 0)
        self._grid.add(self._time, 0, 0)
```

![GUI](https://github.com/styinx/ACLIB/blob/master/stuff/images/gui.svg 'GUI')

![Classes](https://github.com/styinx/ACLIB/blob/master/stuff/images/classes.svg 'Classes')
