from memory.ac_data import ACData
from memory.ac_meta import ACMeta
from ui.animation import Animation
from ui.color import AnimationColor, TRANSPARENT
from ui.gui.widget import ACApp
from util.log import log


class Flag(ACApp):
    FLAG_COLOR = {1: (AnimationColor(0, 0, 0, 0), AnimationColor(0, 0, 1, 1)),    # Blue
                  2: (AnimationColor(0, 0, 0, 0), AnimationColor(1, 1, 0, 1)),    # Yellow
                  3: (AnimationColor(0, 0, 0, 0), AnimationColor(0, 0, 0, 1)),    # Black
                  4: (AnimationColor(0, 0, 0, 0), AnimationColor(1, 1, 1, 1)),    # White
                  5: (AnimationColor(0, 0, 0, 1), AnimationColor(1, 1, 1, 1)),    # Checkered
                  6: (AnimationColor(0, 0, 0, 0), AnimationColor(1, 0, 0, 1))}    # Penalty /This should not be red :( )

    def __init__(self, data: ACData = None, meta: ACMeta = None):
        super().__init__('ACLIB_Flag', 200, 200, 150, 150)

        self.hide_decoration()

        self._data = data

        data.on(ACData.EVENT.FLAG_CHANGED, self.show_flag)

    def show_flag(self, flag: int):
        start, step, stop = None, None, None
        granularity = 0.1

        log(flag)

        # If there is an active animation remove it.
        self.animation = None

        if 1 <= flag <= 6:
            # Start color of the animation
            start = Flag.FLAG_COLOR[flag][0]

        # Checkered is White -> Black
        if flag == 5:
            step = AnimationColor(-granularity, -granularity, -granularity, 0)
        # Unknown or no flag
        else:
            pass

        if start is not None:
            # Stop color of the animation
            stop = Flag.FLAG_COLOR[flag][1]
            if step is None:
                step = stop * granularity
            self.add_animation(Animation(self, 'background_color', start, step, stop, 10, 'Alternate'))

    def update(self, delta: int):
        super().update(delta)
