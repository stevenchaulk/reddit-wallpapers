import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

class Config:

    PATTERN_LIST = [ \
        "((http:)?//i.imgur.com/[a-z0-9]*(.jpg|.png))", \
        "(https://i.redd.it/[a-z0-9]*(.jpg|.png))"]

    def __init__(self, location):
        self.config_file = location
        if not os.path.exists(self.config_file):
            print("Creating new config file at: " + self.config_file)
            self.create_config()
        self.config_root = ET.parse(self.config_file)

    def get_default(self, name, attribute=None):
        root = self.config_root
        if attribute == None:
            try:
                return {"value":root.find("Defaults").find(name).text, "bool":True}
            except:
                print("Incorrect name.")
                return {"value":"", "bool":False}
        else:
            try:
                return {"value":root.find("Defaults").find(name).get(attribute), "bool":True}
            except:
                print("Incorrect name or attribute.")
                return {"value":"", "bool": False}

    def get_patterns(self):
        root = self.config_root
        patternList = []
        for child in root.find("Patterns"):
            if child.get("use_flag") == "True":
                patternList.append(child.text)
        return patternList

    def create_config(self):
        root = ET.Element("Config_Head")

        defaults = ET.SubElement(root, "Defaults")
        folder = ET.SubElement(defaults, "Folder")
        folder.text = "C:\\Users\\Steven\\Pictures\\Downloaded_Pictures\\"
        url = ET.SubElement(defaults, "URL")
        url.text = "https://www.reddit.com/r/wallpapers/"

        patterns = ET.SubElement(root, "Patterns")
        for i in range(len(self.PATTERN_LIST)):
            pattern = ET.SubElement(patterns, "Pattern")
            pattern.set("id", str(i))
            pattern.set("use_flag", str(True))
            pattern.text = self.PATTERN_LIST[i]

        tree = ET.ElementTree(root)
        # print(ET.tostring(root, "utf-8"))
        print(minidom.parseString(ET.tostring(root, "utf-8")).toprettyxml())

        tree.write(self.config_file)

if __name__ == "__main__":
    print("Running " + __file__ + " as main.")
    CONFIG_FILE = "C:\\Users\\Steven\\Desktop\\config.xml"
    temp = Config(CONFIG_FILE)
    temp.create_config()