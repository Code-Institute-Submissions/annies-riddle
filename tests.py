import unittest, json
from types import IntType
from utils import check_username, check_answer, get_next_riddle
from constants import *

with open("data/riddles.json") as riddle_file:
    RIDDLES = json.load(riddle_file)["riddles"]
    
with open("data/scores.json") as scores_file:
    USERSCORES = json.load(scores_file)

class AnswerTests(unittest.TestCase):
    '''
    Asserts a known correct answer is checked as correct
    '''
    def test_correct_answer(self):
        self.assertTrue(
            check_answer(RIDDLES[3], "lawsuit"), 
            "Correct answer was checked as incorrect")
        
    '''
    Asserts a known incorrect answer is checked as incorrect
    '''
    def test_incorrect_answer(self):
        self.assertFalse(
            check_answer(RIDDLES[5], "incorrect"), 
            "Incorrect answer was not marked as incorrect")
        
    '''
    Asserts an empty answer is checked as incorrect
    '''
    def test_empty_answer(self):
        self.assertFalse(
            check_answer(RIDDLES[7], ""), 
            "Empty answer was not marked as empty")
    
    '''
    Asserts a constant is an integer as required
    '''
    def test_points_const_is_int(self):
        self.assertTrue(
            type(POINTS_PER_RIDDLE) is IntType,
            "POINTS_PER_RIDDLE constant is not an integer")

class RiddleTests(unittest.TestCase):
    '''
    Asserts that game doesn't load a riddle beyond MAX_RIDDLES
    '''
    def test_game_over(self):
        self.assertEqual(
            get_next_riddle(RIDDLES, MAX_RIDDLES-1), 
            None, 
            "Game did not end after maximum number of riddles")
        
    '''
    Asserts that initial riddle is loaded correctly
    '''
    def test_initial_load(self):
        self.assertEqual(
            get_next_riddle(RIDDLES, None)["question"], 
            "I have no muscle, yet I rule two hemispheres. What am I?", 
            "First riddle did not load")
            
    '''
    Asserts that ATTEMPTS_PER_RIDDLE is an integer as required
    '''
    def test_attempts_const_is_int(self):
        self.assertTrue(
            type(ATTEMPTS_PER_RIDDLE) is IntType,
            "ATTEMPTS_PER_RIDDLE constant is not an integer")

class UsernameTests(unittest.TestCase):
    '''
    Asserts that an empty username is checked as invalid
    '''
    def test_username_empty(self):
        result = check_username(USERSCORES, "")
        self.assertFalse(result, "Empty username was not marked as empty")
        
    '''
    Asserts that a known taken username is checked as invalid
    '''
    def test_username_taken(self):
        result = check_username(USERSCORES, "smithers")
        self.assertFalse(result, "Taken username was not marked as taken")

if __name__ == '__main__':
    unittest.main()