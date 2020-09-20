import ac

def active_car_only(func):
    if ac.getFocusedCar() == 0:
        return func()
    else:
        return - 1
