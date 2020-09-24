from settings import METADATA_DIR, path
from storage.config import Config


class Tyres:
    def __init__(self, data, acd: dict):
        self._acd = acd
        self._brake_config = Config(self._acd['brakes.ini'], only_strings=True)
        self._tyre_config = Config(self._acd['tyres.ini'], only_strings=True)
        self._tyre_meta = Config(path(METADATA_DIR, data.car.model, 'ACLIB_tyres.ini'))

        compound = ''
        for sec_name, section in self._tyre_config.dict.items():
            if 'NAME' in section:
                compound = section['NAME']

            if compound and section:
                self._tyre_meta.select(compound)

                if sec_name.find('THERMAL_FRONT') > -1 or sec_name.find('THERMAL_REAR') > -1:
                    position = 'front' if sec_name.find('THERMAL_FRONT') > -1 else 'rear'
                    self._tyre_meta.set(position + '_temp_curve', self._lut_dict(section['PERFORMANCE_CURVE']))

                elif sec_name.find('FRONT') > -1 or sec_name.find('REAR') > -1:
                    position = 'front' if sec_name.find('FRONT') > -1 else 'rear'
                    self._tyre_meta.set(position + '_ideal_pressure', section['PRESSURE_IDEAL'])
                    self._tyre_meta.set(position + '_wear_curve', self._lut_dict(section['WEAR_CURVE']))

        self._tyre_meta.select('Brakes')
        if 'TEMPS_FRONT' in self._brake_config.dict:
            if 'PERF_CURVE' in self._brake_config['TEMPS_FRONT']:
                self._tyre_meta.set('front_brake_temp_curve',
                                    self._lut_dict(self._brake_config['TEMPS_FRONT']['PERF_CURVE']))

                self._tyre_meta.set('rear_brake_temp_curve',
                                    self._lut_dict(self._brake_config['TEMPS_REAR']['PERF_CURVE']))
            else:
                # If there is no data on the brake temperature we use a default
                self._tyre_meta.set('front_brake_temp_curve',
                                    self._inline_lut_dict('(|0=0.70|300=0.8|500=1.0|600=1.0|800=0.7|1200=0.2|)'))
                self._tyre_meta.set('rear_brake_temp_curve',
                                    self._inline_lut_dict('(|0=0.70|300=0.8|500=1.0|600=1.0|800=0.7|1200=0.2|)'))
        else:
            # If there is no data on the brake temperature we use a default
            self._tyre_meta.set('front_brake_temp_curve',
                                self._inline_lut_dict('(|0=0.70|300=0.8|500=1.0|600=1.0|800=0.7|1200=0.2|)'))
            self._tyre_meta.set('rear_brake_temp_curve',
                                self._inline_lut_dict('(|0=0.70|300=0.8|500=1.0|600=1.0|800=0.7|1200=0.2|)'))

    def _lut_dict(self, file: str):
        content = self._acd[file]
        d = {}
        for line in content.split('\n'):
            if line.find('|') > -1:
                k, v = line.split('|')
                d[k] = v
        return d

    def _inline_lut_dict(self, content: str):
        d = {}
        for line in content.split('|'):
            if line.find('=') > -1:
                k, v = line.split('=')
                d[k] = v
        return d

    def ideal_pressure(self, compound: str, front: bool):
        if compound in self._tyre_meta.dict:
            key = 'front' if front else 'rear'
            return self._tyre_meta.dict[compound][key + '_ideal_pressure']
        else:
            return 26

    def ideal_temperature(self, compound: str, front: bool):
        if compound in self._tyre_meta.dict:
            key = 'front' if front else 'rear'
            min_max = [float(k) for k, v in self._tyre_meta.dict[compound][key + '_temp_curve'].items() if v == '1.0']
            return min(min_max), max(min_max)
        else:
            return 80, 100

    def ideal_brake_temperature(self, front: bool):
        key = 'front' if front else 'rear'
        min_max = [float(k) for k, v in self._tyre_meta.dict['Brakes'][key + '_brake_temp_curve'].items() if v == '1.0']
        return min(min_max), max(min_max)
