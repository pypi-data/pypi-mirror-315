import unittest
import random
import sys
from pathlib import Path

src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

from SpotYourSpotify.stats import readdata as rd
from SpotYourSpotify.quiz.quizbuilder import Question, QuestionBuilder


class TestQuestion(unittest.TestCase):
    """Test the Question class"""
    
    @classmethod
    def setUpClass(cls):
        cls.testpl = rd.Playlist(f"{src_path}/SpotYourSpotify/playlist")
        
    def setUp(self):
        self.question = Question(self.testpl)
        
    def tearDown(self):
        self.question = None
        
    @classmethod
    def tearDownClass(cls):
        cls.testpl = None
    
    def test_getData(self):
        data = self.question.getdata()
        self.assertEqual(len(data), 4, "Number of songs return is not 4")
        
    def test_checkerTrue(self):
        self.assertTrue(self.question.checker("True", "True"))
    
    def test_checkerFalse(self):
        self.assertFalse(self.question.checker("False", "True"))
        
    def test_invalidType(self):
        with self.assertRaises(ValueError):
            self.question.makequestion("invalid")
        

class TestQuestionBuilder(unittest.TestCase):
    """Test the QuestionBuilder class"""
    
    @classmethod
    def setUpClass(cls):
        cls.testpl = rd.Playlist(f"{src_path}/SpotYourSpotify/playlist")
        
    def setUp(self):
        self.qBuilder = QuestionBuilder(self.testpl)
    
    def tearDown(self):
        self.qBuilder = None
    
    @classmethod
    def tearDownClass(cls):
        cls.testpl = None

    def test_makeQuestion(self):
        question, options, solution = self.qBuilder.makequestion("artist")
        cur_question = self.qBuilder.cur_question
        cur_options = self.qBuilder.cur_options
        cur_solution = self.qBuilder.cur_solution
        self.assertEqual(cur_question, question, f"cur_question: {cur_question} does not match with question: {question}")
        self.assertEqual(cur_options, options, f"cur_options: {cur_options} does not match with options: {options}")
        self.assertEqual(cur_solution, solution, f"cur_solution: {cur_solution} does not match with solution: {solution}")
        self.assertIsNotNone(question, "question is None")
    
    def test_artist_question(self):
        question, options, solution = self.qBuilder.artist_question()
        self.assertIn(solution, options, "solution is not in the option list")
        self.assertIsInstance(question, str, "question is not string")
        self.assertIn(len(options), [3,4], "option length is not 3 or 4")
        self.assertIsInstance(solution, str, "solution is not string")
        
        
    def test_label_question(self):
        question, options, solution = self.qBuilder.label_question()
        self.assertIn(solution, options, "solution is not in the option list")
        self.assertIsInstance(question, str, "question is not string")
        self.assertIn(len(options), [3,4], "option length is not 3 or 4")
        self.assertIsInstance(solution, str, "solution is not string")
        
    def test_length_question(self):
        question, options, solution = self.qBuilder.length_question()
        self.assertIn(solution, options, "solution is not in the option list")
        self.assertIsInstance(question, str, "question is not string")
        self.assertIn(len(options), [3,4], "option length is not 3 or 4")
        self.assertIsInstance(solution, str, "solution is not string")
        
    def test_age_question(self):
        question, options, solution = self.qBuilder.age_question()
        self.assertIn(solution, options, "solution is not in the option list")
        self.assertIsInstance(question, str, "question is not string")
        self.assertIn(len(options), [3,4], "option length is not 3 or 4")
        self.assertIsInstance(solution, str, "solution is not string")
        
    def test_tempo_question(self):
        question, options, solution = self.qBuilder.tempo_question()
        self.assertIn(solution, options, "solution is not in the option list")
        self.assertIsInstance(question, str, "question is not string")
        self.assertIn(len(options), [3,4], "option length is not 3 or 4")
        self.assertIsInstance(solution, str, "solution is not string")
        
unittest.main(argv =[''], verbosity=2, exit=False)