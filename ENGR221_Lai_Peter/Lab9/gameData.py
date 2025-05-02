"""
Author: Peter Jayden Lai
Date: 5/1/2025
Description: Represents the current state of the game including board, snake, and food.
"""

from boardCell import BoardCell
from preferences import Preferences
import random
from enum import Enum, auto

class GameData:
    def __init__(self):
        # Dimensions of the board (in cells)
        self.__height = Preferences.NUM_CELLS_TALL
        self.__width = Preferences.NUM_CELLS_WIDE
        self.__freeCells = self.__height * self.__width
        self.__totalCells = self.__height * self.__width
        self.__currentMode = self.SnakeMode.GOING_EAST
        self.__board = self.createBoard()
        self.__foodCells = []
        self.__snakeCells = []
        self.__gameOver = False

    def createBoard(self):
        """ Populate the starting state of the board """
        board = [[BoardCell(row, col) for col in range(self.__width)] 
                for row in range(self.__height)]
        
        # Create walls around the edges
        for row in range(self.__height):
            board[row][0].becomeWall()
            board[row][self.__width-1].becomeWall()
            self.__freeCells -= 2
            
        for col in range(1, self.__width-1):
            board[0][col].becomeWall()
            board[self.__height-1][col].becomeWall()
            self.__freeCells -= 2

        return board
        
    def placeSnakeAtStartLocation(self):
        """ Place the snake in the upper left corner, facing east """
        head = self.getCell(1, 2)
        body = self.getCell(1, 1)
        head.becomeHead()
        body.becomeBody()
        self.__snakeCells.append(head)
        self.__snakeCells.append(body)
        self.__freeCells -= 2

    def inAIMode(self):
        """ Returns whether in AI mode """
        return self.__currentMode == self.SnakeMode.AI_MODE

    def getCell(self, row, col):
        """ Returns the cell at given row and column """
        if 0 <= row < self.__height and 0 <= col < self.__width:
            return self.__board[row][col]
        raise Exception(f"Invalid cell access: ({row}, {col})")
        
    def noFood(self):
        """ Returns whether there is food on the board """
        return len(self.__foodCells) == 0
    
    def addFood(self):
        """ Adds food to an open spot on the board """
        row = random.randrange(1, self.__height)
        col = random.randrange(1, self.__width)
        cell = self.getCell(row, col)

        if cell.isEmpty():
            cell.becomeFood()
            self.__foodCells.append(cell)
            self.__freeCells -= 1
        elif self.__freeCells / self.__totalCells > 0.3:
            self.addFood()

    # Neighbor methods
    def getNorthNeighbor(self, cell):
        """ Returns cell to the north """
        return self.getCell(cell.getRow()-1, cell.getCol())
        
    def getSouthNeighbor(self, cell):
        """ Returns cell to the south """
        return self.getCell(cell.getRow()+1, cell.getCol())
    
    def getEastNeighbor(self, cell):
        """ Returns cell to the east """
        return self.getCell(cell.getRow(), cell.getCol()+1)
    
    def getWestNeighbor(self, cell):
        """ Returns cell to the west """
        return self.getCell(cell.getRow(), cell.getCol()-1)
    
    def getNextCellInDir(self):
        """ Returns next cell in current direction """
        head = self.getSnakeHead()
        if self.__currentMode == self.SnakeMode.GOING_NORTH:
            return self.getNorthNeighbor(head)
        elif self.__currentMode == self.SnakeMode.GOING_SOUTH:
            return self.getSouthNeighbor(head)
        elif self.__currentMode == self.SnakeMode.GOING_EAST:
            return self.getEastNeighbor(head)
        elif self.__currentMode == self.SnakeMode.GOING_WEST:
            return self.getWestNeighbor(head)
        return head

    # Snake movement helpers
    def moveSnake(self, nextCell):
        """ Moves snake to next cell """
        if nextCell.isFood():
            self.__foodCells.remove(nextCell)
            self.__snakeCells[0].becomeBody()
            nextCell.becomeHead()
            self.__snakeCells.insert(0, nextCell)
        else:
            self.__snakeCells[0].becomeBody()
            nextCell.becomeHead()
            self.__snakeCells.insert(0, nextCell)
            tail = self.__snakeCells.pop()
            tail.becomeEmpty()
            self.__freeCells += 1

    # Direction setters
    def setDirectionNorth(self):
        if self.__currentMode != self.SnakeMode.GOING_SOUTH:
            self.__currentMode = self.SnakeMode.GOING_NORTH

    def setDirectionSouth(self):
        if self.__currentMode != self.SnakeMode.GOING_NORTH:
            self.__currentMode = self.SnakeMode.GOING_SOUTH

    def setDirectionEast(self):
        if self.__currentMode != self.SnakeMode.GOING_WEST:
            self.__currentMode = self.SnakeMode.GOING_EAST

    def setDirectionWest(self):
        if self.__currentMode != self.SnakeMode.GOING_EAST:
            self.__currentMode = self.SnakeMode.GOING_WEST

    def setAIMode(self):
        self.__currentMode = self.SnakeMode.AI_MODE

    # Access methods
    def getSnakeHead(self):
        return self.__snakeCells[0]
    
    def getSnakeTail(self):
        return self.__snakeCells[-1]
    
    def getSnakeNeck(self):
        return self.__snakeCells[1]

    def setGameOver(self):
        self.__gameOver = True

    def getGameOver(self):
        return self.__gameOver

    def resetCellsForSearch(self):
        for row in self.__board:
            for cell in row:
                cell.clearSearchInfo()

    class SnakeMode(Enum):
        GOING_NORTH = auto()
        GOING_SOUTH = auto()
        GOING_EAST = auto()
        GOING_WEST = auto()
        AI_MODE = auto()