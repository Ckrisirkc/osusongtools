#class Test:
#	def __init__(self, a, b):
#		self.x = a
#		self.y = b
#	def __str__(self):
#		return "("+str(self.x)+","+str(self.y)+")"
#	def __add__(self, other):
#		return Test(self.x + other.x, self.y + other.y)

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

class BMFolder:
    def __init__(self, folder):
        self.folder = folder
        self.songs = set()
        for file in os.listdir(folder):
            if ".osu" in os.path.splitext(file)[1].lower():
                getInfoFromFile(file)
			
    def getInfoFromFile(file):
        reader = open(file, 'r')
        for line in reader:
            if line.startswith("AudioFilename"):
                #print("Line: %s"  % line)
                songPath = line[line.index(":")+1:].strip()
            if line.startswith("Title"):
                songTitle = line[line.index(":")+1:].strip()
            if line.startswith("Artist"):
                songArtist = line[line.index(":")+1:].strip()
        if songPath is None:
            return
        song = BMSong(songPath)
        if song in self.songs:
            return