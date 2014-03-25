#coding=utf-8
import urllib.request
import urllib.parse
import re
from xml.dom import minidom


def deEncXiamiMusicLocation(encedLocation):
    # "4eyddnpwctored"
    # code + word
    encCode = int(encedLocation[0])
    encedWord = encedLocation[1:]

    # word per line:       "eydd"    "npw" "cto" "red"
    # length per line: len(3)+add(1)  len   len   len
    encLenPerLine = len(encedWord) // encCode
    encLenAddition = len(encedWord) % encCode

    # encedWordList = [
    #    "eydd",
    #    "npw",
    #    "cto",
    #    "red"
    # ]
    encedWordList = []
    for i in range(encCode):
        if i < encLenAddition:
            encedWordList.append(encedWord[i * (encLenPerLine + 1):
                                           (i + 1) * (encLenPerLine + 1)])
        else:
            encedWordList.append(encedWord[encLenAddition * (encLenPerLine + 1):]
                                 [(i - encLenAddition) * encLenPerLine:
                                  (i - encLenAddition + 1) * encLenPerLine])

    # URLList = [
    #    "e", "n", "c", "r", #encedWordList[0][0],[1][0],...
    #    "y", "p", "t", "e", #                [1]    [1]
    #    "d", "w", "o", "r",
    #    "d"
    # ]
    URLList = []
    for i in range(encLenPerLine):
        for m in range(encCode):
            URLList.append(encedWordList[m][i])
    for i in range(encLenAddition):
        URLList.append(encedWordList[i][encLenPerLine])

    # deEncedURL = "encryptedword"
    deEncedURL = urllib.parse.unquote("".join(URLList)).replace("^", "0")

    return deEncedURL


class XiamiMusicDetail:
    def __init__(self, musicID):
        self.musicID = musicID
        self.loaded = 0
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
        }
        self.xmlUrl = "http://www.xiami.com/song/playlist/id/%d/object_name/default/object_id/0"\
            % self.musicID
        self.headers['Referer'] = self.xmlUrl

    def loadDetail(self):
        self.xmlReq = urllib.request.Request(self.xmlUrl, headers=self.headers)
        self.xmlResponse = urllib.request.urlopen(self.xmlReq)
        self.xmlPage = self.xmlResponse.read().decode('utf-8')

        self.xmlDoc = minidom.parseString(self.xmlPage)
        self.title = self.xmlDoc.getElementsByTagName('title')[0].firstChild.data
        self.album_id = int(self.xmlDoc.getElementsByTagName('album_id')[0].firstChild.data)
        self.album_name = self.xmlDoc.getElementsByTagName('album_name')[0].firstChild.data
        self.artist = self.xmlDoc.getElementsByTagName('artist')[0].firstChild.data
        self.artist_url = self.xmlDoc.getElementsByTagName('artist_url')[0].firstChild.data
        self.pic = self.xmlDoc.getElementsByTagName('pic')[0].firstChild.data
        self.lyric = self.xmlDoc.getElementsByTagName('lyric')[0].firstChild.data
        self.location = self.xmlDoc.getElementsByTagName('location')[0].firstChild.data
        self.deEncedLocation = deEncXiamiMusicLocation(self.location)

        self.loaded = 1

if __name__ == "__main__":
    while 1:
        try:
            musicID = int(input('PLease enter the music ID of Xiami:\n'))
        except ValueError:
            print("Invalid ID.")

        try:
            musicDetail = XiamiMusicDetail(musicID)
            musicDetail.loadDetail()
            print("\n" + "-" * 80)
            print("Title: " + musicDetail.title)
            print("Album ID: " + str(musicDetail.album_id))
            print("Album Name: " + musicDetail.album_name)
            print("Artist: " + musicDetail.artist)
            print("Artist URL: " + musicDetail.artist_url)
            print("Picture: " + musicDetail.pic)
            print("Lyric: " + musicDetail.lyric)
            #print("Location(encrypted): " + musicDetail.location)
            print("Location: " + musicDetail.deEncedLocation)
            print("-" * 80 + "\n")
        except:
            print("Invalid ID or Network Error, Please try again.\n")
