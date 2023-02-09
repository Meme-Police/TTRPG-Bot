import unittest
from unittest.mock import MagicMock
# This import will only work when the test is run from the main directory
from bot import dice

###########################################################################
# Important information regarding running tests
# Tests must be run from the main directory
# Tests must start with the word test to be discovered
# Use the command "python -m unittest discover -s test" to run all tests
###########################################################################

class DiceTest(unittest.TestCase):
    def testRoll(self):
        result = dice.make_roll("3d10")
        self.assertEqual(len(result[0]), 3)
    def testParsing(self):
        # This string contains three instances of dice notation.
        roll_string = "3d10+4d6+d20+4"
        rolls = dice.parse_rolls(roll_string)
        self.assertEqual(rolls, ["3d10", "4d6", "d20"])
        
if __name__ == '__main__':
    unittest.main()
