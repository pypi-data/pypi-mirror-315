import unittest
import random
import builtins
from io import StringIO
import sys
from pathlib import Path

src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

from SpotYourSpotify.stats import readdata as rd
from SpotYourSpotify.quiz.playgame import Game

class TestPlayGame(unittest.TestCase):
    """Test for the Game class"""

    @classmethod
    def setUpClass(cls):
        cls.testpl = rd.Playlist(f"{src_path}/SpotYourSpotify/playlist")
    
    def setUp(self):
        self.game = Game(self.testpl)
    
    def tearDown(self):
        self.game = None
        
    @classmethod
    def tearDownClass(cls):
        cls.testpl = None
        
    def test_getOptions(self):
        expected = ["artist", "label", "length", "age", "tempo"]
        self.assertEqual(self.game.getoptions(), expected, "options given are not part of the expected options list.")
    
    def test_setSeed(self):
        self.game.setseed(8566)
        first = random.randint(0, 1000000)
        self.game.setseed(8566)
        second = random.randint(0, 1000000)
        self.assertEqual(first, second, "Random number produced by the same seed is not consistent")
        
    def test_getScore(self):
        self.game.score = 2
        self.game.q_count = 3
        expected = f"Your current score is: {self.game.score}/{self.game.q_count}. Keep up the great work!"
        got = self.game.getscore()
        self.assertEqual(got, expected, f"Received: {got}, Expected: {expected}")
        
    def test_askQuestion(self):
        #use dummy make question and checker function to simulate user input.
        def dummy_makeQuestion(q_type):
            return "This is a temporary question", ["Temporary Option 1", "Temporary Option 2"], "Temporary Option 1"
        def dummy_checker(user_answer, solution):
            return user_answer == solution
    
        self.game.q_builder.makequestion = dummy_makeQuestion
        self.game.q_builder.checker = dummy_checker
        
        #correct answer check:
        self.game.score = 0
        self.game.q_count = 0
        
        def dummy_input(prompt):
            print(prompt)
            return "1"
        
        real_input = builtins.input
        builtins.input = dummy_input
        
        try:
            self.game.ask("artist")
            self.assertEqual(self.game.score, 1)
            self.assertEqual(self.game.q_count, 1)
        finally:
            builtins.input = real_input
        
        #wrong answer check:
        self.game.score = 0
        self.game.q_count = 0
        
        def dummy_input2(prompt):
            print(prompt)
            return "2"
        
        real_input = builtins.input
        builtins.input = dummy_input2
        
        try:
            self.game.ask("artist")
            self.assertEqual(self.game.score, 0)
            self.assertEqual(self.game.q_count, 1)
        finally:
            builtins.input = real_input
            
        #invalid input check:
        self.game.score = 0
        self.game.q_count = 0
        
        loop_count = 0
        
        def dummy_input3(prompt):
            print(prompt)
            nonlocal loop_count
            loop_count += 1
            if loop_count < 2:
                return "text"
            if loop_count < 3:
                return "7"
            else :
                return "1"
        
        real_input = builtins.input
        builtins.input = dummy_input3
        
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.game.ask("artist")
            out = sys.stdout.getvalue()
            self.assertIn("Invalid input. Please enter a number from the list!", out)
            self.assertIn("Invalid number. Please enter a number from the list!", out)
            self.assertEqual(self.game.score, 1)
            self.assertEqual(self.game.q_count, 1)
        finally:
            builtins.input = real_input
            
            
    def test_play(self):
        dummy_input_list = iter(["dummyUser", "score", "exit"])
        
        def dummy_input(prompt):
            return next(dummy_input_list)
        
        real_input = builtins.input
        builtins.input = dummy_input
        
        real_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.game.score = 8
            self.game.q_count = 10
            
            self.game.play()
            
            out = sys.stdout.getvalue()
            
            self.assertIn("SPOT YOUR SPOTIFY: QUIZ", out, "Quiz title is not printed")
            self.assertIn("Hello dummyUser!", out, "Hello username is not printed")
            self.assertIn("Your current score is: 8/10. Keep up the great work!", out, "Score is not printed")
            self.assertIn("QUIZ ENDED. dummyUser's score is 8/10", out, "Exit message not printed")
        
        finally:
            builtins.input = real_input
            sys.stdout = real_stdout
            
unittest.main(argv =[''], verbosity=2, exit=False)