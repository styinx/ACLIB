import ac


class Server:
    def __init__(self):
        pass

    @property
    def name(self):
        return ac.getServerName()

    @property
    def ip(self):
        return ac.getServerIP()

    @property
    def port(self):
        return ac.getServerPort()

    @property
    def slots(self):
        return ac.getServerSlotsCount()

    @property
    def cars(self):
        return ac.getCarsCount()
