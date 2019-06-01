from os import listdir
from os.path import isfile, join

def Files():
    files = [f for f in listdir('uploads') if isfile(join('uploads', f))]
    return files