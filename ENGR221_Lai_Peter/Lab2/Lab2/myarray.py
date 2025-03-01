"""
Author: Peter Lai
Filename: myarray.py
Description: Implementation of multiple sorting algorithms.
"""

class MyArray():
    # Constructor
    def __init__(self, initialSizeOrValues):

        if type(initialSizeOrValues) == int: # Array Initialization
            self.__a = initialSizeOrValues # Stores list as array
            self.__length = len(initialSizeOrValues) # Sets length to list length
            self.__capacity = self.__length # Sets capacity equal to value set

        elif type(initialSizeOrValues) == int: # Array Initialization
            self.__a = [None] * initialSizeOrValues # The array stored as a list
            self.__length = 0               # Start with no values in the list
            self.__capacity = initialSizeOrValues # Sets capacity to integer

        else:
            print("Invalid") # error message
    
    ########
    # Methods
    ########
        
    # Return the current length of the array
    def length(self):
        return self.__length 
    
    # Return a list of the current array values
    def values(self):
        return self.__a[:self.__length]

    # Return the value at index idx
    # Otherwise, do not return anything
    def get(self, idx):
      if 0 <= idx and idx < self.__length: # Check if idx is in bounds, and
         return self.__a[idx]              # only return item if in bounds
 
    # Set the value at index idx
    def set(self, idx, value):         
      if 0 <= idx and idx < self.__length: # Check if idx is in bounds, and
         self.__a[idx] = value               # only set item if in bounds
    
    # Insert value to the end of the array
    def insert(self, value):

        if self.__length == self.__capacity: #checks if array is full
            new_capacity = self.__capacity * 2 if self.__capacity > 0 else 1 #cap is doubled if > 0, otherwise initializes 1
            self.__a.extend([None] * [new_capacity - self.__capacity]) # expands null capacity
            self.__capacity = new_capacity # updates capacity

        self.__a[self.__length] = value # sets new value at current position

        # Increment the length
        self.__length += 1   

    # Return the index of value in the array, 
    # or -1 if value is not in the array
    def search(self, value):

        # Only search the indices we've inserted
        for idx in range(self.__length): 

            # Check the value at the current index 
            if self.__a[idx] == value:  

                # Return the index  
                return idx  
            
        # Return -1 if value was not found             
        return -1                        

    # Delete the first occurrence of value in the array
    # Returns True if value was deleted, False otherwise
    def delete(self, value):

        deleted = False # sees if deletion was successful

        i = 0 # establishing search value

        while i < self.__length: # Finds first occurance of value in array

            if self.__a[i] == value:

                for j in range (i, self.__length - 1):
                    self.__a[j] = self.__a[j + 1] 
                self.__a[self.__length - 1] = None #sets ending value to "None"

                self.__length -= 1 # Reduces array length
        # Find the index of the value to delete
        idx = self.search(value)
        
        # If the value was found
        if idx != -1: 

            # Decrement the array length
            self.__length -= 1

            # Shift all the remaining values 
            for j in range(idx, self.__length):
                self.__a[j] = self.__a[j+1]

            # Return that value was deleted
            return True
        
        # Return False if the value was not found
        return False
    
    # Print all items in the list
    def traverse(self):
        for i in range(self.__length):
            print(self.__a[i])

if __name__ == '__main__':
    pass
