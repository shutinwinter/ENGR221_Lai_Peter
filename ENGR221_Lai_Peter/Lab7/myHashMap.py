"""
Author: Peter Lai
FileName: myHashMap.py
Description: to impliment a hashmap
Adapted from UCSD CSE12
"""

"""
MyHashMap Implementation
Python hash map implementation using separate chaining for collision resolution
"""

class MyHashMap:
    def __init__(self, load_factor=0.75,
                       initial_capacity=16):
        self.load_factor = load_factor 
        self.capacity = initial_capacity 
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    """
    Resizes the self.buckets array when the load_factor is reached. """
    def resize(self):
        # Store old buckets
        old_buckets = self.buckets
        # Double the number of buckets
        self.capacity *= 2 
        # Create a new set of buckets that's twice as big as the old one
        self.buckets = [[] for _ in range(self.capacity)]
        # Reset size to recalculate during rehashing
        old_size = self.size
        self.size = 0
        # Add each key, value pair already in the MyHashMap to the new buckets
        for bucket in old_buckets:
            if bucket != []:
                for entry in bucket:
                    self.put(entry.getKey(), entry.getValue())
        # Ensure size is correctly maintained
        assert self.size == old_size, "Size mismatch after resizing"

    """
    Adds the specified key, value pair to the MyHashMap if 
    the key is not already in the MyHashMap. If adding a new key would
    surpass the load_factor, resize the MyHashMap before adding the key.
    Return true if successfully added to the MyHashMap.
    Raise an exception if the key is None. """
    def put(self, key, value):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Check if resize is needed before adding
        if (self.size + 1) / self.capacity > self.load_factor:
            self.resize()
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key already exists
        for entry in self.buckets[index]:
            if entry.getKey() == key:
                return False  # Key already exists
        
        # Add the new entry
        new_entry = self.MyHashMapEntry(key, value)
        self.buckets[index].append(new_entry)
        self.size += 1
        return True

    """
    Replaces the value that maps to the given key if it is present.
    Input: key is the key whose mapped value is being replaced.
           newValue is the value to replace the existing value with.
    Return true if the key was in this MyHashMap and replaced successfully.
    Raise an exception if the key is None. """
    def replace(self, key, newValue):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key exists
        for entry in self.buckets[index]:
            if entry.getKey() == key:
                entry.setValue(newValue)
                return True
        
        return False  # Key not found

    """
    Remove the entry corresponding to the given key.
    Return true if an entry for the given key was removed.
    Raise an exception if the key is None. """
    def remove(self, key):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key exists
        for i, entry in enumerate(self.buckets[index]):
            if entry.getKey() == key:
                # Remove the entry
                self.buckets[index].pop(i)
                self.size -= 1
                return True
        
        return False  # Key not found

    """
    Adds the key, value pair to the MyHashMap if it is not present.
    Otherwise, replace the existing value for that key with the given value.
    Raise an exception if the key is None. """
    def set(self, key, value):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key already exists
        for entry in self.buckets[index]:
            if entry.getKey() == key:
                entry.setValue(value)
                return
        
        # If we reach here, key doesn't exist, so add it
        # Check if resize is needed
        if (self.size + 1) / self.capacity > self.load_factor:
            self.resize()
            # Recalculate index after resize
            index = key_hash % self.capacity
        
        # Add the new entry
        new_entry = self.MyHashMapEntry(key, value)
        self.buckets[index].append(new_entry)
        self.size += 1

    """
    Return the value of the specified key. If the key is not in the
    MyHashMap, return None.
    Raise an exception if the key is None. """
    def get(self, key):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key exists
        for entry in self.buckets[index]:
            if entry.getKey() == key:
                return entry.getValue()
        
        return None  # Key not found

    """
    Return the number of key, value pairs in this MyHashMap. """
    def size(self):
        return self.size

    """
    Return true if the MyHashMap contains no elements, and 
    false otherwise. """
    def isEmpty(self):
        return self.size == 0

    """
    Return true if the specified key is in this MyHashMap. 
    Raise an exception if the key is None. """
    def containsKey(self, key):
        if key is None:
            raise ValueError("Key cannot be None")
        
        # Find the index for this key
        key_hash = hash(key)
        index = key_hash % self.capacity
        
        # Check if key exists
        for entry in self.buckets[index]:
            if entry.getKey() == key:
                return True
        
        return False  # Key not found

    """
    Return a list containing the keys of this MyHashMap. 
    If it is empty, return an empty list. """
    def keys(self):
        keys_list = []
        
        for bucket in self.buckets:
            for entry in bucket:
                keys_list.append(entry.getKey())
        
        return keys_list

    class MyHashMapEntry:
        def __init__(self, key, value):
            self.key = key 
            self.value = value 

        def getKey(self):
            return self.key 
        
        def getValue(self):
            return self.value 
        
        def setValue(self, new_value):
            self.value = new_value 

if __name__ == "__main__":
    pass