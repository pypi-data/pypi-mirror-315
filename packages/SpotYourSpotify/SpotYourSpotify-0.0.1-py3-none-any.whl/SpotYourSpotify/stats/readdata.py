import pandas as pd
import random

class ReadCsvError(Exception):
    pass

class Playlist():
    """
    A class for playlist managing and interaction.

    The Question class loads the playlist data from a user's CSV file. It allows access to the data
    including functions to fetch specific songs and its corresponding attributes. 

    Parameters
    ----------
    filename : str
        The name (or path) of the CSV file (without the .csv extension) containing the playlist data

    Attributes
    ----------
    filename : str
        Name (or path) of the CSV file (without the .csv extension) that containes the playlist data.
    table : pandas.DataFrame
        The pandas DataFrame that contains the playlist data.
    length : int
        Total number of songs (rows) in the playlist.
    ids : pandas.Series
        Unique identifiers (Track ID) of songs in the playlist
    tracks : pandas.Series
        The title(s) of the song(s) in the playlist.
    albums : pandas.Series
        The album(s) of the song(s) in the playlist.
    artists : pandas.Series
        The artist name(s) of the song(s) in the playlist.
    releases : pandas.Series
        The release date(s) of the song(s) in the playlist.
    durations : pandas.Series
        The duration (millisecond) of the song(s) in the playlist.
    genres : pandas.Series
        The genres of the song(s) in the playlist.
    labels : pandas.Series
        The record label that publishes the song(s) in the playlist.
    tempos : pandas.Series
        The tempo (BPM) of the song(s) in the playlist.

    Methods
    -------
    showtable():
        Prints the playlist table.
    getSong(index):
        Fetch a song data from the playlist at a specified index.
    getSongId(id):
        Fetch a song data from the playlist by a specified id. 
    randSong():
        Returns a random song from the playlist.
    """
    
    def __init__(self, filename):
        try:
            self.filename = filename
        except:
            print("No filename to get playlist from!")
            raise
        try:
            self.__df = pd.read_csv(filename + ".csv")
        except:
            print("Something went wrong reading the playlist into a dataframe!")
            raise ReadCsvError

    def showtable(self):
        """Prints the playlist data as a table,"""
        print(self.__df)

    @property
    def table(self):
        """Returns the playlist data as a pandas DataFrame,"""
        return (self.__df)

    @property
    def length(self):
        """Returns the number of rows (total number of songs) in the playlist data"""
        return len(self.__df)
    
    @property
    def ids(self):
        """Returns a series of unique Track ID of the song(s)."""
        return self.__df["Track ID"].dropna()
    
    @property
    def tracks(self):
        """Returns a series of song title."""
        return self.__df["Track Name"].dropna()
    
    @property
    def albums(self):
        """Returns a series of album names."""
        return self.__df["Album Name"].dropna()
    
    @property
    def artists(self):
        """Returns a series of artist names"""
        return self.__df["Artist Name(s)"].dropna()
    
    @property
    def releases(self):
        """Returns a series of song release dates"""
        return self.__df["Release Date"].dropna()
    
    @property
    def durations(self):
        """Returns a series of song durations in milliseconds"""
        return self.__df["Duration (ms)"].dropna()
    
    @property
    def genres(self):
        """Returns a series of song genres."""
        return self.__df["Genres"].dropna()
    
    @property
    def labels(self):
        """Returns a series of record labels."""
        return self.__df["Record Label"].dropna()
    
    @property
    def tempos(self):
        """Returns a series of song tempo (BPM)."""
        return self.__df["Tempo"]
    
    def getSong(self, index):
        """Fetch song data in the playlist at a specified index.
        
        Parameters
        ----------
        index: int
            The index of the song to fetch.
            
        Returns
        -------
        pandas.Series
            The row of dataframe corresponding to the song data.
        """
        return self.__df.iloc[index]
    
    def getSongId(self, id):
        """Fetch a song data from the playlist by a specified id. 
        
        Parameters
        ----------
        id : str
            The Track ID of the song.
            
        Returns
        -------
        pandas.Series
            The row of dataframe corresponding to the song data.
        """
        if id in self.__df["Track ID"].values:
            return self.__df[self.__df["Track ID"] == id].iloc[0]
    
    def randSong(self):
        """Returns a random song from the playlist.
        
        Returns
        -------
        pandas.Series
            The row of dataframe corresponding to the song data.
        """
        rand = random.randint(0, self.length)
        return self.getSong(rand)
    
class Song():
    """
    A class for managing and interacting a single song in the playlist.
    
    The Song class is initialized with a playlist object and optional identifier (index or Track ID). 
    A random song is selected if the optional identifier is not provided.
    
    Parameters
    ----------
    pl: Playlist
        The playlist object that contains the playlist data.
    id : int, str, optional
        The index or Track ID of the song. If not provided, a random song is chosen.
        
    Attributes
    ----------
    id : str
        The Track ID of the song.
    track : str
        The title of the song.
    album : str
        The name of the album of the song.
    artist : str
        The artist who performed the song.
    release : str
        The release date of the song.
    duration : int
        The duration of the song in milliseconds.
    genre : str
        The genre of the song.
    label : str
        THe record label that publisehd the song.
    tempo : float
        THe tempo of the song in BPM.
    
    Methods
    -------
    None
    """
    def __init__(self, pl, id = None):
        if isinstance(id, int):
            self.__song = pl.getSong(id)
        elif isinstance(id, str):
            self.__song = pl.getSongId(id)
        else:
            self.__song = pl.randSong()

    @property
    def id(self):
        """Returns the Track ID of the song."""
        return self.__song["Track ID"]
    
    @property
    def track(self):
        """Returns the title of the song."""
        return self.__song["Track Name"]
    
    @property
    def album(self):
        """"Returns the album name of the song."""
        return self.__song["Album Name"]
    
    @property
    def artist(self):
        """Returns the artist who performed the song."""
        return self.__song["Artist Name(s)"]
    
    @property
    def release(self):
        """Returns the release date of the song."""
        return self.__song["Release Date"]
    
    @property
    def duration(self):
        """Returns the duration of the song in milliseconds."""
        return self.__song["Duration (ms)"]
    
    @property
    def genre(self):
        """Returns the genre of the song."""
        return self.__song["Genres"]
    
    @property
    def label(self):
        """Returns the record label that published the song."""
        return self.__song["Record Label"]
    
    @property
    def tempo(self):
        """Returns the tempo of the song in BPM"""
        return self.__song["Tempo"]