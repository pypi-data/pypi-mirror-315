import unittest
import sys
from pathlib import Path

src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))

from SpotYourSpotify.stats import showstats as ss

class TestPlaylistSs(unittest.TestCase):
    """Tests the additional playlist functions included in the showstats Playlist class"""

    @classmethod
    def setUpClass(TestPlaylistSs):
        TestPlaylistSs.testpl = ss.Playlist(f"{src_path}/SpotYourSpotify/playlist")

    def setUp(self):
        self.testpl = ss.Playlist(f"{src_path}/SpotYourSpotify/playlist")

    def tearDown(self):
        self.testpl = None

    @classmethod
    def tearDownClass(TestPlaylistSs):
        TestPlaylistSs.testpl = None

    def test_label(self):
        self.assertEqual(self.testpl.topLabel[0], "Columbia")
        self.assertEqual(self.testpl.topLabel[1], 43)

    def test_artist(self):
        self.assertEqual(self.testpl.topArtists[0], "KISS")
        self.assertEqual(self.testpl.topArtists[1], 12)

    def test_genre(self):
        self.assertEqual(self.testpl.topGenres[0], "rock")
        self.assertEqual(self.testpl.topGenres[1], 513)

    def test_length(self):
        self.assertEqual(self.testpl.shortest[0], "Fell In Love With a Girl")
        self.assertEqual(self.testpl.shortest[2], "1 min, 50 sec")
        self.assertEqual(self.testpl.longest[0], "Bat Out of Hell")
        self.assertEqual(self.testpl.longest[2], "9 min, 50 sec")

    def test_tempo(self):
        self.assertEqual(self.testpl.slowest[0], "Desperado - 2013 Remaster")
        self.assertEqual(self.testpl.slowest[2], "60 BPM")
        self.assertEqual(self.testpl.fastest[0], "Lovin', Touchin', Squeezin'")
        self.assertEqual(self.testpl.fastest[2], "211 BPM")

class TestCalc(unittest.TestCase):
    """Tests the time conversion (ms to mins) function"""

    @classmethod
    def setUpClass(TestCalc):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(TestCalc):
        pass

    def test_integers(self):
        self.assertEqual(ss.toMins(60000), "1 min, 0 sec")
        self.assertEqual(ss.toMins(6000000), "100 min, 0 sec")
        self.assertEqual(ss.toMins(6000), "0 min, 6 sec")

    def test_floats(self):
        self.assertEqual(ss.toMins(60000.01), "1 min, 0 sec")
        self.assertEqual(ss.toMins(6000000.01), "100 min, 0 sec")
        self.assertEqual(ss.toMins(6000.01), "0 min, 6 sec")