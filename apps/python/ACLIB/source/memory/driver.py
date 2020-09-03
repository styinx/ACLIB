class Driver:
    def __init__(self, info):
        self._info = info

    @property
    def firstname(self):
        return self._info.static.playerName

    @property
    def lastname(self):
        return self._info.static.playerSurname

    @property
    def full_name(self):
        return self.firstname + ' ' + self.lastname

    @property
    def nick(self):
        return self._info.static.playerNick

    @property
    def name_abbreviation(self):
        return (self.nick[0:3] + ' ' + self.nick[-3:]).upper()
