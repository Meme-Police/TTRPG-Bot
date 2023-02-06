import unittest
import dice


class TestDice(unittest.TestCase):
    def testRoll(self):
        result = dice.make_roll("3d10")
        self.assertEqual(len(result[0]), 3)
        
if __name__ == '__main__':
    unittest.main()
