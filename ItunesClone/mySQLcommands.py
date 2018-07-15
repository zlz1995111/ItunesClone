from pymysql import*

def setupSQLconnector():
  conn = connect(host = "localhost",
               user = "root",
               password = "root",
               db = "ItunesClone")

  return conn

createPlaylist = "CREATE TABLE %s (SongName VARCHAR(50) NOT NULL,\
                              Duration VARCHAR(50) NULL,\
                              Artists VARCHAR(50) NOT NULL,\
                              Album VARCHAR(50) NOT NULL,\
                              Genre VARCHAR(50) NULL,\
                              PRIMARY KEY (SongName, Artists))"

createSongs = "CREATE TABLE Songs (SongName VARCHAR(50) NOT NULL,\
                              Duration VARCHAR(50) NULL,\
                              Artists VARCHAR(50) NOT NULL,\
                              Album VARCHAR(50) NOT NULL,\
                              Genre VARCHAR(50) NULL,\
                              PRIMARY KEY (SongName, Artists))"

createArtists = "CREATE TABLE Artists (Artists VARCHAR(50) NOT NULL,\
                                       AlbumNumber INT NULL,\
                                       SongNumber INT NULL,\
                                       PRIMARY KEY (Artists))"

createAlbums = "CREATE TABLE Albums (Album VARCHAR(50) NOT NULL,\
                                     ReleaseYear INT NULL,\
                                     PRIMARY KEY (Album))"

showTables = "SHOW TABLES FROM ItunesClone"

showSongs = "SHOW COLUMNS FROM Songs"
selectSongs = "SELECT * FROM Songs"

showArtists = "SHOW COLUMNS FROM Artists"
selectArtists = "SELECT * FROM Artists"

showAlbums = "SHOW COLUMNS FROM Albums"
selectAlbums = "SELECT * FROM Albums"

addToSong = "INSERT INTO Songs VALUES(%s, %s, %s, %s, %s)"
addToArtist = "INSERT INTO Artists VALUES(%s, %d, %d)"
addToAlbum = "INSERT INTO Albums VALUES(%s, %d)"

deleteSong = "DELETE FROM Songs WHERE SongName = %s"