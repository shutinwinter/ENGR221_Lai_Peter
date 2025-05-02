"""
Author: Peter Jayden Lai
Date: 5/1/2025
Description: The Controller of the game, handling key presses and game logic.
"""

from preferences import Preferences
from gameData import GameData
from boardDisplay import BoardDisplay
import pygame
from enum import Enum
from queue import Queue

class Controller():
    def __init__(self):
        self.__data = GameData()
        self.__display = BoardDisplay()
        self.__numCycles = 0

        try:
            pygame.mixer.init()
            self.__audioEat = pygame.mixer.Sound(Preferences.EAT_SOUND)
            self.__display.headImage = pygame.image.load(Preferences.HEAD_IMAGE)
        except:
            print("Problem loading audio/images")
            self.__audioEat = None

        self.startNewGame()
        
    def startNewGame(self):
        """ Initializes the board for a new game """
        self.__data.placeSnakeAtStartLocation()

    def gameOver(self):
        """ Indicates the player has lost """
        self.__data.setGameOver()

    def run(self):
        """ Main game loop """
        clock = pygame.time.Clock()
        while not self.__data.getGameOver():
            self.cycle()
            clock.tick(Preferences.SLEEP_TIME)

    def cycle(self):
        """ Main behavior of each time step """
        self.checkKeypress()
        self.updateSnake()
        self.updateFood()
        self.__numCycles += 1
        self.__display.updateGraphics(self.__data)

    def checkKeypress(self):
        """ Handle keyboard input """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameOver()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.Keypress.REVERSE.value:
                    self.reverseSnake()
                elif event.key in self.Keypress.AI.value:
                    self.__data.setAIMode()
                elif event.key in self.Keypress.UP.value:
                    self.__data.setDirectionNorth()
                elif event.key in self.Keypress.DOWN.value:
                    self.__data.setDirectionSouth()
                elif event.key in self.Keypress.LEFT.value:
                    self.__data.setDirectionWest()
                elif event.key in self.Keypress.RIGHT.value:
                    self.__data.setDirectionEast()

    def updateSnake(self):
        """ Move the snake forward one step """
        if self.__numCycles % Preferences.REFRESH_RATE == 0:
            nextCell = (self.getNextCellFromBFS() if self.__data.inAIMode() 
                        else self.__data.getNextCellInDir())
            try:
                self.advanceSnake(nextCell)
            except:
                print("Failed to advance snake")

    def advanceSnake(self, nextCell):
        """ Update game state to move snake's head to nextCell """
        if nextCell.isWall() or nextCell.isBody():
            self.gameOver()
        elif nextCell.isFood():
            self.playSound_eat()
            self.__data.moveSnake(nextCell)
            self.__data.addFood()
        elif nextCell.isEmpty():
            self.__data.moveSnake(nextCell)

    def updateFood(self):
        """ Add food periodically """
        if self.__data.noFood() or (self.__numCycles % Preferences.FOOD_ADD_RATE == 0):
            self.__data.addFood()

    def getNextCellFromBFS(self):
        """ Uses BFS to find next step toward closest food """
        self.__data.resetCellsForSearch()
        cellsToSearch = Queue()
        head = self.__data.getSnakeHead()
        head.setAddedToSearchList()
        cellsToSearch.put(head)

        while not cellsToSearch.empty():
            current = cellsToSearch.get()
            if current.isFood():
                return self.getFirstCellInPath(current)
            
            for neighbor in self.__data.getNeighbors(current):
                if (not neighbor.alreadyAddedToSearchList() and 
                    (neighbor.isEmpty() or neighbor.isFood())):
                    neighbor.setAddedToSearchList()
                    neighbor.setParent(current)
                    cellsToSearch.put(neighbor)

        return self.__data.getRandomNeighbor(head)

    def getFirstCellInPath(self, foodCell):
        """ Returns first cell in path from head to food """
        path = []
        current = foodCell
        while current.getParent() != self.__data.getSnakeHead():
            current = current.getParent()
        return current

    def reverseSnake(self):
        """ Reverses snake direction """
        snake = self.__data._GameData__snakeCells
        if len(snake) < 2:
            return
            
        # Reverse the body
        body = snake[1:-1]
        body.reverse()
        snake[1:-1] = body
        
        # Update head and tail
        old_head = snake[0]
        old_tail = snake[-1]
        old_head.becomeBody()
        old_tail.becomeHead()
        snake[0], snake[-1] = snake[-1], snake[0]
        
        # Update direction
        neck = snake[1]
        head = snake[0]
        if neck.getRow() < head.getRow():
            self.__data.setDirectionNorth()
        elif neck.getRow() > head.getRow():
            self.__data.setDirectionSouth()
        elif neck.getCol() < head.getCol():
            self.__data.setDirectionWest()
        elif neck.getCol() > head.getCol():
            self.__data.setDirectionEast()

    def playSound_eat(self):
        """ Plays eating sound """
        if self.__audioEat:
            pygame.mixer.Sound.play(self.__audioEat)
            pygame.mixer.music.stop()

    class Keypress(Enum):
        UP = pygame.K_i, pygame.K_UP
        DOWN = pygame.K_k, pygame.K_DOWN
        LEFT = pygame.K_j, pygame.K_LEFT
        RIGHT = pygame.K_l, pygame.K_RIGHT
        REVERSE = pygame.K_r,
        AI = pygame.K_a,

if __name__ == "__main__":
    Controller().run()