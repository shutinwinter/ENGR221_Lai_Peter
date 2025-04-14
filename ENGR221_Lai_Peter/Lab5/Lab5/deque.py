"""
WRITE YOUR PROGRAM HEADER HERE
"""

from .doublyLinkedList import DoublyLinkedList

class Deque():
    def __init__(self):
        self.__values = DoublyLinkedList()

    def isEmpty(self):
        return self.__values.isEmpty()
    
    def __len__(self):
        return len(self.__values)
    
    def __str__(self):
        return str(self.__values)

    def peekLeft(self):
        return self.__values.first()

    def peekRight(self):
        if self.isEmpty():
            raise Exception("Deque is empty")
        return self.__values.getLastNode().getValue()

    def insertLeft(self, value):
        self.__values.insertFront(value)
        
    def insertRight(self, value): 
        self.__values.insertBack(value)

    def removeLeft(self): 
        return self.__values.deleteFirstNode()

    def removeRight(self):
        return self.__values.deleteLastNode()
    
if __name__ == "__main__":
    pass