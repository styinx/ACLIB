# ACLIB

_Assetto Corsa App Library_

<br>

## Features

- Assetto Corsa GUI
- Extensible Widget Collection
- Car Data in one place
- Animations
- ~~Overhead detection~~
- ~~SQLite3 Database Connection~~
- GUI Events / ACLIB Events
- Realtime App Configuration and Stylesheets

<br> 

## Issues

- tyre temperatures do not work for DLC cars

## Install

- **1**
  - Either: Download the repository
  - Or: ```git clone https://github.com/styinx/ACLIB```

- **optional**
  - remove the folder /images and README.md

- **2**
  - extract the folders /apps and /contents into the location where you have Assetto Corsa installed (usually ```C:/Program Files (x86)/Steam/steamapps/common/assettocorsa```)

- **3**
  - run Assetto Corsa
  - enable ACLIB in the settings
  
<br>

## Getting Started

If you have installed the library into AC then you can start to code.
If you want to create a new app you have to create a file into the folder ```assettocorsa/apps/ACLIB/apps/```.
The filename of the app needs to have the following pattern: **ACLIB_**_name of your app_**.py**
Within this file you need to create a App class that has the name _name of your app_.
This class must inherit from the class ACApp from the module ```source.gui```.
Here is an example:

- ACLIB/:
    - apps/
        - ACLIB_Test.py
        - ACLIB_MyNewApp.py
        - ...

**ACLIB_MyNewApp.py**     
```python
from source.gui import ACApp, ACLabel
from source.gl import rect

class MyNewApp(ACApp):
    def __init__(self):
        super().__init__("MyCustom App Name", 0, 0, 200, 200)
        
        self.my_widget = ACLabel("", self, self)
             
    # update is called in 'acUpdate(delta)'
    def update(self, delta):
        super().update(delta)
        self.my_widget.setText("widget text: " + str(delta))
        
    # render is called automatically from the app
    # use opengl functions only in this method
    def render(self, delta):
        super().render(delta)
        r = self.geometry
        rect(r=r.add(y=-5, h=5))
```

Afterward, you can extend the app with widgets and custom elements.
Please note, that you can look into existing apps to see how to create a new app.

<br>

## Features in Detail

### Assetto Corsa GUI:

- Composite Model wrapped around AC GUI elements
- Layout Elements (grid, box, ...)

Example:
```python
# Note that such an app is only possible if the contents are placed in the file ACLIB.py
# Please prefer the example shown in 'Getting Started'.
from source.aclib import ACLIB
from source.gui import ACApp, ACGrid, ACLabel, ACLabelPair

def acMain(version):
    global myapp, lap_title, laps, pos_widget

    myapp = ACApp("my app name", 0, 0, 200, 200).hideDecoration()
    grid = ACGrid(myapp, 2, 2)
    lap_title = ACLabel("", myapp, text_h_alignment="center")
    laps = ACLabel("", myapp)
    pos_widget = ACLabelPair(myapp, label=ACLabel("", myapp, text_h_alignment="center"), widget=ACLabel("", myapp))

    grid.addWidget(lap_title, 0, 0, 1, 1)
    grid.addWidget(laps, 1, 0, 1, 1)
    grid.addWidget(pos_widget, 0, 1, 2, 1)
    
def acUpdate(delta):
    global myapp, lap_title, laps, pos_widget

    current_car = ACLIB.getFocusedCar()

    lap_title.setText("Laps: ")
    laps.setText("{:d}/{:2}".format(ACLIB.CARS[current_car].lap, ACLIB.getLaps()))
    pos_widget.label_widget.setText("Pos: ")
    pos_widget.pair_widget.setText("{:d}/{:d}".format(ACLIB.CARS[current_car].position, ACLIB.getCarsCount()))

```

---

<br>

### Widget Collection:

- GUI Widgets (progress bar, ...)
- Car Widgets (tyres, shift indicators, fuel, ...)

---

<br>

### Car Data in one place:

- Data from all cars on the grid is updated and saved in the Car class.
- Common data fields like distance to next car is managed here.
- Reimplementation of those fields is therefore not necessary.
- Managed Fields:
    - gear, speed, rpm
    - position, class position, benefit (gained positions per lap) 
    - location, fuel, flag, pit status, penalties, 
    - other car distances and times (absolute and relative)
    - lap data (fastest km/mini sector/sector, current lap performance)
    - fuel per lap/sector/mini/km sector, estimated laps/sectors/mini sectors/km from fuel
    - tyre information (temperature, pressure, dirt, compound), also ideal temperature and pressure
    - and more ... 
