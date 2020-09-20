import os
from struct import unpack


# Computes the hash keys of a folder/filename.
def get_ACD_key(name):
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

    return '-'.join([str(x & 0xff) for x in [key1, key2, key3, key4, key5, key6, key7, key8]])


# Reads a *.acd file and stores the filenames and their contents in a dictionary.
# Returns the decrypted folder name and the dictionary.
def decrypt_ACD(filepath):
    result = {}
    f = open(filepath, 'rb')
    buffer_size = os.path.getsize(filepath)
    buffer = bytearray(f.read(buffer_size))
    buffer_len = len(buffer)

    filepath = filepath.replace('\\', '/')

    folder = filepath[:filepath.rfind('/')]
    key = get_ACD_key(folder[folder.rfind('/') + 1:])

    index = 0

    if unpack('l', buffer[index:index + 4])[0] < 0:
        index += 8
    else:
        index = 0

    while index < buffer_len:
        file_name_len = unpack('L', buffer[index:index + 4])[0]
        index += 4

        file_name = buffer[index:index + file_name_len].decode('utf8')
        index += file_name_len

        file_size = unpack('L', buffer[index:index + 4])[0]
        index += 4

        file_content = buffer[index:index + file_size * 4][::4]
        index += file_size * 4

        content = ''
        key_len = len(key)
        for i in range(0, file_size):
            val = file_content[i] - ord(key[i % key_len])
            if 0 < val < 256:
                content += chr(val)

        result[file_name] = content

    return folder, result


def write_ACD(folder: str, out_path: str, acd_contents = None):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

        if acd_contents:
            folder_name, files = acd_contents
        else:
            folder_name, files = decrypt_ACD(folder)

        for file, content in files.items():
            f = open(os.path.join(out_path, file), 'w+', encoding='utf-8')
            f.write(content)
            f.close()
