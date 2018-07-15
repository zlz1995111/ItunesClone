# itunesClone.py
# @author Xuliang Sun
# @author Lizhi Zhao
################################################################################
import os
import string
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from pymysql import*
from mySQLcommands import*

# initialize database only once ################################################
conn = setupSQLconnector()
cur = conn.cursor()

def userInit(cur):
  cur.execute(showTables)
  rows = cur.fetchall()
  if not rows:
    cur.execute(createSongs)
    cur.execute(createArtists)
    cur.execute(createAlbums)
  conn.commit()
userInit(cur)


playList = []

win = tk.Tk()
win.title("Itunes Clone")
win.resizable(0,0)
win.iconbitmap(r"/Users/xuliangsun/Desktop/itunesClone.ico")

# Create a container
library = ttk.LabelFrame(win, text = "Library")
library.grid(column = 0, row = 1)


# Create a Tab Control ########################################################
tabControl = ttk.Notebook(library, width = 900, height = 450)

tab0 = ttk.Frame(tabControl)
tabControl.add(tab0, text = "Player")

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text = 'Songs')

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text = 'Albums')

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text = "Artists")

tabControl.pack(expand = 1, fill = "both") # Pack to make visible

# Creata Player Panel to hold ##################################################
def play():
  pass

  
playerPanel = ttk.LabelFrame(tab0)
playerPanel.grid(column = 0, row = 0, ipadx = 8, ipady = 4)
  
playerLabel = ttk.Label(playerPanel, text = "Playlists")
playerLabel.grid(column = 0, row = 0, sticky = tk.W)

playListBox = tk.Listbox(playerPanel, width = 50, height = 20)
playListBox.grid(column = 0, row = 1, sticky = tk.W)

playButton = tk.Button(playerPanel, text = "Play", command = play)
playButton.grid(row = 4, column = 0, sticky = tk.W, pady = 5)


def addToPlayer(song, playListBox):
  for i in range(len(song)):
    item = song[i]
    print(item[0], item[1], item[1])
    #cur.execute(addToSong, (item[0], "", item[1], item[2], ""))
    conn.commit()
    playListBox.insert(i + 1, item[0])


# CITATION: directoryChooser() from https://pastebin.com/t8KMexkp ##############
listOfSongs = []
songAttributes = []
index = 0
def directoryChooser():
  directory = askdirectory()
  os.chdir(directory)

  for file in os.listdir(directory):
    if file.endswith(".mp3"):
      realdir = os.path.realpath(file)
      audio = ID3(realdir)
      songAttributes.append((audio["TIT2"].text[0],
                             audio["TPE1"].text[0],
                             audio["TALB"].text[0]))
      listOfSongs.append(file)
  addToPlayer(songAttributes, playListBox)
  pygame.mixer.init()
  pygame.mixer.music.load(listOfSongs[0])
  pygame.mixer.music.play(-1)

def nextsong():
  global index
  index += 1
  pygame.mixer.music.load(listOfSongs[index])
  pygame.mixer.music.play()

def prevsong():
  global index
  index -= 1
  pygame.mixer.music.load(listOfSongs[index])
  pygame.mixer.music.play()

prevButton = tk.Button(playerPanel, text = "Prev", command = prevsong)
prevButton.grid(row = 4, column = 0, pady = 5)

nextButton = tk.Button(playerPanel, text = "Next", command = nextsong)
nextButton.grid(row = 4, column = 0, pady = 5, sticky = tk.E)

###############################################################################
def addPlaylist():
  cur.execute(addToSong,(songname.get(), duration.get(), 
                         artist.get(), album.get(), 
                         genre.get()))
  conn.commit()
  songnameEntered.delete(0, 'end')
  artistEntered.delete(0, 'end')
  durationEntered.delete(0, 'end')
  albumEntered.delete(0, 'end')
  genreEntered.delete(0, 'end')

subPanel = ttk.LabelFrame(tab0)
subPanel.grid(column = 1, row = 0, ipadx = 8, ipady = 4, sticky = tk.N)

SongnameLabel = ttk.Label(subPanel, text = "Song title")
SongnameLabel.grid(column = 1, row = 0, sticky = tk.W)
# Adding a Textbox Entry
songname = tk.StringVar()
songnameEntered = ttk.Entry(subPanel, width = 20, textvariable = songname)
songnameEntered.grid(column = 1, row = 1, sticky = tk.N)


