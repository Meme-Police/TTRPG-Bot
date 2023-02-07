import unittest
from bot import dice

class DiceTest(unittest.TestCase):
    def testRoll(self):
        result = dice.make_roll("3d10")
        print("Test was run {result}")
        self.assertEqual(len(result[0]), 3)
        
if __name__ == '__main__':
    unittest.main()
