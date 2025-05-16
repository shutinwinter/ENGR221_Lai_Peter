"""
Author: Peter Jayden Lai
Date: May 16, 2025
Description: Handles the display of the game board and UI elements including
             the snake, food, walls, score, and lives display.
"""

import pygame
from preferences import Preferences

class BoardDisplay:
    def __init__(self):
        """
        Initializes the display for the game.
        """
        # Initialize pygame and set up the display
        pygame.init()
        
        # Calculate the total window size (board + score area)
        self.scoreAreaHeight = 60  # Height reserved for displaying score and lives
        self.windowWidth = Preferences.GAME_BOARD_WIDTH
        self.windowHeight = Preferences.GAME_BOARD_HEIGHT + self.scoreAreaHeight
        
        # Create the window with the calculated dimensions
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("Snake Game")
        
        # Load font for displaying score and lives
        self.font = pygame.font.SysFont('arial', 24)
        
        # Variable for snake head image (will be set in Controller if available)
        self.headImage = None
        
        # Initialize special effects variables
        self.pulse_effect = 0
        self.pulse_direction = 1

    def updateGraphics(self, gameData, score, lives):
        """
        Updates the game display based on the current game state.
        
        Parameters:
        gameData - The GameData object containing the current game state
        score - The current player score
        lives - The number of lives remaining
        """
        # Fill background
        self.window.fill(Preferences.COLOR_BACKGROUND)
        
        # Draw the board (walls, food, snake)
        self.drawBoard(gameData)
        
        # Draw score area
        self.drawScoreArea(score, lives)
        
        # Update display with all drawn elements
        pygame.display.update()
        
        # Update special effects
        self.updateEffects()

    def drawBoard(self, gameData):
        """
        Draws the game board with all elements (walls, food, snake).
        
        Parameters:
        gameData - The GameData object containing the current game state
        """
        # Draw each cell on the board
        for row in range(gameData.getHeight()):
            for col in range(gameData.getWidth()):
                cell = gameData.getCell(row, col)
                self.drawCell(cell, row, col)
        
        # Draw game over message if game is over
        if gameData.getGameOver():
            self.drawGameOver()

    def drawCell(self, cell, row, col):
        """
        Draws a single cell on the game board.
        
        Parameters:
        cell - The BoardCell to draw
        row - The row of the cell
        col - The column of the cell
        """
        # Calculate cell position
        x = col * Preferences.CELL_SIZE
        y = row * Preferences.CELL_SIZE
        
        # Get cell color based on its type
        color = cell.getCellColor()
        
        # Apply pulse effect to food
        if cell.isFood():
            color = self.applyPulseEffect(color)
        
        # Draw the cell as a rectangle
        pygame.draw.rect(
            self.window, 
            color, 
            (x, y, Preferences.CELL_SIZE, Preferences.CELL_SIZE)
        )
        
        # If it's the snake's head and we have an image, draw it
        if cell.isHead() and self.headImage:
            # Scale image to fit cell size
            scaled_image = pygame.transform.scale(
                self.headImage, 
                (Preferences.CELL_SIZE, Preferences.CELL_SIZE)
            )
            self.window.blit(scaled_image, (x, y))

    def drawScoreArea(self, score, lives):
        """
        Draws the score area with current score and lives.
        
        Parameters:
        score - The current player score
        lives - The number of lives remaining
        """
        # Score area starts after the game board
        score_area_y = Preferences.GAME_BOARD_HEIGHT
        
        # Fill score area with a different color
        pygame.draw.rect(
            self.window,
            (50, 50, 50),  # Dark grey background for score area
            (0, score_area_y, self.windowWidth, self.scoreAreaHeight)
        )
        
        # Render score text
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        self.window.blit(score_text, (20, score_area_y + 20))
        
        # Render lives text
        lives_text = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        self.window.blit(lives_text, (self.windowWidth - 120, score_area_y + 20))

    def drawGameOver(self):
        """
        Draws the game over message in the center of the screen.
        """
        # Create a semi-transparent overlay
        overlay = pygame.Surface((Preferences.GAME_BOARD_WIDTH, Preferences.GAME_BOARD_HEIGHT))
        overlay.set_alpha(180)  # 70% opacity
        overlay.fill((0, 0, 0))  # Black overlay
        self.window.blit(overlay, (0, 0))
        
        # Create game over text
        game_over_render = Preferences.GAME_OVER_FONT.render(
            Preferences.GAME_OVER_TEXT, 
            True, 
            Preferences.GAME_OVER_COLOR
        )
        
        # Get text rect for centering
        game_over_rect = game_over_render.get_rect(
            center=(Preferences.GAME_OVER_X, Preferences.GAME_OVER_Y)
        )
        
        # Draw the game over text
        self.window.blit(game_over_render, game_over_rect)

    def updateEffects(self):
        """
        Updates special effects like pulsing for food items.
        """
        # Update pulse effect for food
        self.pulse_effect += self.pulse_direction
        
        # Reverse direction when reaching limits
        if self.pulse_effect > 50:
            self.pulse_direction = -1
        elif self.pulse_effect < 0:
            self.pulse_direction = 1

    def applyPulseEffect(self, color):
        """
        Applies a pulsing effect to a color.
        
        Parameters:
        color - The base color to apply pulsing effect to
        
        Returns:
        The modified color with pulsing effect applied
        """
        # Calculate pulse intensity for each channel (r, g, b)
        r = min(255, color[0] + self.pulse_effect // 2)
        g = min(255, color[1] + self.pulse_effect // 4)
        b = min(255, color[2] + self.pulse_effect // 4)
        
        return (r, g, b)
