from source.aclib import ACLIB
from source.gui import ACApp, ACGrid, ACLabel
from source.widget import ACShiftLightBarWidget, ACShiftLightWidget, ACTwinShiftLightWidget


class Test(ACApp):
    def __init__(self):
        super().__init__("ACLIB_Test", 200, 200, 512, 96)

        self.hideDecoration()

        self.grid = ACGrid(self, 5, 5)

        self.s1 = ACShiftLightWidget()
        self.s2 = ACTwinShiftLightWidget()
        self.s3 = ACShiftLightBarWidget()
        self.text = ACLabel("", self, font_size=16, bold=1, text_h_alignment="center")

        self.grid.addWidget(self.s1, 0, 0, 5, 1)
        self.grid.addWidget(self.s2, 0, 2, 5, 1)
        self.grid.addWidget(self.text, 2, 2, 1, 1)
        self.grid.addWidget(self.s3, 0, 4, 5, 1)

    def update(self, delta):
        super().update(delta)

        self.text.setText("{:4.0f}".format(ACLIB.CARS[0].rpm))

    def render(self, delta):
        super().render(delta)