artistLabel = ttk.Label(subPanel, text = "Artist name")
artistLabel.grid(column = 1, row = 2, sticky = tk.W)
# Adding a Textbox Entry
artist = tk.StringVar()
artistEntered = ttk.Entry(subPanel, width = 20, textvariable = artist)
artistEntered.grid(column = 1, row = 3, sticky = tk.N)

durationLabel = ttk.Label(subPanel, text = "Duration")
durationLabel.grid(column = 1, row = 4, sticky = tk.W)
# Adding a Textbox Entry
duration = tk.StringVar()
durationEntered = ttk.Entry(subPanel, width = 20, textvariable = duration)
durationEntered.grid(column = 1, row = 5, sticky = tk.N)

albumLabel = ttk.Label(subPanel, text = "Album name")
albumLabel.grid(column = 1, row = 6, sticky = tk.W)
# Adding a Textbox Entry
album = tk.StringVar()
albumEntered = ttk.Entry(subPanel, width = 20, textvariable = album)
albumEntered.grid(column = 1, row = 7, sticky = tk.N)

genreLabel = ttk.Label(subPanel, text = "Genre")
genreLabel.grid(column = 1, row = 8, sticky = tk.W)
# Adding a Textbox Entry
genre = tk.StringVar()
genreEntered = ttk.Entry(subPanel, width = 20, textvariable = genre)
genreEntered.grid(column = 1, row = 9, sticky = tk.N)

#Adding a Button
add = ttk.Button(subPanel, text = "Add", command = addPlaylist)
add.grid(column = 1, row = 10, pady = 10, sticky = tk.W)

subPanel2 = ttk.LabelFrame(tab0)
subPanel2.grid(column = 2, row = 0, sticky = tk.N)
searchLabel = ttk.Label(subPanel2, text = "Search")
searchLabel.grid(column = 2, row = 0, padx = 10, sticky = tk.W)

def searchKey():
  results.delete(0, "end")
  cur.execute(showTables)
  cur.execute(showSongs)
  cur.execute(selectSongs)
  songtable = cur.fetchall()
  print(keyword.get())
  if keyword.get() != "":
    for row in range(len(songtable)):
      for col in range(len(songtable[0])):
        if keyword.get().lower() in songtable[row][col].lower():
          results.insert(1, songtable[row][col])

# Adding a Search Entry
keyword = tk.StringVar()
keywordEntered = ttk.Entry(subPanel2, width = 20, textvariable = keyword)
keywordEntered.grid(column = 2, row = 1, padx = 10, sticky = tk.W)

searchButton = ttk.Button(subPanel2, text = "Search", command = searchKey)
searchButton.grid(column = 3, row = 1, sticky = tk.W)

results = tk.Listbox(subPanel2, width = 20, height = 10)
results.grid(column = 2, row = 2)


# Creata Song Panel to hold ###################################################
def loadSongData():
  songTree.delete(*songTree.get_children())
  cur.execute(showTables)
  cur.execute(showSongs)
  cur.execute(selectSongs)
  rows = cur.fetchall()
  for i in range(len(rows)):
    row = rows[i]
    songTree.insert("", i, text = row[0], values = row[1:])

def getFocusItem(event):
  curItem = songTree.focus()
  songDic = songTree.item(curItem)
  selectedSong = songDic['text']
  cur.execute(deleteSong, selectedSong)
  conn.commit()

songPanel = ttk.LabelFrame(tab1)
songPanel.grid(column = 0, row = 0, padx = 8, pady = 4)

songLabel = ttk.Label(songPanel, text = "Songs")
songLabel.grid(column = 0, row = 0, sticky = tk.W)

songTree = ttk.Treeview(songPanel)
songTree.grid(column = 0, row = 1, sticky = tk.W)
songTree["columns"] = ("one", "two", "three", "four", "five")
songTree.column("one", width = 120)
songTree.column("two", width = 120)
songTree.column("three", width = 120)
songTree.column("four", width = 120)
songTree.column("five", width = 120)
songTree.heading("one", text = "Time")
songTree.heading("two", text = "Artist")
songTree.heading("three", text = "Album")
songTree.heading("four", text = "Genre")
songTree.heading("five", text = "Year")

load = ttk.Button(songPanel, text = "Load", command = loadSongData)
load.grid(column = 0, row = 2, ipady = 4, pady = 8, sticky = tk.W)

