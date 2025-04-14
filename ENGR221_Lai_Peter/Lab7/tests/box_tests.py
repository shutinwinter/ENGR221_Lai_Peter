import unittest
from box import Box
from entry import Entry

class TestBox(unittest.TestCase):
    def setUp(self):
        self.box = Box()
    
    def test_add_and_find(self):
        # Test adding a new entry
        self.assertTrue(self.box.add("TestNickname", "TestSpecies"))
        
        # Test finding the entry
        entry = self.box.findEntryByNickname("TestNickname")
        self.assertIsNotNone(entry)
        self.assertEqual(entry._Entry__nickname, "TestNickname")
        self.assertEqual(entry._Entry__species, "TestSpecies")
        
        # Test adding an entry with existing nickname
        self.assertFalse(self.box.add("TestNickname", "DifferentSpecies"))
        
        # Test finding with specific species
        entry = self.box.find("TestNickname", "TestSpecies")
        self.assertIsNotNone(entry)
        
        # Test finding with incorrect species
        entry = self.box.find("TestNickname", "WrongSpecies")
        self.assertIsNone(entry)
    
    def test_remove(self):
        # Add a test entry
        self.box.add("RemoveTest", "RemoveSpecies")
        
        # Test removeByNickname
        self.assertTrue(self.box.removeByNickname("RemoveTest"))
        self.assertIsNone(self.box.findEntryByNickname("RemoveTest"))
        
        # Test removing a non-existent nickname
        self.assertFalse(self.box.removeByNickname("NonExistentNickname"))
        
        # Add an entry for removeEntry test
        self.box.add("RemoveEntryTest", "RemoveEntrySpecies")
        
        # Test removeEntry with correct species
        self.assertTrue(self.box.removeEntry("RemoveEntryTest", "RemoveEntrySpecies"))
        self.assertIsNone(self.box.findEntryByNickname("RemoveEntryTest"))
        
        # Test removeEntry with incorrect species
        self.box.add("RemoveEntryTest2", "CorrectSpecies")
        self.assertFalse(self.box.removeEntry("RemoveEntryTest2", "WrongSpecies"))
        self.assertIsNotNone(self.box.findEntryByNickname("RemoveEntryTest2"))
    
    def test_find_all_nicknames(self):
        # Test on populated box from entries.txt
        nicknames = self.box.findAllNicknames()
        self.assertIsInstance(nicknames, list)
        self.assertGreater(len(nicknames), 0)
        
        # Create an empty box and test
        empty_box = Box()
        empty_box.nicknameMap = empty_box.nicknameMap.__class__()  # Create a new empty HashMap
        self.assertEqual(len(empty_box.findAllNicknames()), 0)

if __name__ == "__main__":
    unittest.main()