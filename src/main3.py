### Chris Tesoriero

from toolclasses3 import *

import os
import shutil
import eyed3
import sys
import time
from tkinter import *
import tkinter.filedialog

SONGS_FOLDER = None
EXPORT_FOLDER = None
SETTINGS = None
SONG_MANAGER = None
BMFOLDERS = None
MINI_MESSAGE = None

def main():
    print("Starting!...")
    global EXPORT_FOLDER
    # Start by finding the songs folder
    setSongsFolder()
    if (SONGS_FOLDER is None): # User hit Cancel
        print("No songs folder selected.")
    else:
        # Initial parse of the songs folder
        print("Using songs folder '" + SONGS_FOLDER + "'")
        print("Parsing Songs Folder, this may take some time...")
        parseSongsFolder()
    EXPORT_FOLDER = os.path.abspath("export")
    mainMenu()
    


def setSongsFolder(desc=False):
    global SONGS_FOLDER
    if desc:
        rtn = "Set songs folder"
        if not(SONGS_FOLDER is "n/a"):
            rtn += "; Currently '" + os.path.abspath(SONGS_FOLDER) + "'"
        return rtn
    
    if (os.path.isdir("C:\\Program Files (x86)\\osu!\\songs") and SONGS_FOLDER is "n/a"):
        sf = "C:\\Program Files (x86)\\osu!\\songs"
    else:
        root = Tk()
        root.withdraw()
        sf = tkinter.filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title="Please select your osu! songs folder")
        if (len(sf) == 0):
            sf = "n/a"
    SONGS_FOLDER = sf
    return True

def parseSongsFolder(desc=False):
    global SONG_MANAGER
    global BMFOLDERS, MINI_MESSAGE
    if desc:
        rtn = "Parse the current songs folder (Do this after changing the songs folder)"
        return rtn
    if (SONGS_FOLDER is "n/a"):
        sys.exit("Songs Folder not seleted")
    folderList = [os.path.join(SONGS_FOLDER, f) for f in os.listdir(SONGS_FOLDER)]
    BMFOLDERS = []
    for dir in folderList:
        if not os.path.isdir(dir):
            continue
        bmf = BMFolder(dir)
        if bmf.isValid():
            BMFOLDERS.append(bmf)
    SONG_MANAGER = SongManager(BMFOLDERS)
    MINI_MESSAGE = "Parsed folder '" + SONGS_FOLDER + "'"
    return True

def filterSongs(desc=False):
    global SONG_MANAGER
    global MINI_MESSAGE
    if desc:
        rtn = "Filter the current song list by keyword"
        return rtn
    print("Okay, give me the keyword to filter by (This uses REGEX!)")
    usrin = input("keyword: ").strip()
    SONG_MANAGER.filterSongs(usrin)
    MINI_MESSAGE = "Filtered songs by keyword '%s'\nThere are now %i songs selected." % (usrin, SONG_MANAGER.getNumSongs())
    return True
    
def resetFilterSongs(desc=False):
    global SONG_MANAGER
    global MINI_MESSAGE
    if desc:
        rtn = "Resets the current song filter if there is one"
        return rtn
    SONG_MANAGER.unfilterSongs()
    MINI_MESSAGE = "Unfiltered Songs. There are now %i songs selected." % (SONG_MANAGER.getNumSongs())
    return True

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

def changeExportFolder(desc=False):
    global EXPORT_FOLDER
    global MINI_MESSAGE
    if desc:
        rtn = "Change the export folder; Currently '" + os.path.abspath(EXPORT_FOLDER) + "'"
        return rtn
    root = Tk()
    root.withdraw()
    ef = tkinter.filedialog.askdirectory(parent=root, initialdir=os.getcwd(), title="Please select the folder you wish to export to")
    EXPORT_FOLDER = ef
    return True
    
