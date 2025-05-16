"""
Author: Peter Jayden Lai
Date: 5/1/2025
Description: Stores constant variables for the game configuration.
"""

import pygame

class Preferences:
    pygame.init()

    # Timing
    REFRESH_RATE = 1
    FOOD_ADD_RATE = 100    
    SLEEP_TIME = 20

    # Sizing
    NUM_CELLS_WIDE = 50
    NUM_CELLS_TALL = 30 
    CELL_SIZE = 20  # Increased from 1 for better visibility
    GAME_BOARD_WIDTH = NUM_CELLS_WIDE * CELL_SIZE
    GAME_BOARD_HEIGHT = NUM_CELLS_TALL * CELL_SIZE

    # Colors
    COLOR_BACKGROUND = pygame.Color('lavender')
    COLOR_WALL = pygame.Color('gray40')
    COLOR_FOOD = pygame.Color('firebrick')
    COLOR_EMPTY = pygame.Color('lavender')
    COLOR_HEAD = pygame.Color('darkorchid4')
    COLOR_BODY = pygame.Color('darkorchid1')

    # Game over display
    GAME_OVER_X = GAME_BOARD_WIDTH / 2
    GAME_OVER_Y = GAME_BOARD_HEIGHT / 2
    GAME_OVER_COLOR = pygame.Color('navy')
    GAME_OVER_FONT = pygame.font.SysFont("arial", 40)
    GAME_OVER_TEXT = "Game Over"

    # Graphics and Audio
    HEAD_IMAGE = "trainer.png"
    EAT_SOUND = "meow.wav"