import unittest
from unittest.mock import MagicMock
# This import will only work when the test is run from the main directory
from bot import shop_table

###########################################################################
# Important information regarding running tests
# Tests must be run from the main directory
# Tests must start with the word test to be discovered
# Use the command "python -m unittest discover -s test" to run all tests
###########################################################################

class ShopTest(unittest.TestCase):

    def testAddItem(self):
        shop = shop_table.ShopTable()
        shop.addItem("Dog", "3gp", "It's a dog")
        self.assertEqual(shop.table[0], ("Dog", "3gp", "It's a dog"))
    def testRemoveItem(self):
        shop = shop_table.ShopTable(table=[("Dog", "3gp", "It's a dog")])
        shop.removeItem(0)
        self.assertEqual(len(shop.table), 0)
    def testDisplayTable(self):
        shop = shop_table.ShopTable(table=[("Dog", "3gp", "It's a dog")])
        string = shop.displayTable()
        self.assertEqual(string, "```\nDog 3gp: It's a dog\n```")
    def testToFromJson(self):
        control = shop_table.ShopTable([], 0)
        print(control.table)
        new = shop_table.fromJson(control.toJson())
        print(new.table)
        self.assertEqual(control.table, new.table)