import pandas as pd
from . import readdata as rd

def toMins(ms):
    """
    Converts millisecond to minutes as a formatted string mm min ss seconds.
    
    Parameters
    ----------
    ms : int
        The duration in milliseconds.
    
    Returns
    -------
    str
        The converted duration as a formatted string 'mm min, ss seconds'.
    """
    try:
        totalsecs = ms // 1000
    except TypeError:
        print("Song duration must be numeric")
    except:
        print("Something went wrong with converting the song duration")
    mins = totalsecs // 60
    secs = totalsecs - mins * 60
    string = "%.0i min, %.0i sec" % (mins, secs)
    return string

class Playlist(rd.Playlist):
    """
    A class that inherits the base Paylist class in the readdata module.
    
    This Playlist class extends the functionality of the base Playlist class by
    providing additional insights about the playlist data including information about
    most frequent labels, artists, genres, shortest duration, longest duration, slowest tempo,
    and fastest tempo.
    
    Attributes
    ----------
    topLabel : list
        The most frequent record label in the playlist and its corresponding count of occurence in the playlist.
    topArtists : list
        The most frequent artist in the playlist and its corresponding count of occurence in the playlist.
    topGenres : list
        The most frequent genre in the playlist and its corresponding count of occurence in the playlist.
    shortest : list
        The song with the shortest duration in the playlist (title, artist, duration).
    longest : list
        The song with the longest duration in the playlist (title, artist, duration).
    slowest : list
        The song with the slowest tempo in the playlist (title, artist, tempo).
    fastest : list
        The song with the fastest tempo in the playlist (title, artist, tempo).
    
    Methods
    -------
    plstats():
        Prints the statistical summary of the playlist. 
    """
    @property
    def topLabel(self):
        """
        Returns the most frequent record label and its corresponding count in the playlist.
        
        Returns
        -------
        list
            A list containing the top lable and its count.
        """
        topcounts = self.labels.value_counts()
        topvalue = topcounts.idxmax()
        topcount = topcounts.max()
        return [topvalue, topcount]
    
    @property
    def topArtists(self):
        """
        Returns the most frequent artist and its corresponding count in the playlist.
        
        Returns
        -------
        list
            A list containing the top artist and their song count in the playlist.
        """
        topcounts = self.artists.value_counts()
        topvalue = topcounts.idxmax()
        topcount = topcounts.max()
        return [topvalue, topcount]
    
    @property
    def topGenres(self):
        """
        Returns the most frequent genre and its corresponding count in the playlist.
        
        Returns
        -------
        list
            A list containing the top genre and its count.
        """
        genrelist = []
        for row in self.genres:
            for item in row.split(sep = ","):
                genrelist.append(item)
        genreseries = pd.Series(genrelist)
        topcounts = genreseries.value_counts()
        topvalue = topcounts.idxmax()
        topcount = topcounts.max()
        return [topvalue, topcount]
    
    @property
    def shortest(self):
        """
        Returns the song with the shortest duration in the playlist.
        
        Returns
        -------
        list
            A list containing the title of the song with the shortest duration, its artist, and its duration. 
        """
        index = self.durations.idxmin()
        song = rd.Song(self, index)
        return [song.track, song.artist, toMins(song.duration)]
    
    @property
    def longest(self):
        """
        Returns the song with the longest duration in the playlist.
        
        Returns
        -------
        list
            A list containing the title of the song with the longest duration, its artist, and its duration.
        """
        index = self.durations.idxmax()
        song = rd.Song(self, index)
        return [song.track, song.artist, toMins(song.duration)]
    
    @property
    def slowest(self):
        """
        Returns the song with the slowest tempo in the playlist.
        
        Returns
        -------
        list
            A list containing the title of tbe song with the slowest tempo, its artist, and its tempo.
        """
        index = self.tempos.idxmin()
        song = rd.Song(self, index)
        return [song.track, song.artist, str(int(song.tempo)) + " BPM"]
    
    @property
    def fastest(self):
        """
        Returns the song with the fastest tempo in the playlist.
        
        Returns
        -------
        list
            A list containing the title of the song with the fastest tempo, its artist, and its tempo.
        """
        index = self.tempos.idxmax()
        song = rd.Song(self, index)
        return [song.track, song.artist, str(int(song.tempo)) + " BPM"]
    
    def plstats(self):
        """
        Prints the statistical summary of the playlist including:
        - Total number of songs in the playlist.
        - If a song appears more than once in the playlist
        - Shortest and longest songs with its durations
        - Slowest and fastest songs with its tempos
        - Most represented artist, genre, and record label.
        """

        try:
            print("Stats for playlist using %s.csv:" % (self.filename))
            print("------------------------------" + "-" * len(self.filename))
            print("This playlist has %i songs." % (self.length))
            if self.ids.is_unique:
                print("This playlist has no duplicate songs.")
            else: print("This playlist contains duplicate songs.")
            print("The shortest song is %s by %s with a duration of %s." % (self.shortest[0], self.shortest[1], self.shortest[2]))
            print("The longest song is %s by %s with a duration of %s." % (self.longest[0], self.longest[1], self.longest[2]))
            print("The slowest song is %s by %s with a tempo of %s." % (self.slowest[0], self.slowest[1], self.slowest[2]))
            print("The fastest song is %s by %s with a tempo of %s." % (self.fastest[0], self.fastest[1], self.fastest[2]))
            print("%s is the most represented artist with %s songs." % (self.topArtists[0], self.topArtists[1]))
            print("%s is the most represented genre with %s songs." % (self.topGenres[0].capitalize(), self.topGenres[1]))
            print("%s is the most represented record label with %s songs." % (self.topLabel[0], self.topLabel[1]))
        except:
            print("Something went wrong printing the stats summary!")
