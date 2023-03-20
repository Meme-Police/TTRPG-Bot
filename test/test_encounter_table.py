import unittest
from unittest.mock import MagicMock
# This import will only work when the test is run from the main directory
from bot import encounter_table
class EncounterTable(unittest.TestCase):

    def testAddItem(self):
        shop = encounter_table.EncounterTable()
        shop.addItem("Description")
        self.assertEqual(shop.table[0], ("Description"))
    def testRemoveItem(self):
        shop = encounter_table.EncounterTable(table=["Description"])
        shop.removeItem(0)
        self.assertEqual(len(shop.table), 0)
    def testDisplayTable(self):
        shop = encounter_table.EncounterTable(table=["Description"])
        string = shop.displayTable()
        self.assertEqual(string, "```\n1: Description\n```")
    def testChoseItem(self):
        shop = encounter_table.EncounterTable(table=["Description"])
        string = shop.choseItem()
        self.assertEqual(string, "```\nDescription\n```")
    def testToFromJson(self):
        control = encounter_table.EncounterTable([], 0)
        new = encounter_table.fromJson(control.toJson())
        self.assertEqual(control.table, new.table)