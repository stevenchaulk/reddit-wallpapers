#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import os
import ctypes
import random

def set_desktop( imagePath ):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath, 3)

def random_file( path ):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for file in onlyfiles:      # remove files that do not have the .jpg or .png extension
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            onlyfiles.remove(file)
    if len(onlyfiles) == 0:     # raise error if 'path' string provided no valid files
        raise NameError("Invalid path name. No files at location.")
    randNum = random.randint(0, len(onlyfiles) - 1)
    return onlyfiles[randNum]

def set_random_desktop( folderPath ):
    try:
        image = random_file(folderPath)
        image_path = os.path.join(folderPath, image)
        set_desktop(image_path)
        return image_path
    except NameError as e:
        print(e)
        return ""

if __name__ == "__main__":
    print("Running " + __file__ + " as main.")