from urllib.request import URLopener
import re
import time
import shutil
import os.path
import sys
import getopt
import sqlite3

# import custom modules
import changeDesktop as CD
import config
import imgTable
import ImgParser as IP

def downloadSet(picSet, picLoc, opener):
    pBkSl = re.compile("[/]")
    pQu = re.compile("[?]")
    errors = 0
    downloads = 0
    for picURL in picSet:
        for match in pQu.finditer(picURL):  # Remove everything after path to file
            index = match.start()
            picURL = picURL[0:index]
        for match in pBkSl.finditer(picURL):  # Get position of last occurance of '/'
            index = match.start()
        picName = picURL[index + 1:]
        picPath = picLoc + picName  # Add file name to file location
        try:
            if not imgTable.image_exists(picName): # os.path.exists(picPath):  # If file already exists, don't bother saving it again
                downloads += 1
                with opener.open(picURL) as response, open(picPath, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)  # Save response as file
                imgTable.add_row(picName, picURL, os.path.getsize(picPath), re.sub("/", "_", time.strftime("%x")), time.strftime("%X")) # Write file info to database
        except sqlite3.Error as e:
            print(e)
        except Exception as e:
            print(e)
            print("Error saving " + picPath)
            errors += 1
    if errors == 0:
        return True
    else:
        print("Error saving " + str(errors) + " of " + str(downloads) + " images.")
        return False

"""
Uses a string regular expression pattern to search
a given string.
"""
def searchWithPattern(regex, page):
    p = re.compile("(^http:|^https:)")
    picSet = set()
    for tup in regex.findall(page):  # Put obtained URL's in a list
        if re.match(p, tup[0]) is None:  # If no "http:" string is present, then add one
            print("Adding string \"http:\" to URL: " + tup[0])
            picSet.add("http:" + tup[0])
        else:
            picSet.add(tup[0])
    return picSet

"""
Print the help menu for the script.
"""
def print_help():
    print("-------------------------------------------------------------------------------")
    print("getPictures.py -x -f <folder> -s <method> --search-method <method>")
    print("\n-x: \n\tUse the -x flag to randomly set an image as desktop background\n\twithout downloading any from online.")
    print("\n-f <folder>:\n\tUse the -f flag to set the folder where images will be saved\n\tto and randomly selected from.")
    print("\n-s, --search-method:\n\tUse the -s or --search-method flags to set a url search method.\n\tValid search methods are: \"regex\" and \"html-parser\".")
    print("-------------------------------------------------------------------------------")

"""
Used to spoof User-Agent in requests
Avoid's those pesky 403 errors
FOR THE LOVE OF GOD, do not use to harass servers
"""
class MyOpener(URLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

if __name__ == "__main__":
    print("Running " + __file__ + " as main.")

    # Create access to config file
    CONFIG_FILE = "C:\\Users\\Steven\\Desktop\\config.xml"
    config = config.Config(CONFIG_FILE)

    # Configure command line arguments
    SHORT_ARGS = "hxf:s:"
    LONG_ARGS = ["hang", "help", "search-method="]
    SEARCH_METHODS = ["regex", "html-parser"]
    DOWN_FLAG = True
    FOLD_FLAG = False
    HANG_FLAG = False
    customFolder = ""
    searchMethod = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], SHORT_ARGS, LONG_ARGS)
    except getopt.GetoptError:
        print('Sur-Prise Mutha Fucka')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt == "-x":
            print("\nDownload flag has been set.")
            DOWN_FLAG = False
        elif opt == "-f":
            FOLD_FLAG = True
            customFolder = arg
        elif opt == "--hang":
            HANG_FLAG = True
        elif opt in ("-s", "--search-method"):
            searchMethod = arg
            print(searchMethod)


    folderloc = config.get_default("Folder")
    url = config.get_default("URL")
    if searchMethod is "":
        searchMethod = config.get_default("Search_Method")["value"]

    # Set download and read location to custom folder if -f <folder> option is used
    if FOLD_FLAG:
        fileloc = folderloc["value"] + customFolder + "\\"
    else:
        date = re.sub("/", "_", time.strftime("%x"))  # Get current date with format: 'MM_DD_YY'
        fileloc = folderloc["value"] + date + "\\"

    if not os.path.exists(fileloc):  # If file location does not exist, create it
        os.makedirs(fileloc)
        print("Created file location: \n" + fileloc)

    # Search for, and download images, if DOWN_FLAG is set
    if DOWN_FLAG:
        # Open URL and receive web-page
        myOpener = MyOpener()
        resp = myOpener.open(url["value"])
        data = resp.read()
        decode = data.decode("utf-8")

        # Use regular expressions to search for images
        if searchMethod == "regex":
            # List of patterns to search with
            patterns = []
            for pattern in config.get_patterns():
                patterns.append(re.compile(pattern, re.IGNORECASE))

            st = set()
            for p in patterns:
                picSet = searchWithPattern(p, decode)
                print("\nNumber of pictures found: " + str(len(picSet)))
                print(picSet)
                st = st.union(picSet)

            print("\nTotal number of pictures found : " + str(len(st)))
            print(st)

        # Use html parser to search for images
        elif searchMethod == "html-parser":
            # First pass to get html with relavent href=<image links>
            parser = IP.TwoPassURLParser()
            parser.feed(decode)
            temp = parser.text

            # Second pass to get list of image url's
            parser.clear()
            parser.set_round(2)
            parser.feed(temp)

            # get set of url's from parser
            st = set(parser.urlList)
            print(st)

        else:
            print("Invalid search method has been set. No search has been conducted.")
            st = set()

        downloadSet(st, fileloc, myOpener)

    file = CD.set_random_desktop(fileloc)

    print("\n" + "Set image as desktop background: " + file)

    # Useful for command line
    if HANG_FLAG:
        print("\nPress Enter/Return key to end program.")
        input()
