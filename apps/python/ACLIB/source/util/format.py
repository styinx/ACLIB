from time import strftime, localtime

from util.text import text, LAPS_ACR, LAP_ACR, MINUTES_ACR, MINUTE_ACR


class Format:
    @staticmethod
    def s(value: float, term: str):
        if abs(value) == 1:
            return str(value) + term
        else:
            return str(value) + term + 's'

    @staticmethod
    def pad(number: float, positions: int = 2):
        return ('{:0' + str(positions) + '}').format(number)

    @staticmethod
    def minute(d=None, h=None, s=None, ms=None, us=None, ns=None):
        pass

    @staticmethod
    def second(d=None, h=None, m=None, ms=None, us=None, ns=None):
        pass

    @staticmethod
    def time():
        return strftime("%H:%M:%S", localtime())

    @staticmethod
    def duration(ms: float = 0, form: str = "{m:02d}:{s:02d}.{ms:03d}"):
        millis = abs(int(ms))
        m = int(millis / 60000)
        s = int((millis % 60000) / 1000)
        ms = millis % 1000

        return form.format(m=m, s=s, ms=ms)

    @staticmethod
    def distance(meters: float = 0, form: str = '{km:02d}.{m:02.0f} km'):
        km = int(meters / 1000)
        m = (meters % 1000) / 10

        return form.format(km=km, m=m)

    @staticmethod
    def gear(gear: int):
        if gear == 0:
            return 'R'
        elif gear == 1:
            return 'N'

        return str(gear - 1)

    @staticmethod
    def rpm(rpm: int):
        return '{:d}'.format(rpm)

    @staticmethod
    def car_distance(dist_ms: float, dist_meters: float, track_len: float):
        track_len = max(track_len, 1000)

        if dist_meters > track_len:
            laps = dist_meters / track_len
            if laps > 1.05:
                return '{:3.1f} {}'.format(laps, text(LAPS_ACR))
            elif laps < 1.05:
                return '{:3.0f}   {}'.format(laps, LAP_ACR)

        if dist_ms > 60:
            minute = dist_ms / 60
            if minute > 1.05:
                return '{:3.1f} {}'.format(minute, MINUTES_ACR)
            elif minute < 1.05:
                return '{:3.0f}   {}'.format(minute, MINUTE_ACR)

        return Format.duration(int(dist_ms * 1000))