- Session information is also stored:
    - fastest km/mini sector/sector/lap
    - session time
---

<br>

### Animations:

- Animations are supported for specific classes.
- These classes require the implementation of the following class methods:
    - \_\_add__ (val + other)
    - \_\_imul__ (val *= other)
    - \_\_ne__ (val != other)
    - \_\_eq__ (val == other)
    
A supported animation class looks like this:
```python
class Color:
    def __init__(self, r, g, b, a=1.0):
        self.r = r
        self.g = g
        self.b = b 
        self.a = a
         
    def __add__(self, other):
        return Color(max(min(self.r + other.r, 1), 0),
                     max(min(self.g + other.g, 1), 0),
                     max(min(self.b + other.b, 1), 0),
                     max(min(self.a + other.a, 1), 0))
     
    def __imul__(self, other):
        self.r *= other
        self.g *= other
        self.b *= other
        self.a *= other
        return self

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other):
        return not (self == other)
```


An applied animation looks like this:
```python
from source.color import Color
from source.animation import Animation
from source.widget import ACWidget

# only classes that inherit from ACWidget can take animations
my_widget = ACWidget().setSize((100, 100))
# the default animation is from type "forward"
# the property will have the stop value after the animation is finished
# in this example the background color of the widget goes from transparent to red 
my_forward_color_animation = Animation(my_widget, "background_color", 
                                       Color(0, 0, 0, 0), Color(0.1, 0, 0, 0.1), Color(1, 0, 0, 1))
# the "alternate" animation sets the property value back to the start value after the animation is finished
# in this example the background color goes from transparent to red and back to transparent
my_alternate_color_animation = Animation(my_widget, "background_color", 
                                         Color(0, 0, 0, 0), Color(0.1, 0, 0, 0.1), Color(1, 0, 0, 1), direction="alternate")

# currently only single animations are allowed
# when the first animation is finished, the second animation is pulled from the queue and added to the widget animation
my_widget.addAnimation(my_forward_color_animation)
my_widget.addAnimation(my_alternate_color_animation)
```

The following animation produces the animation shown in the image below:
```python
from source.color import Color
from source.math import Rect
from source.animation import Animation

def update(self, delta):
    super().update(delta)
    
    if self.loops % 100 == 0:
        start = Color(0, 0, 0, 1)
        step = Color(0.05, 0.05, 0, 0)
        stop = Color(1, 1, 0, 1)
        self.addAnimation(Animation(self, "background_color", start, step, stop, 0, "Alternate"))
        self.setBackgroundColor(Color(1, 1, 0))

    if self.loops % 500 == 0:
        x, y = self.getPos()
        w, h = self.getSize()
        start = Rect().set(x, y, w, h)
        step = Rect().set(0, 0, 1, 1)
        stop = Rect().set(x, y, w + 25, h + 25)
        self.addAnimation(Animation(self, "geometry", start, step, stop, 0, "Alternate"))

    if self.loops == 1000:
        self.loops = 0
    else:
        self.loops += 1
```

![Animation](https://github.com/styinx/ACLIB/blob/master/images/animation.gif "Animation")

---

<br>

### ~~Overhead Detection~~:

- ~~Based on the systems performance the apps used with ACLIB can suspend/resume expensive calculations.~~
---

<br>

### ~~SQLite3 Database~~:

- ~~useful to store cross sessions or other more complex data~~

---

<br>

### GUI Events / ACLIB Events:

- Ingame events can trigger custom functions
- Examples: Position change, Lap change, ...

---

### Realtime App Configuration (and Stylesheets):

- apps can be styled with configuration
- changes are applied in real time without reloading
- enables app customization without altering code
- stylesheets are not yet working

![Realtime Config](https://github.com/styinx/ACLIB/blob/master/images/config.gif "Realtime Config")

---

## Default Apps in ACLIB

Driver App:
- Shows the basic car and driver information.

![Driver](https://github.com/styinx/ACLIB/blob/master/images/driver.png "Driver App")

Tower App:
- Shows current standings.

![Tower](https://github.com/styinx/ACLIB/blob/master/images/tower.png "Tower App")

Notification App:
- Notifies driver when events occur.
- yellow flag, faster car behind, position gained/lost, penalty

