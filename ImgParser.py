from urllib.request import URLopener
from html.parser import HTMLParser

class SpoofOpener(URLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

class TwoPassURLParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        HTMLParser.__init__(self)
        self.text = ""
        self.round = 1
        self.urlList = []

    def clear(self):
        self.clear_text()
        self.clear_urlList()

    def clear_urlList(self):
        self.urlList.clear()

    def clear_text(self):
        self.text = ""

    def set_round(self, num):
        self.round = num

    def handle_starttag(self, tag, attrs):
        if self.round == 1:
            if tag == "div" :
                for attr in attrs:
                    if attr[0] == "data-cachedhtml":
                        self.text += attr[1] + "\n"
        elif self.round == 2:
            if tag == "a":
                for attr in attrs:
                    if attr[0] == "href":
                        self.text += attr[1] + "\n"
                        self.urlList.append(attr[1])

            if tag == "iframe":
                for attr in attrs:
                    if attr[0] == "src":
                        self.text += attr[1] + "\n"
                        self.urlList.append(attr[1])

if __name__ == "__main__":
    print("Running " + __file__ + " as main.")

    # Open URL and receive web-page
    myOpener = SpoofOpener()
    resp = myOpener.open("https://www.reddit.com/r/wallpapers")
    data = resp.read()
    decode = data.decode("utf-8")

    parser = TwoPassURLParser()
    parser.feed(decode)
    temp = parser.text

    parser.clear()
    parser.set_round(2)
    parser.feed(temp)

    for url in parser.urlList:
        print(url)

