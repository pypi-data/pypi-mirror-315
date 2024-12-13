import unittest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
src_path = project_root / "src"
tests_path = project_root / "tests"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(tests_path))

import testquizbuilder as tqb
import testplaygame as tpg
import testreaddata as trd
import testshowstats as tss


def stats_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(trd.TestPlaylist('test_getplaylist'))
    suite.addTest(trd.TestPlaylist('test_properties'))
    
    suite.addTest(trd.TestSong('test_getsong_id'))
    suite.addTest(trd.TestSong('test_getsong_index'))
    suite.addTest(trd.TestSong('test_getsongs'))
    suite.addTest(trd.TestSong('test_properties'))

    suite.addTest(tss.TestPlaylistSs('test_label'))
    suite.addTest(tss.TestPlaylistSs('test_artist'))
    suite.addTest(tss.TestPlaylistSs('test_genre'))
    suite.addTest(tss.TestPlaylistSs('test_length'))
    suite.addTest(tss.TestPlaylistSs('test_tempo'))
    
    suite.addTest(tss.TestCalc('test_integers'))
    suite.addTest(tss.TestCalc('test_floats'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))

def quiz_suite():
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    suite.addTest(tqb.TestQuestion('test_getData'))
    suite.addTest(tqb.TestQuestion('test_checkerTrue'))
    suite.addTest(tqb.TestQuestion('test_checkerFalse'))
    suite.addTest(tqb.TestQuestion('test_invalidType'))

    suite.addTest(tqb.TestQuestionBuilder('test_makeQuestion'))
    suite.addTest(tqb.TestQuestionBuilder('test_artist_question'))
    suite.addTest(tqb.TestQuestionBuilder('test_label_question'))
    suite.addTest(tqb.TestQuestionBuilder('test_length_question'))
    suite.addTest(tqb.TestQuestionBuilder('test_age_question'))
    suite.addTest(tqb.TestQuestionBuilder('test_tempo_question'))
    
    suite.addTest(tpg.TestPlayGame('test_getOptions'))
    suite.addTest(tpg.TestPlayGame('test_setSeed'))
    suite.addTest(tpg.TestPlayGame('test_getScore'))
    suite.addTest(tpg.TestPlayGame('test_askQuestion'))
    suite.addTest(tpg.TestPlayGame('test_askQuestion'))
    suite.addTest(tpg.TestPlayGame('test_play'))
    
    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))

stats_suite()
quiz_suite()