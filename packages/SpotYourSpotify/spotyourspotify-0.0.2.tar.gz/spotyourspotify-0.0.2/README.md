# Spot Your Spotify
Collaborative programming DATA 533 Project by Seamus Riordan-Short and Jason Samuel Suwito.

Travis CI passing build stamp:
[![Build Status](https://app.travis-ci.com/seamusprs/spotyour3.svg?token=7UF1azKGExT8qQ7H4BEq&branch=main)](https://app.travis-ci.com/seamusprs/spotyour3)

### Project idea: Personalized Spotify Playlist Stats & Quiz: Spot your Spotify.

A package that contains two subpackages: stats and quiz. Stats allows users to gain insights about their Spotify playlist such as top artist, longest song, slowest song, etc. Quiz allows users to enter a game where they will be questioned on how well they know their playlist. The program will read a CSV file of the user playlist that users can obtain using Exportify.

**Package**: spotyourspotify
  - **Subpackage**: stats: contains all the code for parsing and analysing playlist

    - **Module**: `readdata`: for parsing the playlist
        - **Class**: `Playlist`: A class for playlist managing and interaction. The Question class loads the playlist data from a user's CSV file. It allows access to the data including functions to fetch specific songs and its corresponding attributes. 
            - **Methods**: 
                - `showtable()`: Prints the playlist table.
                - `getSong(index)`: Fetch a song data from the playlist at a specified index.
                - `getSongId(id)`: Fetch a song data from the playlist by a specified id. 
                - `randSong()`: Returns a random song from the playlist.
            - **Attributes**:
                - `filename` : str
                    
                    Name (or path) of the CSV file (without the .csv extension) that containes the playlist data.

                - `table` : pandas.DataFrame

                    The pandas DataFrame that contains the playlist data.

                - `length` : int
            
                    Total number of songs (rows) in the playlist.
        
                - `ids` : pandas.Series
            
                    Unique identifiers (Track ID) of songs in the playlist
    
                - `tracks` : pandas.Series
            
                    The title(s) of the song(s) in the playlist.
        
                - `albums` : pandas.Series
                    
                    The album(s) of the song(s) in the playlist.
        
                - `artists` : pandas.Series
            
                    The artist name(s) of the song(s) in the playlist.
        
                - `releases` : pandas.Series
            
                    The release date(s) of the song(s) in the playlist.
        
                - `durations` : pandas.Series
            
                    The duration (millisecond) of the song(s) in the playlist.
        
                - `genres` : pandas.Series
                    
                    The genres of the song(s) in the playlist.

                - `labels` : pandas.Series
                
                    The record label that publishes the song(s) in the playlist.

                - `tempos` : pandas.Series
            
                    The tempo (BPM) of the song(s) in the playlist.

        - **Class**: `Song`: A class for managing and interacting a single song in the playlist. The Song class is initialized with a playlist object and optional identifier (index or Track ID). A random song is selected if the optional identifier is not provided.

    - **Module**: `showstats`: contains the code for analysing playlist and giving fun stats.
        - **Class**: `Playlist`: A class that inherits the base Paylist class in the readdata module. This Playlist class extends the functionality of the base Playlist class by providing additional insights about the playlist data including information about most frequent labels, artists, genres, shortest duration, longest duration, slowest tempo, and fastest tempo.
            - **Attributes**:
                - `topLabel` : list
                    
                    The most frequent record label in the playlist and its corresponding count of occurence in the playlist.

                - `topArtists` : list
                    
                    The most frequent artist in the playlist and its corresponding count of occurence in the playlist.

                - `topGenres` : list
                    
                    The most frequent genre in the playlist and its corresponding count of occurence in the playlist.

                - `shortest` : list
                    
                    The song with the shortest duration in the playlist (title, artist, duration).

                - `longest` : list
                    
                    The song with the longest duration in the playlist (title, artist, duration).

                - `slowest` : list
                    
                    The song with the slowest tempo in the playlist (title, artist, tempo).

                - `fastest` : list
                    
                    The song with the fastest tempo in the playlist (title, artist, tempo).

            - **Methods**:
                - `plstats()`: Prints the statistical summary of the playlist. 

  - **Subpackage**: `quiz`: contains modules and functions to build and run the quiz for the user based on their playlist stats.
    
    - **Module**: `quizbuilder`: build the quiz with question libraries
        
        - **Class**: `Question`: A class for a question in the quiz game. The Question class allows for questions to be built based on the current playlist. It includes functions for fetching songs, checking the desired question type,  and checking the validity of answers.

            - **Attributes**:
                - `cur_question` : str
                    
                    A string containing the question being asked of the user.
    
                - `cur_options` : list of str
        
                    A list of strings containing four possible solutions to the question (one correct).
    
                - `cur_solution` :
        
                    A string containing the correct answer to the question being asked.

            - **Methods**:
                - `getdata(num_song=4)`: Builds a list of songs randomly selected from the playlist, used as options when generating questions.
                - `makequestion(question_type : str)`: Takes the desired question type as an argument, calls the appropriate question type function, and returns the question information (question, options, and solution).
                - `checker(user_input, solution)`:
                Compares the user input answer to the correct solution and returns True if correct, false otherwise.
            
        - **Class** `QuestionBuilder(Question)`: A class for different question types in the quiz game. Inherits from the Question class and includes methods for various types of questions.
            - **Methods**:
                - `artist_question()`: Builds a question identifying a song's artist.
                - `label_question()`: Builds a question identifying a song's record label.
                - `length_question()`: Builds a question comparing song lengths.
                - `age_question()`: Builds a question comparing song release dates.
                - `tempo_question()`: Builds a question comparing song tempos (BPM).

    - **Module**: `playgame`: run the quiz

        - **Class** `Game`: A class for a quiz game. The Game class handles most aspects of conducting the quiz game, including all interactions with the user for the main game loop, as well as functions such as setting a random seed, asking questions, checking solutions, and keeping score.

            - **Attributes**:
                - `q_builder` : QuestionBuilder
        
                    An instance of the 'QuestionBuilder' class specific to the current playlist.
    
                - `score` : int
        
                    The number of questions correctly answered in the current game.
    
                - `q_count` : int
        
                    The number of questions asked in the current game.
            
            - **Methods**:
                - `getoptions()`: Returns a list of possible question types.
                - `setseed()`: Sets random seed for reproducibility in otherwise randomized actions (question order).
                - `ask(q_type : str)`: Gets a question, asks the user, and checks user input answer against correct solution.
                - `getscore()`: Prints number of correct answers and number of total questions asked.
                - `play()`: Takes the user through the main quiz game loop.
