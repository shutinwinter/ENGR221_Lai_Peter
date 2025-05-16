"""
Author: Peter Jayden Lai
Date: May 16, 2025
Description: Handles the game data and logic, including snake movement,
             food placement, and game state.
"""

from boardCell import BoardCell
from preferences import Preferences
from enum import Enum
import random

class GameData:
    def __init__(self):
        """
        Initializes the game data including the board, snake, and game state.
        """
        self.__gameOver = False
        self.__aiMode = False
        self.__direction = self.Direction.EAST
        self.__snakeCells = []  # List of BoardCells representing the snake
        
        # Create the game board
        self.__board = []
        for row in range(Preferences.NUM_CELLS_TALL):
            rowList = []
            for col in range(Preferences.NUM_CELLS_WIDE):
                cell = BoardCell(row, col)
                rowList.append(cell)
            self.__board.append(rowList)
        
        # Add border walls around the edges of the board
        self.__addBorderWalls()

    def __addBorderWalls(self):
        """
        Adds wall cells around the border of the game board.
        """
        height = self.getHeight()
        width = self.getWidth()
        
        # Add top and bottom walls
        for col in range(width):
            self.__board[0][col].becomeWall()
            self.__board[height-1][col].becomeWall()
        
        # Add left and right walls (excluding corners which are already set)
        for row in range(1, height-1):
            self.__board[row][0].becomeWall()
            self.__board[row][width-1].becomeWall()

    def placeSnakeAtStartLocation(self):
        """
        Places the snake at its starting location in the middle of the board.
        """
        # Clear any existing snake cells
        for cell in self.__snakeCells:
            cell.becomeEmpty()
        self.__snakeCells.clear()
        
        # Place snake at the center of the board
        centerRow = self.getHeight() // 2
        centerCol = self.getWidth() // 2
        
        # Create initial snake (3 cells long, pointing east)
        head = self.__board[centerRow][centerCol]
        body1 = self.__board[centerRow][centerCol-1]
        body2 = self.__board[centerRow][centerCol-2]
        
        head.becomeHead()
        body1.becomeBody()
        body2.becomeBody()
        
        self.__snakeCells = [head, body1, body2]
        self.__direction = self.Direction.EAST

    def addFood(self):
        """
        Adds a food cell at a random empty location on the board.
        """
        emptyCells = []
        
        # Find all empty cells on the board
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                cell = self.__board[row][col]
                if cell.isEmpty():
                    emptyCells.append(cell)
        
        # Place food in a random empty cell if any exist
        if emptyCells:
            randomCell = random.choice(emptyCells)
            randomCell.becomeFood()

    def noFood(self):
        """
        Checks if there's no food on the board.
        
        Returns:
        True if there's no food on the board, False otherwise
        """
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                if self.__board[row][col].isFood():
                    return False
        return True

    def moveSnake(self, nextCell):
        """
        Moves the snake one cell in the current direction.
        
        Parameters:
        nextCell - The next cell the snake's head will move into
        """
        # Move snake by adding new head and either removing tail or growing
        oldHead = self.__snakeCells[0]
        oldHead.becomeBody()
        
        nextCell.becomeHead()
        self.__snakeCells.insert(0, nextCell)
        
        # If the next cell isn't food, remove the tail to maintain snake length
        if not nextCell.isFood():
            tailCell = self.__snakeCells.pop()
            tailCell.becomeEmpty()

    def getNextCellInDir(self):
        """
        Gets the next cell in the snake's current direction.
        
        Returns:
        The BoardCell that the snake would move into given its current direction
        """
        head = self.__snakeCells[0]
        
        if self.__direction == self.Direction.NORTH:
            return self.getNorthNeighbor(head)
        elif self.__direction == self.Direction.SOUTH:
            return self.getSouthNeighbor(head)
        elif self.__direction == self.Direction.EAST:
            return self.getEastNeighbor(head)
        else:  # WEST
            return self.getWestNeighbor(head)

    def getNeighbors(self, cell):
        """
        Gets all neighboring cells of the given cell.
        
        Parameters:
        cell - The cell to get neighbors for
        
        Returns:
        A list of the neighboring cells (north, south, east, west)
        """
        return [
            self.getNorthNeighbor(cell),
            self.getSouthNeighbor(cell),
            self.getEastNeighbor(cell),
            self.getWestNeighbor(cell)
        ]

    def getNorthNeighbor(self, cell):
        """
        Gets the cell to the north of the given cell.
        
        Parameters:
        cell - The reference cell
        
        Returns:
        The cell directly north of the given cell
        """
        row = cell.getRow() - 1
        col = cell.getCol()
        return self.__board[row][col]

    def getSouthNeighbor(self, cell):
        """
        Gets the cell to the south of the given cell.
        
        Parameters:
        cell - The reference cell
        
        Returns:
        The cell directly south of the given cell
        """
        row = cell.getRow() + 1
        col = cell.getCol()
        return self.__board[row][col]

    def getEastNeighbor(self, cell):
        """
        Gets the cell to the east of the given cell.
        
        Parameters:
        cell - The reference cell
        
        Returns:
        The cell directly east of the given cell
        """
        row = cell.getRow()
        col = cell.getCol() + 1
        return self.__board[row][col]

    def getWestNeighbor(self, cell):
        """
        Gets the cell to the west of the given cell.
        
        Parameters:
        cell - The reference cell
        
        Returns:
        The cell directly west of the given cell
        """
        row = cell.getRow()
        col = cell.getCol() - 1
        return self.__board[row][col]

    def resetCellsForSearch(self):
        """
        Resets all cells' search-related information for BFS.
        """
        for row in range(self.getHeight()):
            for col in range(self.getWidth()):
                self.__board[row][col].clearSearchInfo()

    def getHeight(self):
        """
        Returns the height of the game board (number of rows).
        
        Returns:
        The number of rows in the game board
        """
        return Preferences.NUM_CELLS_TALL

    def getWidth(self):
        """
        Returns the width of the game board (number of columns).
        
        Returns:
        The number of columns in the game board
        """
        return Preferences.NUM_CELLS_WIDE

    def getCell(self, row, col):
        """
        Returns the cell at the specified position.
        
        Parameters:
        row - The row of the cell
        col - The column of the cell
        
        Returns:
        The BoardCell at the specified position
        """
        if 0 <= row < self.getHeight() and 0 <= col < self.getWidth():
            return self.__board[row][col]
        return None

    def setGameOver(self):
        """Sets the game state to game over."""
        self.__gameOver = True

    def getGameOver(self):
        """
        Returns True if the game is over, False otherwise.
        
        Returns:
        The game over state
        """
        return self.__gameOver

    def setAIMode(self):
        """Toggles AI mode on/off."""
        self.__aiMode = not self.__aiMode

    def inAIMode(self):
        """
        Returns True if the game is in AI mode, False otherwise.
        
        Returns:
        The AI mode state
        """
        return self.__aiMode

    def setDirectionNorth(self):
        """Sets the snake's direction to north if not moving south."""
        if self.__snakeCells[0].getRow() <= self.__snakeCells[1].getRow():
            self.__direction = self.Direction.NORTH

    def setDirectionSouth(self):
        """Sets the snake's direction to south if not moving north."""
        if self.__snakeCells[0].getRow() >= self.__snakeCells[1].getRow():
            self.__direction = self.Direction.SOUTH

    def setDirectionEast(self):
        """Sets the snake's direction to east if not moving west."""
        if self.__snakeCells[0].getCol() >= self.__snakeCells[1].getCol():
            self.__direction = self.Direction.EAST

    def setDirectionWest(self):
        """Sets the snake's direction to west if not moving east."""
        if self.__snakeCells[0].getCol() <= self.__snakeCells[1].getCol():
            self.__direction = self.Direction.WEST

    def getSnakeHead(self):
        """
        Returns the cell representing the snake's head.
        
        Returns:
        The BoardCell that is the snake's head (first element in __snakeCells)
        """
        if self.__snakeCells:
            return self.__snakeCells[0]
        return None

    def getSnakeBody(self):
        """
        Returns the list of cells representing the snake's body (excluding head).
        
        Returns:
        A list of BoardCells that make up the snake's body
        """
        if len(self.__snakeCells) > 1:
            return self.__snakeCells[1:]
        return []

    class Direction(Enum):
        """Enumeration of possible snake movement directions."""
        NORTH = 0
        SOUTH = 1
        EAST = 2
        WEST = 3
