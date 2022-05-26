from .constants import BLACK, SQUARE_SIZE, WHITE, RED, CROWN
import pygame

class Piece:

    PADDING = 15
    BORDER = 0

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()
    
    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def transform_to_king(self):
        self.king = True

    def draw(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, RED, (self.x, self.y), radius + self.BORDER)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2 , self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()
        
    def __repr__(self):
        return str(self.row) + str(self.col)