def exportSongs(desc=False):
    global MINI_MESSAGE
    if desc:
        rtn = "Export all currently selected songs"
        return rtn
    if (EXPORT_FOLDER is None or SONG_MANAGER is None):
        MINI_MESSAGE = "Missing Export Folder or Song Manager"
        return True
    print("\nThis will attempt to export %i songs to the directory %s" % (SONG_MANAGER.getNumSongs(), EXPORT_FOLDER))
    memReq = (SONG_MANAGER.getTotalFileSize() / 1024.0) / 1024.0
    print("This is going to require %d.04 MB" % memReq)
    print("\nIs this okay?\n1) Yes it is, go for it!\n2) No! Don't do it!")
    confirm = userChoice([1,2])
    if (int(confirm) == 2):
        MINI_MESSAGE = "Did not export songs!"
        return True
    if not(os.path.isdir(EXPORT_FOLDER)):
        os.mkdir("export")
    print("Alright, I'm going to start.")
    time.sleep(1.500)
    print("A bunch of scary warnings are probably going to pop up, this is pretty much expected.")
    time.sleep(2.000)
    print("osu! song files are -very- diverse in what condition their audio files are in,")
    time.sleep(3.000)
    print("I'm going to export everything as well as I can, but I'm going to prioritize not crashing!")
    time.sleep(3.500)
    print("Here it goes,")
    time.sleep(1)
    print("3...")
    time.sleep(1.000)
    print("2...")
    time.sleep(1.000)
    print("1...")
    time.sleep(1.000)
    
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
            print("Unicode Error with file %s, cannot properly edit file." % os.path.basename(exported))
            continue
        if audiofile is None:
            print("Could not edit tags for %s, because it is not a supported file type!" % os.path.basename(exported))
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
        filetag.album = ("osu! folder")
        filetag.artist = str(song.getArtist())
        filetag.title = str(song.getTitle())
        filetag.track_num = (counter, None)
        filetag.save()
        counter += 1
    MINI_MESSAGE = "Finished exporting songs!"
    return True

def done(desc=False):
    if desc:
        rtn = "Exit"
        return rtn
    sys.exit("User Quit")
def fallthru(desc=False):
    if desc:
        rtn = "Back"
        return rtn
    return False

def menu(choices, header, clear=True):
    global MINI_MESSAGE
    print("")
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    for toprint in header:
        print(toprint)
    if (MINI_MESSAGE is not None):
        print(MINI_MESSAGE)
        MINI_MESSAGE = None
    for n in range(len(choices)):
        print("%i) %s" % (n+1, choices[n](True)))
    
    choice = userChoice([x + 1 for x in range(len(choices))])
    return choices[int(choice)-1]()

def mainMenu(desc=False):
    if desc:
        rtn = "Main Menu"
        return rtn
    
    
    choices = [exportSongs, exportConfigMenu, done]
    header = ["=== Main Menu ===", "Using songs folder '%s'\nContaining %i Song Folders, with a total of %i beatmaps for %i songs" % \
            (SONGS_FOLDER, len(BMFOLDERS), sum([len(bmf.getBeatmaps()) for bmf in BMFOLDERS]), SONG_MANAGER.getNumSongs())]
    menu(choices,header,False)
    while True:
        header = ["=== Main Menu ===", "Using songs folder '%s'\nContaining %i Song Folders, with a total of %i beatmaps for %i songs" % \
            (SONGS_FOLDER, len(BMFOLDERS), sum([len(bmf.getBeatmaps()) for bmf in BMFOLDERS]), SONG_MANAGER.getNumSongs())]
        menu(choices, header)
    return

def exportConfigMenu(desc=False):
    if desc:
        rtn = "Song Export Options"
        return rtn
    
    header = ["=== Export Options Menu ==="]
    
    choices = [setSongsFolder, parseSongsFolder, filterSongs, resetFilterSongs, changeExportFolder, fallthru]
    
    while menu(choices, header):
        pass

main()
print("Ended")