songTree.bind("<Button-2>", getFocusItem)
# Create Album Panel to hold ###################################################
def loadAlbumData():
  albumTree.delete(*albumTree.get_children())
  cur.execute(showTables)
  cur.execute(showAlbums)
  cur.execute(selectAlbums)
  rows = cur.fetchall()
  for i in range(len(rows)):
    row = rows[i]
    albumTree.insert("", i, text = row[0], values = row[1:])

albumPanel = ttk.LabelFrame(tab2)
albumPanel.grid(column = 0, row = 0, padx = 8, pady = 4)

albumLabel = ttk.Label(albumPanel, text = "Albums")
albumLabel.grid(column = 0, row = 0, sticky = tk.W)

load = ttk.Button(albumPanel, text = "Load", command = loadAlbumData)
load.grid(column = 0, row = 2, ipady = 4, pady = 8, sticky = tk.W)

albumTree = ttk.Treeview(albumPanel)
albumTree.grid(column = 0, row = 1, sticky = tk.W)
albumTree["columns"] = ("one", "two", "three")
albumTree.column("one", width = 200)
albumTree.column("two", width = 200)
albumTree.column("three", width = 200)
albumTree.heading("one", text = "Album")
albumTree.heading("two", text = "Artist")
albumTree.heading("three", text = "Year")


# Create Artist Panel to hold ##################################################
def loadArtistData():
  artistTree.delete(*artistTree.get_children())
  cur.execute(showTables)
  cur.execute(showArtists)
  cur.execute(selectArtists)
  rows = cur.fetchall()
  for i in range(len(rows)):
    row = rows[i]
    artistTree.insert("", i, text = row[0], values = row[1:])

artistPanel = ttk.LabelFrame(tab3, text = "Artists")
artistPanel.grid(column = 0, row = 0, padx = 8, pady = 4)

artistLabel = ttk.Label(artistPanel, text = "Albums")
artistLabel.grid(column = 0, row = 0, sticky = tk.W)

load = ttk.Button(artistPanel, text = "Load", command = loadArtistData)
load.grid(column = 0, row = 2, ipady = 4, pady = 8, sticky = tk.W)

artistTree = ttk.Treeview(artistPanel)
artistTree.grid(column = 0, row = 1, sticky = tk.W)

artistTree["columns"] = ("one", "two")
artistTree.column("one", width = 300)
artistTree.column("two", width = 300)
artistTree.heading("one", text = "Artist")
artistTree.heading("two", text = "Song")

# Add a new song
def addNewSong():
  songname = input('please input the song name:')
  duration = input('please input the duration:')
  artist = input('please input the artist:')
  album = input('please input the album:')
  genre = input('please input the genre:')
  releaseyear = input('please input the release year:')
  cur.execute(addToSong,(songname, duration, artist, album, genre))
  cur.execute(addToAlbum,(album,releaseyear))
  conn.commit()
  print("Hello")

def createRelatedTable(tab):
    pass

# Create a new playlist
playListCount = 0
def createNewPlayList():
    global playListCount
    playListCount += 1
    tab = ttk.Frame(tabControl)
    tabControl.add(tab, text = "Playlist%d"%playListCount)
    createRelatedTable(tab)

def deleteFromPlaylist():
    pass

# Creating a Menu Bar ##########################################################
# Exit GUI cleanly
def quit():
    win.quit()
    win.destroy()
    cur.close()
    conn.close()
    exit()

menuBar = Menu(win)
win.config(menu=menuBar)

# Add menu items
fileMenu = Menu(menuBar, tearoff = 0)
menuBar.add_cascade(label = "File", menu = fileMenu)
newMenu = Menu(fileMenu, tearoff  = 0)
fileMenu.add_cascade(label = "New", menu = newMenu)
newMenu.add_command(label = "Playlist", command = createNewPlayList)
fileMenu.add_command(label = "Open", command = directoryChooser)
fileMenu.add_command(label = "Exit", command = quit)
fileMenu.add_separator()
fileMenu.add_command(label = "Add to Library", command = addNewSong)

# Add another Menu to the Menu Bar and an item
helpMenu = Menu(tabControl, tearoff = 0)
helpMenu.add_command(label = "About")
menuBar.add_cascade(label = "Help", menu = helpMenu)

# create a pop-up menu
popup = Menu(win, tearoff = 0)
popup.add_command(label = "Delete from Library", command = deleteFromPlaylist)

def doPopup(event):
    # display the popup memu
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab
        popup.grab_release()
tabControl.bind("<Button -2>", doPopup)

win.mainloop()