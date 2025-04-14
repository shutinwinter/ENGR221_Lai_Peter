import unittest
from myHashMap import MyHashMap

class TestMyHashMap(unittest.TestCase):
    def test_put_and_get(self):
        hashmap = MyHashMap()
        # Test putting and getting values
        self.assertTrue(hashmap.put("key1", "value1"))
        self.assertTrue(hashmap.put("key2", "value2"))
        self.assertTrue(hashmap.put("key3", "value3"))
        
        self.assertEqual(hashmap.get("key1"), "value1")
        self.assertEqual(hashmap.get("key2"), "value2")
        self.assertEqual(hashmap.get("key3"), "value3")
        self.assertIsNone(hashmap.get("nonexistent"))
        
        # Test putting an existing key
        self.assertFalse(hashmap.put("key1", "new_value"))
        self.assertEqual(hashmap.get("key1"), "value1")  # Should not change
        
    def test_resize(self):
        hashmap = MyHashMap(load_factor=0.5, initial_capacity=4)
        # Add elements until resize is triggered
        for i in range(3):  # 3 elements with load_factor=0.5 and capacity=4 will trigger resize
            hashmap.put(f"key{i}", f"value{i}")
            
        # After resize, capacity should be 8
        self.assertEqual(hashmap.capacity, 8)
        
        # Ensure all values are still accessible
        for i in range(3):
            self.assertEqual(hashmap.get(f"key{i}"), f"value{i}")
    
    def test_remove_and_contains(self):
        hashmap = MyHashMap()
        hashmap.put("key1", "value1")
        hashmap.put("key2", "value2")
        
        # Test containsKey
        self.assertTrue(hashmap.containsKey("key1"))
        self.assertTrue(hashmap.containsKey("key2"))
        self.assertFalse(hashmap.containsKey("nonexistent"))
        
        # Test remove
        self.assertTrue(hashmap.remove("key1"))
        self.assertFalse(hashmap.containsKey("key1"))
        self.assertIsNone(hashmap.get("key1"))
        
        # Test removing non-existent key
        self.assertFalse(hashmap.remove("nonexistent"))
        
        # Test keys list
        self.assertEqual(set(hashmap.keys()), {"key2"})
    
    def test_set_and_replace(self):
        hashmap = MyHashMap()
        
        # Test set (add new key)
        hashmap.set("key1", "value1")
        self.assertEqual(hashmap.get("key1"), "value1")
        
        # Test set (replace existing key)
        hashmap.set("key1", "new_value")
        self.assertEqual(hashmap.get("key1"), "new_value")
        
        # Test replace
        self.assertTrue(hashmap.replace("key1", "replaced_value"))
        self.assertEqual(hashmap.get("key1"), "replaced_value")
        
        # Test replace non-existent key
        self.assertFalse(hashmap.replace("nonexistent", "value"))

if __name__ == "__main__":
    unittest.main()