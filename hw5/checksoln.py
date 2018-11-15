import numpy as np
import sys

# Load maze and solution data
def loadData(maze_file, solution_file):
    maze_data = np.loadtxt(maze_file, dtype='int')
    solution = np.loadtxt(solution_file, dtype='int')
    # Generate maze with 0 indicates valid road, -1 indicates the walls
    n_row, n_col = maze_data[0]
    maze = np.zeros((n_row, n_col))
    
    for i in range(1, len(maze_data)):
        row, col = maze_data[i]
        maze[row, col] = -1
    
    return maze, solution

# Checking solution process
def checkSol(maze, solution):
    n_row, n_col = maze.shape
    
    # Not enter the maze via the first row
#--style_0
#--Try indexing in numpy array using syntax solution[0, 0] as it avoids an extra copy of the line under the hood.
#--START
    if solution[0][0] != 0:
        return False
#--END
    # Not reach the last row
    if solution[-1][0] != n_row - 1:
        return False
    
    for i in range(len(solution)):
        # Out of the bounds
        row, col = solution[i]
        if row < 0 or col < 0 or row > n_row - 1 or col > n_col - 1:
            return False
        
        # Cross the wall
        if maze[row, col] != 0:
            return False
        
        # Invalid movement
        if i > 0:
#--style_0
#--you could have vectorized this step using (solution[1:] - solution[:-1]).abs().sum(axis=1), and then checked that the array is full of ones.
#--START
            move = sum([abs(x) for x in solution[i] - solution[i-1]])
            if move != 1:
                return False
#--END
    return True


def main():
    if len(sys.argv) < 3:
        print('Usage:')
        print('  python3 checksoln.py <maze file> <solution file>')
        sys.exit()
    
    maze, solution = loadData(sys.argv[1], sys.argv[2])
    isValid = checkSol(maze, solution)
    
    if isValid:
        print("Solution is valid!")
    else:
        print("Solution is not valid!")
    
    return


if __name__ == "__main__":
    main()

#--correctness_0
#--Your program checks the main issues in a maze escape, well done !
#--END

#--style_0
#--You could have used slightly more of the numpy vectorized possibilities, but your code is quite efficient and pleasant to read !
#--END