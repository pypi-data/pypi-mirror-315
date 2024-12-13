from SpotYourSpotify.stats import showstats as ss
from SpotYourSpotify.quiz import playgame as pg

class StartQuizError(Exception):
    pass

print("Welcome to Spot Your Spotify!")
print("Please select a playlist.")

inp = ""

while inp != "exit":
    inp = input("Enter path to playlist csv without file extension: ").lower()
    if inp == "":
        try:
            pl = ss.Playlist("SpotYourSpotify/playlist")
        except:
            print("Default playlist not found!")
            continue
    else:
        try:
            pl = ss.Playlist(inp)
        except:
            print("Invalid file path! Please try again, or leave blank to use example playlist")
            continue

    while inp != "exit":
        print("Please enter 'stats' for playlist information, 'quiz' for the quiz game, 'new' to change playlist, or 'exit' to exit.")
        inp = input("Please enter option: ").lower()
        if inp == "exit" or inp == "new": 
            break
        elif inp == "stats": 
            pl.plstats()
        elif inp == "quiz": 
            try:
                quiz = pg.Game(pl)
                quiz.play()
            except NameError:
                print("Could not access playlist to create quiz, please try selecting a new playlist file")
            except:
                print("Could not start quiz!")
                raise StartQuizError
            
        else:
            print("Input not accepted, please try again")
            continue

print("Goodbye!")
