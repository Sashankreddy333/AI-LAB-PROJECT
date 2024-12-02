import pygame
from collections import deque


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
LBROWN = (172, 112, 61)
DBROWN = (121, 63, 13)
RED= (255, 0, 0)


class Tile:
    def __init__(self, row, col, width, totalRows):
        self.width = width
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = LBROWN
        self.totalRows = totalRows
        self.neighbors = []
        self.smell_intensity = 0  

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    
    def setStart(self):
        self.color = BLUE

    def isStart(self):
        return self.color == BLUE

    def setEnd(self):
        self.color = PURPLE

    def isEnd(self):
        return self.color == PURPLE

    def setWall(self):
        self.color = BLACK

    def isWall(self):
        return self.color == BLACK

    
    def setOpen(self):
        self.color = RED

    def isOpen(self):
        return self.color == RED

    def setClosed(self):
        self.color = GRAY

    def isClosed(self):
        return self.color == GRAY

    def reset(self):
        self.color = LBROWN
        self.smell_intensity = 0

    
    def getPos(self):
        return self.row, self.col

    def setPath(self):
        self.color = GREEN

    
    def initializeAllNeighbors(self, grid):
        self.neighbors = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  
            (-1, -1), (-1, 1), (1, -1), (1, 1)  
        ]
        for d_row, d_col in directions:
            n_row, n_col = self.row + d_row, self.col + d_col
            if 0 <= n_row < self.totalRows and 0 <= n_col < self.totalRows:
                neighbor = grid[n_row][n_col]
                if not neighbor.isWall():
                    self.neighbors.append(neighbor)

    def updateNeighbors(self, grid, allowDiagonal):
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].isWall():  
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isWall():  
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].isWall():  
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isWall():  
            self.neighbors.append(grid[self.row][self.col + 1])

        if allowDiagonal:
            if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].isWall():  
                self.neighbors.append(grid[self.row - 1][self.col - 1])
            if self.row > 0 and self.col < self.totalRows - 1 and not grid[self.row - 1][self.col + 1].isWall():  
                self.neighbors.append(grid[self.row - 1][self.col + 1])
            if self.row < self.totalRows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].isWall():  
                self.neighbors.append(grid[self.row + 1][self.col - 1])
            if self.row < self.totalRows - 1 and self.col < self.totalRows - 1 and not grid[self.row + 1][self.col + 1].isWall():  
                self.neighbors.append(grid[self.row + 1][self.col + 1])

    
    def setRotten(self):
        self.color = ORANGE
        self.smell_intensity = 8  

    def propagateSmell(self, grid):
        queue = deque([(self, self.smell_intensity)])
        visited = set()

        while queue:
            current_tile, current_intensity = queue.popleft()
            if current_tile in visited or current_intensity < 1:
                continue
            visited.add(current_tile)

            for neighbor in current_tile.neighbors:
                if neighbor.isWall() or neighbor.isStart() or neighbor.isEnd():
                    continue

                new_intensity = current_intensity / 2
                if new_intensity >= neighbor.smell_intensity and new_intensity >=1:
                    neighbor.smell_intensity += new_intensity-1
                    queue.append((neighbor, new_intensity))

        
        for row in grid:
            for tile in row:
                if tile.smell_intensity > 0:
                    gradient_factor = 1 - min(tile.smell_intensity / 8, 1)  

                
                    red = 255
                    green = int(165 + (200 - 165) * gradient_factor)  
                    blue = int((150 - 0) * gradient_factor)  

                    tile.color = (red, green, blue)

        print("Tiles with non-zero smell intensity:")
        for row in grid:
            for tile in row:
                if tile.smell_intensity > 0:
                    print(f"Tile at ({tile.row}, {tile.col}) - Smell Intensity: {tile.smell_intensity}")