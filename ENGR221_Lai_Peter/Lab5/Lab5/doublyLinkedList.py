"""
Author: Peter Lai
Filename: doublyLinkedList.py
Description: Set a doublyLinkedList
"""

from .doubleNode import DoubleNode 

class DoublyLinkedList():

    def __init__(self):
        self.__firstNode = None
        self.__lastNode = None 

    def isEmpty(self):
        return self.__firstNode is None

    def first(self):
        if self.isEmpty():
            raise Exception("List is empty")
        return self.__firstNode.getValue()
    
    def getFirstNode(self):
        return self.__firstNode

    def getLastNode(self):
        return self.___lastNode
    
    def setFirstNode(self, node):
        if isinstance(node, DoubleNode) or node is None:
            self.__firstNode = node
        else:
            raise Exception("Invalide node")

    def setLastNode(self, node):
        if isinstance(node, DoubleNode) or node is None:
            self.__lastNode = node
        else:
            raise Exception("Invalid Node")

    def find(self, value):
        current = self.__firstNode
        while current:
            if current.getValue() == value:
                return current
            current = current.getNextNode()
        return None

    def insertFront(self, value):
        new_node = DoubleNode(value, self.__firstNode)
        if self.isEmpty():
            self.__lastNode = new_node
        else:
            self.__firstNode.setPreviousNode(new_node)
        self.__firstNode = new_node

    def insertBack(self, value):
        new_node = DoubleNode(value, None, self.__lastNode)
        if self.isEmpty():
            self.__firstNode = new_node
        else:
            self.__lastNode.setNextNode(new_node)
        self.__lastNode = new_node

    def insertAfter(self, value_to_add, after_value) -> None:
        current = self.find(after_value)
        if current:
            new_node = DoubleNode(value_to_add, current.getNextNode(), current)
            if current.getNextNode():
                current.getNextNode().setPreviousNode(new_node)
            else:
                self.__lastNode = new_node
            current.setNextNode(new_node)
            return True
        return False


    def deleteFirstNode(self):
        if self.isEmpty():
            raise Exception("List is empty")
        value = self.__firstNode.getValue()
        self.__firstNode = self.__firstNode.getnextNode()
        if self.__firstNode:
            self.__firstNode.seetPreviousNode(None)
        else:
            self.__lastNode = None
        return value
    
    def deleteLastNode(self):
        if self.isEmpty():
            raise Exception("List is empty")
        value = self.__lastNode.getValue()
        self.__lastNode = self.__lastNode.getPreviousNode()
        if self.__lastNode:
            self.__lastNode.setNextNode(None)
        else:
            self.__firstNode = None
        return value
    
    def deleteValue(self, value):
        current = self.find(value)
        if current is None:
            raise Exception("Value not found")
        if current.isFirst():
            return self.deleteFirstNode()
        if current.isLast():
            return self.deleteLastNode()
        prev_node = current.getPreviousNode()
        next_node = current.getNextNode()
        prev_node.setNextNode(next_node)
        next_node.setpreviousNode(prev_node)
        return current.getValue()


    def forwardTraverse(self):
        current = self.__firstNode
        while current:
            print(current.getValue())
            current = current.getNextNode

    def reverseTraverse(self):
        current = self.__lastNode
        while current:
            print(current.getValue())
            current = current.getPreviousNode()

    def __len__(self):
        count = 0
        current = self.__firstNode
        while current:
            count += 1
            current = current.getNextNode()
        return count
    
    def __str__(self):
        values = []
        current = self.__firstNode
        while current:
            values.append(str(current.getValue()))
            current - current.getnextNode()
        return "[" + "<->".join(values) + "']"
    
if __name__ == "__main__":
    pass