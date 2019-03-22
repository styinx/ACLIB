import os
from struct import unpack
from source.config import Config


def getKey(name):
    key1 = key2 = key3 = 0
    key4 = 0x1683
    key5 = 0x42
    key6 = 0x65
    key7 = key8 = 0xab

    # 1
    for c in name:
        key1 += ord(c)

    # 2
    for i in range(0, len(name) - 1, 2):
        key2 *= ord(name[i])
        i += 1
        key2 -= ord(name[i])

    # 3
    for i in range(1, len(name) - 3, 3):
        key3 *= ord(name[i])
        i += 1
        key3 = int(key3 / (ord(name[i]) + 0x1b))
        i -= 2
        key3 += (-0x1b - ord(name[i]))

    # 4
    for i in range(1, len(name)):
        key4 -= ord(name[i])

    # 5
    for i in range(1, len(name) - 4, 4):
        t1 = (ord(name[i]) + 0xf) * key5
        i -= 1
        key5 = (ord(name[i]) + 0xf) * t1 + 0x16
        i += 1

    # 6
    for i in range(0, len(name) - 2, 2):
        key6 -= ord(name[i])

    # 7
    for i in range(0, len(name) - 2, 2):
        key7 %= ord(name[i])

    # 8
    for i in range(0, len(name) - 1):
        key8 = int(key8 / ord(name[i]))
        i += 1
        key8 += ord(name[i])
        i -= 1

    return "-".join([str(x & 0xff) for x in [key1, key2, key3, key4, key5, key6, key7, key8]])


def decryptACD(filepath, keys=True):
    result = {}
    f = open(filepath, "rb")
    buffer_size = os.path.getsize(filepath)
    buffer = bytearray(f.read(buffer_size))
    buffer_len = len(buffer)

    folder = filepath[:filepath.rfind("/")]
    key = getKey(folder[folder.rfind("/") + 1:])

    index = 0

    if unpack("l", buffer[index:index + 4])[0] < 0:
        index += 8
    else:
        index = 0

    while index < buffer_len:
        file_name_len = unpack("L", buffer[index:index + 4])[0]
        index += 4

        file_name = buffer[index:index + file_name_len].decode("utf8")
        index += file_name_len

        file_size = unpack("L", buffer[index:index + 4])[0]
        index += 4

        file_content = buffer[index:index + file_size * 4][::4]
        index += file_size * 4

        content = ""
        key_len = len(key)
        for i in range(0, file_size):
            val = file_content[i] - ord(key[i % key_len])
            if 0 < val < 256:
                content += chr(val)

        if not keys:
            result[file_name] = content
        else:
            if file_name[-3:] == "ini" and content != "":
                conf = Config(content, False)
                result[file_name] = {}
                for s in conf:
                    result[file_name][s] = {}
                    for k in conf.get(s):
                        result[file_name][s][k] = conf.get(s, k)
            else:
                result[file_name] = content

    return result
