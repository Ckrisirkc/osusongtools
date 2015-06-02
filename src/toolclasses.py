import os
import re

class BMSong:
    def __init__(self, fileName):
        self.fileName = fileName
        self.artist = ""
        self.title = ""
        self.tags = set()
    def __eq__(self, other):
        return (self.fileName == other.fileName)
    def __ne__(self, other):
        return (self.fileName != other.fileName)
    def __hash__(self):
        return hash(self.fileName)
    def __str__(self):
        return ("%s - %s - %s" % (self.artist, self.title, self.fileName))
    def setArtist(self, artist):
        self.artist = artist
    def setTitle(self, title):
        self.title = title
    def getFileName(self):
        return self.fileName
    def getArtist(self):
        return self.artist
    def getTitle(self):
        return self.title
    def getSize(self):
        return os.path.getsize(fileName)
    def search(self, keyword):
        return (re.search(keyword, self.Title, re.IGNORECASE) or re.search(keyword, self.Artist, re.IGNORECASE))

class BMFolder:
    def __init__(self, folder):
        self.folder = folder
        self.songs = set()
        self.beatmaps = set()
        for file in os.listdir(folder):
            if ".osu" in os.path.splitext(file)[1].lower():
                filep = os.path.join(folder, file)
                self.beatmaps.add(filep)
                self.getInfoFromFile(filep)
    def getInfoFromFile(self, file):
        reader = open(file, 'r')
        for line in reader:
            if line.startswith("AudioFilename"):
                #print("Line: %s"  % line)
                songPath = os.path.join(self.folder, line[line.index(":")+1:].strip())
            if line.startswith("Title:"):
                songTitle = line[line.index(":") + 1:].strip()
            if line.startswith("Artist:"):
                songArtist = line[line.index(":") + 1:].strip()
        if songPath is None:
            return
        song = BMSong(songPath)
        if song in self.songs:
            return
        song.setArtist(songArtist)
        song.setTitle(songTitle)
        self.songs.add(song)
    def __str__(self):
        return ("%s, %s Beatmaps for %s song" % (self.folder, len([name for name in os.listdir(self.folder) if "osu" in os.path.splitext(name)[1].lower()]), len(self.songs)))
    def getSongs(self):
        return self.songs
    def getBeatmaps(self):
        return self.beatmaps
    def isValid(self):
        return (len(self.songs) > 0)

class SongManager:
    def __init__(self, bmfolders):
        self.songs = [individualsong for bmfolder in bmfolders for individualsong in list(bmfolder.getSongs()) if os.path.isfile(individualsong.getFileName())] # This makes my head hurt. Get a list of all songs from all BMFolders in bmfolders
        self.selected = list(self.songs)
    def filterSongs(self, keyword):
        self.selected = [match for song in self.songs if song.search(keyword)]
        # equivalent code below --
        #for song in self.songs:
        #    if song.search(keyword):
        #        self.selected.add(song)
    def unfilterSongs(self):
        self.selected = list(self.songs)
    def getNumSongs(self, allSongs=False):
        songlist = self.songs if allSongs else self.selected
        return len(songlist)
    def getTotalFileSize(self, allSongs=False):
        songlist = self.songs if allSongs else self.selected
        return sum([song.getSize() for song in songlist])
    def getSongs(self, allSongs=False):
        songlist = self.songs if allSongs else self.selected
        return songlist

    
def userChoice(choices=None):
    usrin = raw_input("Enter Option: ").strip()
    if (choices is None):
        return usrin
    while (not(usrin.lower() in [str(x).lower() for x in choices])):
        print "Invalid Option {%s}" % usrin
        print "Avilable Options: ",
        for x in choices:
            print x,
        usrin = raw_input("Enter Option: ").strip()
    return usrin
        