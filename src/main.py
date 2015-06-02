### Chris Tesoriero

from toolclasses import *

import os
import shutil
import eyed3
import sys

SONGS_FOLDER = None
EXPORT_FOLDER = None
SETTINGS = None
SONG_MANAGER = None
BMFOLDERS = None

def main():
    global EXPORT_FOLDER
    # Start by finding the songs folder
    setSongsFolder()
    # Initial parse of the songs folder
    parseSongsFolder()
    if not(os.path.isdir("export")):
        os.mkdir("export")
    EXPORT_FOLDER = os.path.abspath("export")
    mainMenu()
    


def setSongsFolder(desc=False):
    global SONGS_FOLDER
    if desc:
        rtn = "Set songs folder"
        if (SONGS_FOLDER == None):
            rtn += " Currently '" + os.path.abspath(SONGS_FOLDER)
        return rtn
    if not(os.path.isdir("songs")):
        sys.exit("No songs")
    SONGS_FOLDER = os.path.join(os.getcwd(), "songs")
    return

def parseSongsFolder(desc=False):
    global SONG_MANAGER
    global BMFOLDERS
    if desc:
        rtn = "Parse the current songs folder"
        return rtn
    if (SONGS_FOLDER == None):
        sys.exit("Songs Folder None")
    folderList = [os.path.join(SONGS_FOLDER, f) for f in os.listdir(SONGS_FOLDER)]
    BMFOLDERS = []
    for dir in folderList:
        if not os.path.isdir(dir):
            continue
        bmf = BMFolder(dir)
        if bmf.isValid():
            BMFOLDERS.append(bmf)
    SONG_MANAGER = SongManager(BMFOLDERS)
    return

def cprn(file, name):
    fileName = os.path.basename(file)
    ext = os.path.splitext(fileName)[1]
    if (ext == ""):
        ext = os.path.splitext(".mp3")[0]
    newFile = os.path.join(EXPORT_FOLDER, fileName)
    counter = 0
    while(os.path.isfile(newFile)):
        newFile = os.path.join(EXPORT_FOLDER, os.path.splitext(fileName)[0] + str(counter) + os.path.splitext(fileName)[1])
        counter += 1
    shutil.copy(file, newFile)
    counter = 0
    rname = name + ext
    while (os.path.isfile(os.path.join(EXPORT_FOLDER, rname))):
        rname = name + str(counter) + ext
        counter += 1
    os.rename(newFile, os.path.join(EXPORT_FOLDER, rname))
    return os.path.join(EXPORT_FOLDER, rname)

def exportSongs(desc=False):
    if desc:
        rtn = "Export all currently selected songs"
        return rtn
    counter = 1
    for song in SONG_MANAGER.getSongs():
        #os.rename(filename, newfilename)
        name = song.getArtist() + "-" + song.getTitle()
        name = name.replace(" ", "_")
        valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        name = ''.join(c for c in name if c in valid_chars)
        exported = cprn(song.getFileName(), name)
        try:
            audiofile = eyed3.load(exported)
        except UnicodeDecodeError:
            print "Unicode Error with file %s, cannot properly edit file." % os.path.basename(exported)
            continue
        if audiofile is None:
            print "Could not edit tags for %s, because it is not a supported file type!" % os.path.basename(exported)
            continue
        filetag = audiofile.tag
        if filetag is None:
            filetag = eyed3.id3.Tag()
            filetag.file_info = eyed3.id3.FileInfo(exported)
            filetag.version = (2,3,0)
        else:
            filetag.clear()
            filetag.file_info = eyed3.id3.FileInfo(exported)
            filetag.version = (2,3,0)
        filetag.album = (u"osu! folder")
        filetag.artist = unicode(song.getArtist())
        filetag.title = unicode(song.getTitle())
        filetag.track_num = (counter, None)
        filetag.save()
        counter += 1

def done(desc=False):
    if desc:
        rtn = "Exit"
        return rtn
    sys.exit("User Quit")
def fallthru(desc=False):
    if desc:
        rtn = "Back"
    pass

def menu(choices, header):
    os.system('cls' if os.name == 'nt' else 'clear')
    for toprint in header:
        print toprint
    for n in range(len(choices)):
        print "%i) %s" % (n+1, choices[n](True))
    choice = userChoice([x + 1 for x in range(len(choices))])
    choices[int(choice)-1]()
    
def mainMenu(desc=False):
    if desc:
        rtn = "Main Menu"
        return rtn
    
    header = "Using songs folder '%s'\nContaining %i Song Folders, with a total of %i beatmaps for %i songs" % \
        (SONGS_FOLDER, len(BMFOLDERS), sum([len(bmf.getBeatmaps()) for bmf in BMFOLDERS]), SONG_MANAGER.getNumSongs())
    choices = [exportSongs, done]
    while True:
        menu(choices, [header])

main()
print "Ended"