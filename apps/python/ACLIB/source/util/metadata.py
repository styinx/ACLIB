from scripts.decrypt import unpackACD


class MetaData:
    STORAGE_DIR = 'metadata/'

    @staticmethod
    def decryptCarData(car_name):
        unpackACD(car_name, MetaData.STORAGE_DIR)

    @staticmethod
    def get_ideal_pressure(car_name):
        return 0, 0

    @staticmethod
    def get_ideal_temperature(car_name):
        return (0, 0), (0, 0)

#     def init(self):
#         tyres = self.data['tyres.ini']
#         compound = ''
#         for sec in tyres:
#             if sec.find('FRONT') or sec.find('REAR'):
#                 if 'SHORT_NAME' in tyres[sec]:
#                     compound = tyres[sec]['SHORT_NAME']
#                     if compound not in self.tyres:
#                         self.tyres[compound] = {}
#                 if compound != '':
#                     if 'PRESSURE_IDEAL' in tyres[sec]:
#                         if re.match(r'FRONT_?', sec):
#                             self.tyres[compound]['pressure_ideal_front'] = tyres[sec]['PRESSURE_IDEAL']
#                         elif re.match(r'REAR_?', sec):
#                             self.tyres[compound]['pressure_ideal_rear'] = tyres[sec]['PRESSURE_IDEAL']
#                     if 'PERFORMANCE_CURVE' in tyres[sec]:
#                         _min, _max = self.readOptimum(tyres[sec]['PERFORMANCE_CURVE'])
#                         if sec.find('THERMAL_FRONT'):
#                             self.tyres[compound]['temp_ideal_front_min'] = _min
#                             self.tyres[compound]['temp_ideal_front_max'] = _max
#                         elif sec.find('THERMAL_REAR'):
#                             self.tyres[compound]['temp_ideal_rear_min'] = _min
#                             self.tyres[compound]['temp_ideal_rear_max'] = _max
#
#     def readOptimum(self, lut_file, optimum='1.0'):
#         _min, _max = -1, -1
#
#         for line in self.data[lut_file].split('\n'):
#             vals = line.split('|')
#             if vals[1] == optimum and _min == -1:
#                 _min = int(vals[0])
#             elif vals[1] == optimum and _min != -1:
#                 _max = int(vals[0])
#                 break
#
#         if _max == -1:
#             _max = _min
#
#         return _min, _max
#
# @staticmethod
#     def getTrackMetaData():
#         name = ACLIB.getTrackName()
#         conf = ACLIB.getTrackConfiguration()
#         if conf != '':
#             file = open('content/tracks/' + name + '/ui/ui_track.json')
#         else:
#             file = open('content/tracks/' + name + '/ui/' + conf + '/ui_track.json')
#         return json.loads(file.read())
#
#     @staticmethod
#     def getCarMetadata(car):
#         name = ACLIB.getCarId(car)
#         file = open('content/cars/' + name + '/ui/ui_car.json')
#         return json.loads(file.read())
#
#     @staticmethod
#     def getCarData(car=0, cache=False):
#         name = ACLIB.getCarId(car)
#
#         if cache:
#             if not os.path.isdir('apps/python/ACLIB/data/'):
#                 os.mkdir('apps/python/ACLIB/data/')
#
#             if os.path.isfile('apps/python/ACLIB/data/' + name + '.acd.chached'):
#                 data = pickle.load(open('apps/python/ACLIB/data/' + name + '.acd.chached', 'rb'))
#             else:
#                 data = decryptACD('content/cars/' + name + '/data.acd')
#                 pickle.dump(data, open('apps/python/ACLIB/data/' + name + '.acd.chached', 'wb'))
#                 return data
#         else:
#             return decryptACD('content/cars/' + name + '/data.acd')
#
#     @staticmethod
#     def getCarClass(car=0):
#         name = ACLIB.getCarId(car)
#         file = open('content/cars/' + name + '/ui/ui_car.json')
#         for line in file.readlines():
#             class_line = line.split(':')
#             if class_line[0].strip() == '\'tags\'':
#                 try:
#                     class_index = class_line[1].index('#')
#                     return class_line[1][class_index + 1:class_line[1].index('\'', class_index)].lower()
#                 except ValueError:
#                     return ''
#
#     @staticmethod
#     def getCarBadge(car=0, form=None):
#         name = ACLIB.getCarId(car)
#         return Texture('content/cars/' + name + '/ui/badge.png')
#
#     @staticmethod
#     def getCarBrand(car=0, form=None):
#         name = ACLIB.getCarId(car)
#         file = open('content/cars/' + name + '/ui/ui_car.json')
#         for line in file.readlines():
#             class_line = line.split(':')
#             if class_line[0].strip() == '\'brand\'':
#                 return class_line[1].strip().replace('\'', '')
#
#     @staticmethod
#     def getCarName(car=0, form=None):
#         name = ACLIB.getCarId(car)
#         file = open('content/cars/' + name + '/ui/ui_car.json')
#         for line in file.readlines():
#             class_line = line.split(':')
#             if class_line[0].strip() == '\'name\'':
#                 return class_line[1].strip().replace('\'', '')
#
#     @staticmethod
#     def getCarType(car=0, form=None):
#         name = ACLIB.getCarId(car)
#         file = open('content/cars/' + name + '/ui/ui_car.json')
#         for line in file.readlines():
#             class_line = line.split(':')
#             if class_line[0].strip() == '\'class\'':
#                 return class_line[1].strip().replace('\'', '')