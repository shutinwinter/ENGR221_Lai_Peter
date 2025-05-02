"""
Author: Peter Jayden Lai 
Date: 5/1/2025
Description: Creates and displays the graphics based on current state of board.
"""

import pygame
from preferences import Preferences

class BoardDisplay:
    def __init__(self):
        # The display where the board is drawn
        self.__display = pygame.display.set_mode((Preferences.GAME_BOARD_WIDTH, Preferences.GAME_BOARD_HEIGHT))
        # Image to show as the "head"
        self.headImage = None

    def updateGraphics(self, gameData):
        """ Re-draws the board, food, and snake based on the current state of the board """
        
        # Clear the board
        self.clear()

        # Draw all cells on the board
        for row in range(gameData._GameData__height):
            for col in range(gameData._GameData__width):
                cell = gameData.getCell(row, col)
                self.drawSquare(cell)
                cell_size = 20  #Makes window larger

        # Draw the game over message if game is over
        if gameData.getGameOver():
            self.displayGameOver()

        # Update the display
        pygame.display.update()

    def clear(self):
        """ Resets the background of the display """
        self.__display.fill(Preferences.COLOR_BACKGROUND)

    def drawSquare(self, cell):
        """ Draws a cell-sized square at the given location """
        row = cell.getRow()
        col = cell.getCol()

        if cell.isHead() and self.headImage:
            self.drawImage(row, col, self.headImage)
        else:
            cellColor = cell.getCellColor()
            pygame.draw.rect(self.__display, cellColor, 
                           [col*Preferences.CELL_SIZE, row*Preferences.CELL_SIZE, 
                            Preferences.CELL_SIZE, Preferences.CELL_SIZE])

    def drawImage(self, row, col, image):
        """ Displays an image at the given cell location """
        image = image.convert_alpha()
        image = pygame.transform.scale(image, (Preferences.CELL_SIZE, Preferences.CELL_SIZE))
        imageRect = image.get_rect()
        imageRect.center = ((col*Preferences.CELL_SIZE) + (Preferences.CELL_SIZE / 2),
                          (row*Preferences.CELL_SIZE) + (Preferences.CELL_SIZE / 2))
        self.__display.blit(image, imageRect)

    def displayGameOver(self):
        """ Displays the game over message """
        font = Preferences.GAME_OVER_FONT
        text = font.render(Preferences.GAME_OVER_TEXT, True, Preferences.GAME_OVER_COLOR)
        textRect = text.get_rect()
        textRect.center = (Preferences.GAME_OVER_X, Preferences.GAME_OVER_Y)
        self.__display.blit(text, textRect)