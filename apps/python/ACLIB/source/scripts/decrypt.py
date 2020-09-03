import os
from sys import stdout
from source.util.acd import decryptACD

def log(what: str):
    stdout.write(what)

def unpackACD(folder, output=None):
    files = None
    folder_name = None
    out_path = '.'

    log('Decrypt {} ...'.format(folder))
    folder_name, files = decryptACD(folder)
    out_path = folder_name + '_decrypted'
    log('done\n')

    if output:
        out_path = output

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    log('Write results to {} ...'.format(out_path))
    for file, content in files.items():
        f = open(os.path.join(out_path, file), 'w+')
        f.write(content)
        f.close()
    log('done\n')