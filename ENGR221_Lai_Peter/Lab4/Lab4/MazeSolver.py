"""
Name: Peter Lai
Description: Solving Mazes
"""
from SearchStructures import Stack, Queue
from Maze import Maze

class MazeSolver:
    # Constructor
    # Inputs:
    #   maze: The maze to solve (Maze)
    #   searchStructure: The search structure class to use (Stack or Queue)
    def __init__(self, maze, searchStructure):
        self.maze = maze             # The maze to solve
        self.ss = searchStructure()  # Initialize a searchStructure object

    def tileIsVisitable(self, row:int, col:int) -> bool:
        if 0 <= row < self.maze.num_rows and 0 <= self.maze.num_cols:
            tile = self.maxe.contents[row][col]
            return not tile.isWall() and not tile.visited
        return False
    
    def resetVisited(self):
        for row in self.maze.contents:
            for title in row:
                title.visited = False
                title.setPrevious(None)

    def solve(self):
        self.resetVisited()
        self.ss.add(self.maze.start)

        while not self.ss.isEmpty():
            current = self.ss.remove()
            current.visited = True

            if current == self.maze.goal:
                return current
            
            row, col = current.getRow(), current.getCol()
            directions = [(-1,0),(1,0),(0,1),(0,-1)] #N, S, E, W

            for dr, dc in directions:
                if self.tileIsVisitable(row + dr, col + dc):
                    neighbor = self.maze.contents[row + dr][col + dc]
                    neighbor.setPrevious(current)
                    self.ss.add(neighbor)
        
        return None

    def getPath(self):
        path = []
        tile = self.maze.goal

        while current is not None:
            path.insert(0, current) # insert to maintain correct order
            current = current.getPrevious() # move to the previous tile in path

        return path if path and path[0] == self.maze.start else [] # Return path if valid

    # Print the maze with the path of the found solution
    # from Start to Goal. If there is no solution, just
    # print the original maze.
    def printSolution(self):
        # Get the solution for the maze from the maze itself
        solution = self.getPath()
        # A list of strings representing the maze
        output = self.maze.makeMazeBase() # gets base representation of maze
        # For all of the tiles that are part of the path, 
        # mark it with a *
        for tile in solution:
            output[tile.getRow()][tile.getCol()] = '*' # Mark path tiles
        # Mark the start and goal tiles
        output[self.maze.start.getRow()][self.maze.start.getCol()] = 'S' # Marks Start
        output[self.maze.goal.getRow()][self.maze.goal.getCol()] = 'G' # Marks Goal

        # Print the output string
        for row in output:
            print(row)

   

if __name__ == "__main__":
    # The maze to solve
    maze = Maze(["____",
                 "S##E",
                 "__#_",
                 "____"])
    # Initialize the MazeSolver to be solved with a Stack
    solver = MazeSolver(maze, Stack)
    # Solve the maze
    solver.solve()
    # Print the solution found
    solver.printSolution()