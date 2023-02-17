import unittest
from unittest.mock import MagicMock
from bot import member

class TestDice(unittest.TestCase):
   def testToFromJson(self):
       control_member = member.Member(1234, 10, 10, [0 for x in range(9)], [0 for x in range(9)])
       json_string = control_member.toJson()
       new_member = member.fromJson(json_string)
       self.assertEqual(control_member.id, new_member.id)
       self.assertEqual(control_member.health, new_member.health)
       self.assertEqual(control_member.spells, new_member.spells)
       