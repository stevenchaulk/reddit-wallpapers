import sqlite3
import os

def convert_unit(size):
    s = size
    units = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while s >= 1024 and i < (len(units)-1):
        s /= 1024
        i += 1
    return {"value": int(s), "unit":units[i]}

def convert_unit_shift(size):
    units = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size >= 1024 and i < (len(units) - 1):
        size = size >> 10
        i += 1
    return {"value": int(size), "unit": units[i]}

def add_row(image, url, sizeInBytes, date, time):
    conn = sqlite3.connect(os.getcwd() + "\\test.db")
    c = conn.cursor()
    temp = convert_unit_shift(sizeInBytes)
    t = (image, url, temp["value"], temp["unit"], date, time)
    c.execute("INSERT INTO downloads VALUES (?,?,?,?,?,?)", t)
    conn.commit()
    conn.close()

def image_exists(image):
    conn = sqlite3.connect(os.getcwd() + "\\test.db")
    c = conn.cursor()
    t = (image,)
    for row in c.execute("SELECT * FROM downloads WHERE image=?", t):
        conn.close()
        return True
    conn.close()
    return False


if __name__ == "__main__":
    print("Running " + __file__ + " as main.")
