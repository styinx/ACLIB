#from source.db import DB
from source.color import Color
from source.gui import ACApp, ACLabel, ACVBox
from source.aclib import ACLIB
from source.gl import texture_rect, Texture


def acMain(version):
    global app, aclib, vbox, text1, text2, text3, text4, pos, loops
    global tex_info_panel
    global tex_tower_even, tex_tower_odd, tex_tower_even_loss, tex_tower_odd_loss, tex_tower_even_gain, tex_tower_odd_gain

    tex_info_panel = Texture("apps/python/ACLIB/resources/info_panel.png")
    tex_tower_even = Texture("apps/python/ACLIB/resources/tower_even.png")
    tex_tower_odd = Texture("apps/python/ACLIB/resources/tower_odd.png")
    tex_tower_even_loss = Texture("apps/python/ACLIB/resources/tower_even_loss.png")
    tex_tower_odd_loss = Texture("apps/python/ACLIB/resources/tower_odd_loss.png")
    tex_tower_even_gain = Texture("apps/python/ACLIB/resources/tower_even_gain.png")
    tex_tower_odd_gain = Texture("apps/python/ACLIB/resources/tower_odd_gain.png")

    loops = 0

    aclib = ACLIB()

    app = ACApp("ACLIB", 200, 200, 160, 192)

    pos = ACVBox(app)
    pos1 = ACLabel("", app)
    pos2 = ACLabel("", app)
    pos3 = ACLabel("", app)
    pos4 = ACLabel("", app)
    pos5 = ACLabel("", app)
    pos6 = ACLabel("", app)

    pos.addWidget(pos1.setBackgroundTexture(tex_tower_even).setFontSize(24).setText(" 1 ABC").setTextAlignment("left", "middle"))
    pos.addWidget(pos2.setBackgroundTexture(tex_tower_odd).setFontSize(24).setText(" 2 FBA").setTextAlignment("left", "middle"))
    pos.addWidget(pos5.setBackgroundTexture(tex_tower_even_gain).setFontSize(24).setText(" 3 aBC").setTextAlignment("left", "middle"))
    pos.addWidget(pos4.setBackgroundTexture(tex_tower_odd_loss).setFontSize(24).setText(" 4 EBc").setTextAlignment("left", "middle"))
    pos.addWidget(pos6.setBackgroundTexture(tex_tower_odd_gain).setFontSize(24).setText(" 5 AdC").setTextAlignment("left", "middle"))
    pos.addWidget(pos3.setBackgroundTexture(tex_tower_even_loss).setFontSize(24).setText(" 6 DBC").setTextAlignment("left", "middle"))

    text1 = ACLabel("", app)
    text2 = ACLabel("", app)
    text3 = ACLabel("", app)
    text4 = ACLabel("", app)

    vbox = ACVBox()
    vbox.addWidget(text1)
    vbox.addWidget(text2)
    vbox.addWidget(text3)
    vbox.addWidget(text4)

    app.setRenderCallback(acRender)
    app.setBackgroundColor(Color(0, 0, 0, 0.75))

    return app.run()


def acUpdate(delta):
    global app, aclib, vbox, text1, text2, loops, pos

    if not app.isSuspended():

        aclib.update(delta)

        if loops % 5 == 0:
            car = aclib.CARS[0]
            text1.setText("lap " + str(car.lap) + " | sector " + str(car.sector) + " | mini sector " + str(car.mini_sector) + " | km " + str(car.km))
            text2.setText(str(car.lap_fuel) + " l/lap | " + str(car.sector_fuel) + " l/sec | " + str(car.mini_sector_fuel) + " l/msec | " + str(car.km_fuel) + " l/km")
            text3.setText(str(car.lap_fuel_range) + " laps| " + str(car.sector_fuel_range) + " sectors " + str(car.mini_sector_fuel_range) + " mini sectors " + str(car.km_fuel_range) + " kms")
            text4.setText(str(car.lap_time) + " | " + str(car.sector_time) + " " + str(car.mini_sector_time) + " | " + str(car.km_time))

        app.update()

        loops += 1
        if loops == 1000:
            loops = 0

        pos.update()


def acRender(delta):
    global tex_info_panel, pos

    texture_rect(0, 200, 320, 48, tex_info_panel, Color(1, 0, 0, 1))
    texture_rect(0, 250, 320, 48, tex_info_panel, Color(0, 1, 0, 1))

    pos.render()


def acShutdown():
    i = 0
