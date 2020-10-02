## Events

For some reason some parts of the shared memory module are sometimes not loaded instantly but with a delay.
As a result some properties from ACData or ACMeta are not loaded properly and access to those will result in errors.
The best example for this is the tyre compound.

To solve this issue the ACData module will fire a 'READY' event when it reads a tyre compound with a string length > 5.
The ACMeta module listens to this 'READY' event and will consequently fire another 'READY' event.
This is not an ideal solution but solves the problem.
Here is an example how you can use this event to have a proper error-free app:

```python
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.ac_widget import ACApp, ACLabel


class Test(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Test', 200, 200, 300, 300)

        self._ready = False
        self._data = data
        self._compound = ACLabel('', parent=self)

        meta.on(ACMeta.EVENT.READY, self.init)

    def init(self):
        self._ready = True

    def update(self, delta: int):
        super().update(delta)
        
        if self._ready:
            self._compound.text = self._data.tyres.compound
``` 

Keep in mind that this code will update the name of the compound every time the update function is called.
For properties that rarely change you should the appropriate events from ACData (`ACData.EVENT.COMPOUND_CHANGED`).

```python
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.gui.ac_widget import ACApp, ACLabel


class Test(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Test', 200, 200, 300, 300)

        self._data = data
        self._compound = ACLabel('', parent=self)

        data.on(ACData.EVENT.READY, self.init)

    def init(self):
        self._data.on(ACData.EVENT.COMPOUND_CHANGED, self.set_compound)

    def set_compound(self, name: str):
        self._compound.text = name

    def update(self, delta: int):
        super().update(delta)
            
```
