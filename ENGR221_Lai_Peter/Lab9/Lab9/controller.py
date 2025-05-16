"""
Author: Peter Jayden Lai
Date: May 16, 2025
Description: The Controller of the game, handling key presses, game logic, AI mode,
             snake reversal, scoring, game speed dynamics, and obstacle generation.
"""

from preferences import Preferences
from gameData import GameData
from boardDisplay import BoardDisplay
import pygame
from enum import Enum
from queue import Queue
import random

class Controller():
    def __init__(self):
        self.__data = GameData()  # Holds game state and logic
        self.__display = BoardDisplay()  # Handles drawing the board
        self.__numCycles = 0  # Tracks game ticks
        self.__score = 0  # Tracks score
        self.__lives = 3  # Lives before game over

        try:
            pygame.mixer.init()  # Initialize audio
            self.__audioEat = pygame.mixer.Sound(Preferences.EAT_SOUND)  # Load eat sound
            self.__display.headImage = pygame.image.load(Preferences.HEAD_IMAGE)  # Load snake head image
        except:
            print("Problem loading audio/images")
            self.__audioEat = None

        self.startNewGame()

    def startNewGame(self):
        """ Initializes the board for a new game """
        self.__data.placeSnakeAtStartLocation()
        self.__data.addFood()
        self.__score = 0
        self.__numCycles = 0
        self.__lives = 3
        self.addObstacles()  # Add initial obstacles

    def gameOver(self):
        """ Ends the game """
        self.__data.setGameOver()

    def run(self):
        """ Main game loop """
        clock = pygame.time.Clock()
        while not self.__data.getGameOver():
            self.cycle()
            clock.tick(Preferences.SLEEP_TIME + self.__score // 5)  # Game speeds up with score

    def cycle(self):
        """ Main behavior of each game tick """
        self.checkKeypress()
        self.updateSnake()
        self.updateFood()
        self.__numCycles += 1
        self.__display.updateGraphics(self.__data, self.__score, self.__lives)  # Pass score and lives to display

    def checkKeypress(self):
        """ Process user keyboard inputs """
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
        """ Move the snake one cell in its current direction or via AI """
        if self.__numCycles % Preferences.REFRESH_RATE == 0:
            nextCell = (self.getNextCellFromBFS() if self.__data.inAIMode() 
                        else self.__data.getNextCellInDir())
            try:
                self.advanceSnake(nextCell)
            except:
                print("Failed to advance snake")

    def advanceSnake(self, nextCell):
        """ Advance the snake into the next cell, handling collisions and food """
        if nextCell.isWall() or nextCell.isBody():
            self.__lives -= 1
            if self.__lives <= 0:
                self.gameOver()
            else:
                self.__data.placeSnakeAtStartLocation()
        elif nextCell.isFood():
            self.playSound_eat()
            self.__data.moveSnake(nextCell)
            self.__data.addFood()
            self.__score += 1
        elif nextCell.isEmpty():
            self.__data.moveSnake(nextCell)

    def updateFood(self):
        """ Periodically add food to the board """
        if self.__data.noFood() or (self.__numCycles % Preferences.FOOD_ADD_RATE == 0):
            self.__data.addFood()

    def getNextCellFromBFS(self):
        """ 
        Uses BFS to find the shortest path to food and returns the next cell 
        
        This method implements a breadth-first search algorithm to find the shortest
        path from the snake's head to the nearest food. It returns the first cell
        in that path, which is the direction the snake should move next.
        """
        # Reset all cells' search metadata
        self.__data.resetCellsForSearch()
        
        # Initialize queue with the snake's head
        cellsToSearch = Queue()
        head = self.__data.getSnakeHead()
        head.setAddedToSearchList()
        cellsToSearch.put(head)
        
        # BFS algorithm to find path to food
        while not cellsToSearch.empty():
            current = cellsToSearch.get()
            
            # If we've found food, get the first cell in the path back to the head
            if current.isFood():
                return self.getFirstCellInPath(current)
            
            # Check all four neighboring cells
            neighbors = [
                self.__data.getNorthNeighbor(current),
                self.__data.getSouthNeighbor(current),
                self.__data.getEastNeighbor(current),
                self.__data.getWestNeighbor(current)
            ]
            
            # Add valid neighbors to the search queue
            for neighbor in neighbors:
                if (not neighbor.alreadyAddedToSearchList() and 
                    (neighbor.isEmpty() or neighbor.isFood())):
                    neighbor.setAddedToSearchList()
                    neighbor.setParent(current)
                    cellsToSearch.put(neighbor)
        
        # If no path to food is found, move in a random valid direction
        return self.getRandomValidMove(head)

    def getRandomValidMove(self, head):
        """
        Returns a random valid neighboring cell when no path to food is found
        
        This helper method finds a neighbor that is neither a wall nor part of the snake's body
        """
        neighbors = [
            self.__data.getNorthNeighbor(head),
            self.__data.getSouthNeighbor(head),
            self.__data.getEastNeighbor(head),
            self.__data.getWestNeighbor(head)
        ]
        
        valid_neighbors = [n for n in neighbors if not (n.isWall() or n.isBody())]
        
        if valid_neighbors:
            return random.choice(valid_neighbors)
        return head  # If no valid moves, return the head (game will end)

    def getFirstCellInPath(self, foodCell):
        """
        Walks back from food to head and returns the first move
        
        This method reconstructs the path from the food cell back to the
        snake's head and returns the first cell in that path (the cell
        immediately after the head).
        """
        # Start at the food cell and work backwards using parent pointers
        current = foodCell
        
        # Keep going until we find the cell that is a direct neighbor of the head
        while current.getParent() != self.__data.getSnakeHead():
            current = current.getParent()
            # Safety check in case there's an issue with the path
            if current is None:
                return self.getRandomValidMove(self.__data.getSnakeHead())
                
        # Return the first cell in the path from head to food
        return current

    def reverseSnake(self):
        """ 
        Reverses the snake's direction and movement
        
        This method flips the snake so the head becomes the tail and vice versa,
        and reverses the body segments in between.
        """
        # Get the snake cells list from the game data
        snake = self.__data._GameData__snakeCells
        
        # If snake is too short, nothing to reverse
        if len(snake) < 2:
            return

        # Reverse the body segments (everything except head and tail)
        body = snake[1:-1]
        body.reverse()
        snake[1:-1] = body

        # Swap head and tail cells
        old_head = snake[0]
        old_tail = snake[-1]
        old_head.becomeBody()  # Former head becomes a body segment
        old_tail.becomeHead()  # Former tail becomes the new head
        snake[0], snake[-1] = snake[-1], snake[0]  # Swap positions in the list

        # Set the direction based on the new head and neck positions
        neck = snake[1]
        head = snake[0]
        
        # Determine direction based on relative position of head and neck
        if neck.getRow() < head.getRow():
            self.__data.setDirectionNorth()
        elif neck.getRow() > head.getRow():
            self.__data.setDirectionSouth()
        elif neck.getCol() < head.getCol():
            self.__data.setDirectionWest()
        elif neck.getCol() > head.getCol():
            self.__data.setDirectionEast()

    def playSound_eat(self):
        """ Play a sound when the snake eats food """
        if self.__audioEat:
            pygame.mixer.Sound.play(self.__audioEat)
            pygame.mixer.music.stop()

    def addObstacles(self):
        """ Randomly place wall obstacles on the board at the start of the game """
        for _ in range(10):
            row = random.randint(1, self.__data.getHeight() - 2)  # Avoid borders
            col = random.randint(1, self.__data.getWidth() - 2)   # Avoid borders
            cell = self.__data.getCell(row, col)
            
            # Don't place obstacles on the snake's starting position
            center_row = self.__data.getHeight() // 2
            center_col = self.__data.getWidth() // 2
            
            # Check if we're too close to starting position (3 cells in any direction)
            if (abs(row - center_row) > 3 or abs(col - center_col) > 3) and cell.isEmpty():
                cell.becomeWall()

    class Keypress(Enum):
        UP = pygame.K_i, pygame.K_UP
        DOWN = pygame.K_k, pygame.K_DOWN
        LEFT = pygame.K_j, pygame.K_LEFT
        RIGHT = pygame.K_l, pygame.K_RIGHT
        REVERSE = pygame.K_r,
        AI = pygame.K_a,

if __name__ == "__main__":
    Controller().run()
