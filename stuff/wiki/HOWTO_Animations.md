## Animations

- Animations are only supported for classes that have specific methods implemented:
    - \_\_add__
    - \_\_imul__
    - \_\_ne__
    - \_\_eq__
    
A supported animation class looks like this:
```python
class AnimationColor:
    def __init__(self, r: float, g: float, b: float, a: float):
        """
        A color is represented by 4 components. Red, green, blue and alpha value.
        The value of any component ranges from -1.0 to 1.0.
        The minimum must be -1.0 since we have to subtract a value in an animation (the value of the step color). 
        """
        self.r = max(min(r, 1.0), -1.0)
        self.g = max(min(g, 1.0), -1.0)
        self.b = max(min(b, 1.0), -1.0)
        self.a = max(min(a, 1.0), -1.0)
         
    def __add__(self, other):
        """
        All components of both colors are added together.
        Example:
            c1 = Color(0, 1, 0, 1)  # Green
            c2 = Color(1, 0, 0, 1)  # Red
            c3 = c1 + c2            # Yellow Color(1, 1, 0, 1)   
        """
        return Color(max(min(self.r + other.r, 1.0), -1.0),
                     max(min(self.g + other.g, 1.0), -1.0),
                     max(min(self.b + other.b, 1.0), -1.0),
                     max(min(self.a + other.a, 1.0), -1.0))
     
    def __imul__(self, other):
        self.r *= other
        self.g *= other
        self.b *= other
        self.a *= other
        return self

    def __eq__(self, other):
        """
        Check the components of this Color instance against another one.
        Returns True if both colors have the exact same components, False otherwise. 
        """
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other):
        """
        Returns False if all components of this Color instance have the same values as the other instance, True otherise.  
        """
        return not (self == other)
```


An applied animation looks like this:
```python
# The usual imports...

# Only classes that inherit from ACWidget can take animations
my_widget = ACWidget()
my_widget.size = (100, 100)

# The default animation is from type 'forward'.
# The property will have the stop value after the animation is finished.
# In this example the `background_color` property of the widget goes from transparent to red. 
my_forward_color_animation = Animation(my_widget, 
                                       'background_color', 
                                       Color(0, 0, 0, 0), 
                                       Color(0.1, 0, 0, 0.1), 
                                       Color(1, 0, 0, 1))

# The 'alternate' animation sets the property value back to the start value after the animation is finished.
# Tn this example the `background_color`property goes from transparent to red and back to transparent.
my_alternate_color_animation = Animation(my_widget, 
                                         'background_color', 
                                         Color(0, 0, 0, 0), 
                                         Color(0.1, 0, 0, 0.1), 
                                         Color(1, 0, 0, 1), 
                                         direction='alternate')

# Currently only single animations are allowed.
# When the first animation is finished, the second animation is pulled from the queue and added to the widget animation.
my_widget.add_animation(my_forward_color_animation)
my_widget.add_animation(my_alternate_color_animation)
```

The following animation produces the animation shown in the image below:
```python
from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.animation import Animation
from ui.gui.widget import ACApp
from ui.color import RED, GREEN, AnimationColor

class Test(ACApp):
    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Test', 200, 200, 300, 300)

        start = RED
        stop = GREEN
        step = AnimationColor(-0.001, 0.001, 0, 0)
        self.add_animation(Animation(self, 'background_color', start, step, stop, -1, 'Forward'))

    def update(self, delta: int):
        super().update(delta)
```

![Animation](https://github.com/styinx/ACLIB/blob/master/stuff/images/animation_forward.gif 'Animation')

The `Alternate` animation looks like this.

![Animation](https://github.com/styinx/ACLIB/blob/master/stuff/images/animation_alternate.gif 'Animation')