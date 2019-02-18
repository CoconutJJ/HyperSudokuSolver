#################################################################
#                                                               #
#    Define any helper functions you need in this file only.    #
#    You will be handing in HyperSudoku.py, nothing else.       #
#                                                               #
#    A few test cases are provided in Test.py. You can test     #
#    Your code by running: (See the file for more details)      #
#               python Test.py                                  #
#    in the directory where the files are located.              #
#                                                               #
#    We're using Python 3.X this time.                          #
#                                                               #
#################################################################


class HyperSudoku:

    # BITMAP of 9 BITS: Bit 0 -> 1, Bit 1 -> 2, etc..
    ALL_POSSIBLE_VALUES = 511 # 2^9 - 1
    @staticmethod
    def solve(grid):
        """
        Input: An 9x9 hyper-sudoku grid with numbers [0-9].
                0 means the spot has no number assigned.
                grid is a 2-Dimensional array. Look at
                Test.py to see how it's initialized.

        Output: A solution to the game (if one exists),
                in the same format. None of the initial
                numbers in the grid can be changed.
                'None' otherwise.
        """

        for i in range(9):
            for j in range(9):
                
                if grid[i][j] == 0:

                    possible_values = HyperSudoku.getPossibleValues(grid, j, i) # HyperSudoku.getPossibleValuesSquare(grid, j,i) & HyperSudoku.getPossibleValuesRowsCols(grid, j,i) & HyperSudoku.getPossibleValuesHyperSquares(grid, j, i)
                    
                    for v in range(9):
                        if (possible_values & (1 << v)) > 0:

                            grid[i][j] = v + 1
                            if HyperSudoku.solve(grid) != None:
                                return grid
                            else:
                                grid[i][j] = 0
                    return None

        return grid

    @staticmethod
    def getPossibleValues(grid, x, y):
        x_sq = int(x/3)
        y_sq = int(y/3)
        possibleValues = HyperSudoku.ALL_POSSIBLE_VALUES
        for i in range(0,3):
            for j in range(0,3):
                cx = j + x_sq * 3
                cy = i + y_sq * 3
                if grid[cy][cx] != 0:
                    possibleValues = possibleValues & ~(1 << (grid[cy][cx] - 1)) 

        for i in range(9):

            if grid[i][x] != 0:
                possibleValues = possibleValues & ~(1 << (grid[i][x] - 1)) 
            
            if grid[y][i] != 0:
                possibleValues = possibleValues & ~(1 << (grid[y][i] - 1)) 
        
        for x_off in [0,4]:
            for y_off in [0,4]:
                xlb = 1 + x_off
                xub = 3 + x_off
                ylb = 1 + y_off
                yub = 3 + y_off
                if xlb <= x <= xub and ylb <= y <= yub:
                
                    for i in range(ylb, yub + 1):
                        for j in range(xlb, xub + 1):
                            if grid[i][j] != 0:
                                possibleValues = possibleValues & ~(1 << (grid[i][j] - 1)) 
                
        return possibleValues

    @staticmethod
    def printGrid(grid):
        """
        Prints out the grid in a nice format. Feel free
        to change this if you need to, it will NOT be 
        used in marking. It is just to help you debug.

        Use as:     HyperSudoku.printGrid(grid)
        """
        print("-"*25)
        for i in range(9):
            print("|", end=" ")
            for j in range(9):
                print(grid[i][j], end=" ")
                if (j % 3 == 2):
                    print("|", end=" ")
            print()
            if (i % 3 == 2):
                print("-"*25)

if __name__ == "__main__":
    import json
    import time
    times = []
    with open('100K_puzzles.txt', 'r') as f:
        puzzles = json.loads(f.readlines()[0].rstrip())
    x = 0
    for grid, soln in puzzles:
        t = time.time()
        my_soln = HyperSudoku.solve(grid)
        
        times.append(time.time() - t)
        print(str(times[x]) + "," + str(x))
        x += 1
        
        assert soln == my_soln
        
        if (x == 20): break
    print(sum(times)/len(times))