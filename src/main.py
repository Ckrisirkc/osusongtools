### Chris Tesoriero
import os
import shutil
import eyed3

#from eyed3.id3 import Tag
#from sys import exit


# returns the Mp3 file name from an .osu file
def getMp3FileName(file):
	reader = open(file, 'r')
	for line in reader:
		if line.startswith("AudioFilename"):
			#print("Line: %s"  % line)
			return line[line.index(":")+1:].strip()
	return "Not Found"

def donothing():
	pass
    
# returns the Mp3 file names from an osu! song folder
def getMp3Names(directory):
	names = []
	for f in os.listdir(directory):
		#print("dir %s" % f) if os.path.isdir(f) else donothing()
		if ".osu" in os.path.splitext(f)[1].lower():
			names.append(getMp3FileName(os.path.join(directory,f)))
	return list(set(names))
#print(os.path.join(os.getcwd(), "songs")) if os.path.isdir("songs") else print("no")
#print(getMp3Names("C:\\Users\\Chris\\Documents\\CS\\151878 Chasers - Lost"))

if not(os.path.isdir("songs")):
	exit("No songs")
if not(os.path.isdir("extracted")):
	os.mkdir("extracted")

#songTags = dict()

songsFolder = os.path.join(os.getcwd(), "songs")
folderList = [os.path.join(songsFolder, f) for f in os.listdir(songsFolder)]
for dir in folderList:
	if not os.path.isdir(dir):
		continue
	songPaths = [os.path.join(dir, song) for song in getMp3Names(dir)]
	for song in songPaths:
		shutil.copy(song, "extracted")
        audiofile = eyed3.load(os.path.join("extracted", song))
        audiofile.tag.album = (u"osu! folder")
        audiofile.tag.save()