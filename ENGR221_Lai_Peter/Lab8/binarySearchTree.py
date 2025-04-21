"""
Binary Search Tree Implementation
Author: Peter Lai
Date: April 19, 2025

This file implements an unbalanced binary search tree (BST) with the following functionality:
- Insertion of key-value pairs
- Search and lookup operations
- Deletion of nodes
- Tree traversal (in-order)
- Finding successors
- Various utility methods (isEmpty, getRoot, etc.)

The implementation follows standard BST properties where for each node:
- All keys in the left subtree are less than the node's key
- All keys in the right subtree are greater than the node's key
- No duplicate keys are allowed (inserting same key updates value)
"""

class BinarySearchTree:
    """A class representing an unbalanced Binary Search Tree (BST).
    
    Attributes:
        __root (__Node): Private reference to the root node of the BST
    """

    def __init__(self):
        """Initialize an empty BST with no root node."""
        self.__root = None  # The root Node of this BST

    def insert(self, insertKey, insertValue):
        """Inserts the given key and value into the BST.
        
        Args:
            insertKey (any): The key to insert. Must be comparable.
            insertValue (any): The value to associate with the key.
            
        Note:
            If the key already exists, its value will be updated.
        """
        # Update the root to include the inserted node
        self.__root = self.__insertHelp(self.__root, insertKey, insertValue)
    
    def __insertHelp(self, node, insertKey, insertValue):
        """Recursive helper for insert(). Handles the actual node placement.
        
        Args:
            node (__Node): Current node being examined
            insertKey (any): Key to insert
            insertValue (any): Value to associate with key
            
        Returns:
            __Node: The node with new node properly inserted
            
        Note:
            Follows BST properties by comparing keys to determine left/right placement
        """
        # Base case - found empty spot, create new node
        if node == None:
            return self.__Node(insertKey, insertValue)
        
        # Recursive cases - navigate left or right based on key comparison
        if insertKey < node.key:
            node.left = self.__insertHelp(node.left, insertKey, insertValue)
        elif insertKey > node.key:
            node.right = self.__insertHelp(node.right, insertKey, insertValue)
        else:
            # Key exists - update the value
            node.value = insertValue
            
        return node

    def isEmpty(self):
        """Check if the BST contains any nodes.
        
        Returns:
            bool: True if tree is empty (no root), False otherwise
        """
        return self.__root is None
    
    def getRoot(self):
        """Get the root node of the BST.
        
        Returns:
            __Node: The root node object, or None if tree is empty
            
        Note:
            This provides access to the root node which contains references
            to the entire tree structure through left/right attributes
        """
        return self.__root

    def search(self, goalKey):
        """Public method to search for a key in the BST.
        
        Args:
            goalKey (any): The key to search for
            
        Returns:
            __Node: The node containing the key, or None if not found
        """
        return self.__searchHelp(self.__root, goalKey)

    def __searchHelp(self, node, goalKey):
        """Recursive helper that performs the actual BST search.
        
        Args:
            node (__Node): Current node being examined
            goalKey (any): Key we're searching for
            
        Returns:
            __Node: Node containing the key, or None if not found
            
        Note:
            Implements standard BST search algorithm:
            - If current node is None, key doesn't exist
            - If key matches current node, return node
            - If key is less, search left subtree
            - If key is greater, search right subtree
        """
        # Base case 1: key not found
        if node is None:
            return None
            
        # Base case 2: key found
        if goalKey == node.key:
            return node
            
        # Recursive cases
        if goalKey < node.key:
            return self.__searchHelp(node.left, goalKey)
        else:
            return self.__searchHelp(node.right, goalKey)

    def lookup(self, goal):
        """Get the value associated with a given key.
        
        Args:
            goal (any): The key to look up
            
        Returns:
            any: The value associated with the key
            
        Raises:
            Exception: If the key is not found in the tree
            
        Example:
            >>> bst = BinarySearchTree()
            >>> bst.insert(5, "five")
            >>> bst.lookup(5)
            "five"
        """
        node = self.search(goal)
        if node is None:
            raise Exception("Key not found in tree")
        return node.value

    def findSuccessor(self, subtreeRoot):
        """Find the successor (smallest key) in a subtree.
        
        Args:
            subtreeRoot (__Node): Root of the subtree to search
            
        Returns:
            __Node: The node with smallest key in the subtree
            
        Note:
            Used primarily for delete operation when a node has two children
        """
        return self.__findSuccessorHelp(subtreeRoot)
    
    def __findSuccessorHelp(self, node):
        """Recursive helper to find the smallest key in a subtree.
        
        Args:
            node (__Node): Current node being examined
            
        Returns:
            __Node: Node with smallest key in the subtree
            
        Note:
            The successor is found by going left until we can't anymore
        """
        # Base case: leftmost node found
        if node.left is None:
            return node
            
        # Recursive case: keep going left
        return self.__findSuccessorHelp(node.left)
    
    def delete(self, deleteKey):
        """Public method to delete a node with the given key.
        
        Args:
            deleteKey (any): The key to delete
            
        Returns:
            Result from __deleteHelp
            
        Raises:
            Exception: If the key is not found in the tree
        """
        if self.search(deleteKey):
            return self.__deleteHelp(self.__root, deleteKey)
        raise Exception("Key not in tree.")
    
    def __deleteHelp(self, node, deleteKey):
        """Recursive helper that handles the actual node deletion.
        
        Args:
            node (__Node): Current node being examined
            deleteKey (any): Key to delete
            
        Returns:
            __Node: The modified subtree with the specified node deleted
            
        Note:
            Handles three cases:
            1. Node has no children (simple removal)
            2. Node has one child (replace with child)
            3. Node has two children (find successor and replace)
        """
        # Base case: key not found
        if node is None:
            return None
        
        # Recursive search for the node to delete
        if deleteKey < node.key:
            node.left = self.__deleteHelp(node.left, deleteKey)
        elif deleteKey > node.key:
            node.right = self.__deleteHelp(node.right, deleteKey)
        else:
            # Case 1: No children
            if node.left is None and node.right is None:
                return None
            # Case 2: One child (right)
            elif node.left is None:
                return node.right
            # Case 2: One child (left)
            elif node.right is None:
                return node.left
            # Case 3: Two children
            else:
                successor = self.__findSuccessorHelp(node.right)
                node.key = successor.key
                node.value = successor.value
                node.right = self.__deleteHelp(node.right, successor.key)
        
        return node

    def traverse(self) -> None:
        """Perform an in-order traversal of the BST, printing each node.
        
        Note:
            In-order traversal visits nodes in sorted key order.
            Prints each node as it's visited.
        """
        self.__traverseHelp(self.__root)

    def __traverseHelp(self, node) -> None:
        """Recursive helper for in-order traversal.
        
        Args:
            node (__Node): Current node being visited
            
        Note:
            Traversal order:
            1. Recursively traverse left subtree
            2. Visit current node
            3. Recursively traverse right subtree
        """
        if node is not None:
            self.__traverseHelp(node.left)
            print(node)
            self.__traverseHelp(node.right)

    def __str__(self) -> str:
        """Generate a string representation of the BST.
        
        Returns:
            str: String showing tree structure in format:
            {(rootkey, rootval), {leftsubtree}, {rightsubtree}}
        """
        return self.__strHelp("", self.__root)
    
    def __strHelp(self, return_string, node) -> str:
        """Recursive helper for string representation.
        
        Args:
            return_string (str): Accumulator for final string
            node (__Node): Current node being processed
            
        Returns:
            str: Formatted string representation of subtree
            
        Note:
            Uses pre-order traversal to build the string
        """
        if node == None:
            return "None"
        return "{{{}, {}, {}}}".format(node, 
                                     self.__strHelp(return_string, node.left), 
                                     self.__strHelp(return_string, node.right))
            

    ##############
    # NODE CLASS #
    ##############

    class __Node:
        """Private inner class representing a node in the BST.
        
        Attributes:
            key (any): The node's key (used for ordering)
            value (any): The data stored in the node
            left (__Node): Reference to left child
            right (__Node): Reference to right child
        """

        def __init__(self, key, value, left=None, right=None):
            """Initialize a BST node with key and value.
            
            Args:
                key (any): The node's key
                value (any): The node's value
                left (__Node): Left child (default None)
                right (__Node): Right child (default None)
            """
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __str__(self):
            """String representation of the node.
            
            Returns:
                str: Formatted as "(key, value)"
            """
            return "({}, {})".format(self.key, self.value)
        
if __name__ == "__main__":
    # Example usage when run directly
    bst = BinarySearchTree()
    bst.insert(5, "five")
    bst.insert(3, "three")
    bst.insert(7, "seven")
    print("Tree structure:", bst)
    print("In-order traversal:")
    bst.traverse()