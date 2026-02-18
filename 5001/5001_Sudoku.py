import time
import tracemalloc
#Predefined Boards [More Boards At End of File.]
Board9x9 = [
  [6, 0, 0, 7, 0, 0, 0, 0, 1],
  [0, 3, 0, 0, 2, 0, 0, 0, 9],
  [0, 0, 0, 6, 8, 0, 3, 0, 0],
  [0, 0, 0, 9, 0, 0, 6, 0, 0],
  [5, 0, 6, 0, 1, 0, 0, 0, 4],
  [0, 0, 0, 0, 3, 0, 0, 0, 8],
  [0, 0, 7, 0, 0, 0, 0, 1, 0],
  [0, 9, 2, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 7, 0, 0, 6]
]
Board6x6 = [
    [2, 0, 5, 0, 0, 3],
    [0, 0, 6, 0, 0, 1],
    [0, 3, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 6, 4, 0, 1, 0],
    [0, 2, 0, 6, 0, 0]
]
Board4x4 = [
    [4, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3],
    [1, 0, 4, 0]
]





#Board Size and Algorithm Selection.
algorithm = input("Choose solving algorithm (\"dfs\" or \"bfs\"): ").lower()
user_input = input("Enter Sudoku Board Size (\"4\", \"6\", or \"9\": ")
match user_input:
    case "4":
        Board, x, subgrid_width, y, RowDivider = (
        Board4x4, 2, 2, 3, "- - - - - -")
        
    case "6":
        Board, x, subgrid_width, y, RowDivider = (
        Board6x6, 2, 3, 5, "- - - - - - - - - ")
        
    case "9":
        Board, x, subgrid_width, y, RowDivider = (
        Board9x9, 3, 3, 8, "- - - - - - - - - - - - - " )
        
    case _:
        print("Invalid Input. Defaulting to 9x9 Board. Please enter ONLY \"4\" \"6\" or \"9\"")
        Board, x, subgrid_width, y, RowDivider = (
        Board9x9, 3, 3, 8, "- - - - - - - - - - - - - " )

#Human Readable Sudoku Output
def print_board(Board):
    for row in range(len(Board)):
        if row % x == 0 and row != 0:
            print(RowDivider)

        for column in range(len(Board[0])):
            if column % x == 0 and column != 0:
                print(" | ", end="")

            if column == y:
                print(Board[row][column])
            else:
                print(str(Board[row][column]) + " ", end="")
                #--- (TechWithTim, 2020)

#----------------------------------------------------------
# Algorithm Functions

#Empty Cell Finder
def find_empty(Board):
    for row in range(len(Board)):
        for column in range(len(Board[0])):
            if Board[row][column] == 0:
                return (row, column)
    return None
            #--- (Coderivers, 2025)

#Valid move checker -----
def valid(board, row, col, number):
    if number in board[row]:
        return False
    
    if number in [board[i][col] for i in range(len(board))]:
        return False
    
    RowIndex1 = x * (row // x)
    ColumnIndex1 = subgrid_width * (col // subgrid_width)
    for i in range(RowIndex1, RowIndex1 + x):
        for j in range(ColumnIndex1, ColumnIndex1 + subgrid_width):
            if board[i][j] == number:
                return False
    return True
            #--- (TechWithTim, 2020)

#Depth-First Search Solver
def solve_dfs(Board):    
    start_time = time.time()
    tracemalloc.start()

    valid_state = 0
    stack = [([row[:] for row in Board], 1)]

    while stack:
        board_peek, iterator = stack[-1]
        
        empty_cell = find_empty(board_peek)
        if empty_cell is None:
            for i in range(len(Board)):
                Board[i][:] = board_peek[i]
            
            x, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()
            print(f"Peak memory usage was {peak} bytes")
            print(f"Time Taken: {end_time - start_time:.6f} seconds")
            print(f"Solved | Valid States Checked {valid_state}")
            return True #Solved
            

        empty_row, empty_column = empty_cell       
        if iterator > len(Board):
            stack.pop()
            continue 
        stack.pop() == (board_peek, iterator + 1)
        stack.append((board_peek, iterator + 1))
        if valid(board_peek, empty_row, empty_column, iterator):
            valid_state += 1
            append_board = [row[:] for row in board_peek]
            append_board[empty_row][empty_column] = iterator
            stack.append((append_board, 1))
    
    x, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    print(f"Peak memory usage was {peak} bytes")
    print(f"Time Taken: {end_time - start_time:.6f} seconds")
    print(f"Unsolved Valid States Checked {valid_state}")
    return False

def solve_bfs(Board):
    start_time = time.time()
    tracemalloc.start()

    valid_state = 0
    queue = [[row[:] for row in Board]]
    while queue:
        popboard = queue.pop(0)
        empty = find_empty(popboard)
        if empty == None:
            for i in range(len(Board)):
                Board[i][:] = popboard[i]

            x, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()
            print(f"Peak memory usage was {peak} bytes")
            print(f"Time Taken: {end_time - start_time:.6f} seconds")
            print(f"Solved | Valid States Checked {valid_state}")
            return True
        
        row1, column1 = empty
        for number in range(1, len(Board) + 1):
            valid_state += 1
            if valid(popboard, row1, column1, number):
                stackboard = [row[:] for row in popboard]
                stackboard[row1][column1] = number
                queue.append(stackboard)

    x, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    print(f"Peak memory usage was {peak} bytes")
    print(f"Time Taken: {end_time - start_time:.6f} seconds")
    print(f"Unsolved Valid States Checked {valid_state}")
    return False

if algorithm == 'dfs':
    if solve_dfs(Board):
        print_board(Board)
elif algorithm == 'bfs': 
    if solve_bfs(Board):
        print_board(Board)
else:
    print("Invalid Algorithm Selection. Please enter ONLY \"dfs\" or \"bfs\"")





#----------------------------------------------------------
#Code References

#TechWithTim (2020) Sudoku Solver Part 1. [online] Techwithtim.net. Available at: https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/part-1. [Accessed 10th Jan. 2026]

#Coderivers (2025). Sudoku Solver in Python: Unraveling the Logic and Best Practices. [online] Coderivers.org. Available at: https://coderivers.org/blog/sudoku-solver-python/ [Accessed 10th Jan. 2026]




















#------------------------------------------

# Assignment Utilised Sudoku Boards.
# #9x9 Easy ------------------------

# 1.
# Board9x9 = [
#   [6, 0, 4, 5, 0, 0, 3, 9, 8],
#   [9, 0, 0, 6, 0, 0, 0, 7, 4],
#   [0, 0, 8, 0, 0, 0, 6, 2, 1],
#   [0, 0, 0, 0, 9, 0, 1, 0, 6],
#   [0, 1, 0, 4, 0, 3, 9, 5, 7],
#   [0, 8, 9, 0, 0, 6, 2, 4, 3],
#   [7, 0, 3, 0, 5, 0, 4, 1, 0],
#   [0, 0, 0, 0, 1, 0, 0, 0, 2],
#   [1, 4, 0, 0, 0, 9, 8, 0, 0]
# ]

# 2.
# Board9x9 = [
#   [2, 0, 0, 4, 6, 7, 5, 3, 0],
#   [0, 0, 0, 0, 0, 0, 0, 1, 0],
#   [4, 0, 7, 0, 5, 1, 6, 0, 8],
#   [0, 1, 8, 0, 3, 2, 0, 0, 0],
#   [7, 2, 9, 0, 4, 5, 0, 8, 0],
#   [0, 3, 0, 0, 0, 0, 9, 6, 2],
#   [1, 7, 3, 0, 9, 4, 2, 0, 6],
#   [0, 0, 0, 5, 2, 0, 0, 9, 2],
#   [0, 0, 2, 0, 1, 0, 0, 0, 3]
# ]

# 3.
# Board9x9 = [
#   [4, 0, 0, 0, 0, 0, 0, 2, 9],
#   [7, 0, 6, 0, 0, 9, 0, 0, 0],
#   [0, 0, 5, 0, 0, 0, 7, 3, 8],
#   [0, 9, 4, 2, 0, 0, 0, 1, 0],
#   [0, 0, 2, 0, 1, 0, 0, 8, 4],
#   [0, 7, 0, 5, 0, 4, 3, 0, 0],
#   [8, 0, 7, 0, 4, 0, 1, 9, 0],
#   [2, 0, 1, 9, 5, 3, 8, 7, 6],
#   [0, 6, 0, 0, 0, 7, 2, 4, 5]
# ]


# #9x9 Medium ------------------------------------------------------------------------------------------

# 1.
# Board9x9 = [
#   [9, 0, 0, 0, 0, 0, 0, 0, 0],
#   [6, 0, 0, 0, 1, 7, 3, 4, 2],
#   [0, 0, 0, 8, 3, 0, 0, 0, 6],
#   [0, 0, 4, 6, 0, 3, 1, 0, 0],
#   [0, 0, 0, 0, 0, 2, 5, 0, 0],
#   [3, 2, 0, 0, 0, 5, 4, 6, 7],
#   [0, 0, 0, 0, 0, 0, 0, 0, 4],
#   [7, 6, 0, 0, 0, 0, 2, 1, 5],
#   [0, 0, 0, 0, 0, 0, 6, 0, 9]
# ]

# 2.
# Board9x9 = [
#   [0, 1, 0, 0, 5, 0, 9, 0, 0],
#   [6, 0, 5, 0, 0, 0, 0, 0, 0],
#   [2, 0, 3, 1, 0, 0, 5, 0, 0],
#   [0, 3, 0, 0, 6, 0, 4, 9, 2],
#   [0, 0, 0, 0, 2, 0, 0, 0, 8],
#   [0, 0, 8, 0, 7, 3, 0, 0, 0],
#   [0, 0, 0, 6, 0, 7, 0, 0, 0],
#   [0, 5, 9, 0, 0, 4, 8, 0, 3],
#   [0, 6, 0, 9, 0, 0, 2, 7, 0]
# ]

# 3.
# Board9x9 = [
#   [7, 0, 0, 0, 0, 0, 5, 0, 8],
#   [0, 0, 0, 1, 4, 0, 3, 0, 2],
#   [8, 0, 0, 7, 0, 0, 0, 0, 0],
#   [0, 7, 4, 0, 0, 0, 0, 0, 0],
#   [2, 3, 8, 6, 7, 0, 9, 5, 0],
#   [0, 0, 1, 0, 3, 0, 0, 0, 0],
#   [0, 8, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 6, 3, 0, 5, 0, 0, 0],
#   [0, 0, 0, 0, 6, 7, 0, 3, 1]
# ]

# #9x9 Hard ------------------------------------------------------------------------------------------
# 1.
# Board9x9 = [
#   [4, 0, 0, 0, 7, 0, 0, 0, 0],
#   [0, 0, 7, 0, 9, 0, 4, 0, 1],
#   [0, 1, 0, 0, 6, 0, 0, 0, 0],
#   [5, 4, 0, 0, 0, 0, 0, 0, 0],
#   [0, 0, 8, 0, 0, 0, 5, 0, 2],
#   [9, 2, 0, 0, 0, 5, 0, 8, 4],
#   [0, 0, 0, 3, 0, 6, 0, 1, 0],
#   [3, 0, 0, 0, 0, 8, 0, 0, 0],
#   [0, 5, 0, 0, 2, 4, 0, 0, 7]
# ]

# 2.
# Board9x9 = [
#   [6, 0, 0, 0, 0, 0, 0, 8, 0],
#   [0, 0, 1, 0, 0, 0, 0, 0, 0],
#   [2, 0, 0, 0, 0, 0, 4, 0, 0],
#   [0, 3, 0, 0, 8, 4, 2, 0, 0],
#   [5, 0, 0, 0, 9, 0, 0, 0, 6],
#   [0, 0, 2, 0, 6, 5, 0, 0, 0],
#   [0, 0, 0, 0, 0, 6, 1, 0, 0],
#   [0, 0, 7, 1, 0, 2, 0, 0, 4],
#   [3, 0, 4, 0, 0, 0, 0, 0, 9]
# ]

# #3.
# Board9x9 = [
#   [0, 3, 7, 0, 0, 5, 0, 0, 9],
#   [0, 0, 0, 0, 0, 9, 0, 0, 0],
#   [0, 0, 1, 0, 0, 0, 8, 0, 0],
#   [4, 0, 0, 3, 7, 0, 2, 0, 0],
#   [0, 0, 5, 0, 6, 4, 0, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 0, 0],
#   [1, 0, 0, 0, 0, 0, 4, 5, 0],
#   [9, 0, 0, 1, 0, 0, 0, 2, 6],
#   [0, 0, 3, 6, 0, 0, 7, 0, 0]
# ]

# #9x9 Very Hard ------------------------------------------------------------------------------------------
# #1.
# Board9x9 = [
#   [0, 0, 2, 0, 0, 0, 0, 0, 9],
#   [7, 0, 0, 4, 0, 0, 0, 0, 0],
#   [0, 0, 9, 0, 6, 0, 0, 3, 0],
#   [2, 0, 0, 7, 8, 4, 0, 0, 0],
#   [6, 0, 0, 1, 0, 0, 0, 0, 7],
#   [0, 0, 4, 2, 0, 0, 0, 0, 0],
#   [0, 0, 3, 0, 2, 0, 8, 0, 0],
#   [0, 0, 0, 0, 0, 0, 0, 5, 0],
#   [1, 0, 0, 9, 0, 3, 4, 0, 0]
# ]

# #2.
# Board9x9 = [
#   [0, 6, 5, 9, 0, 0, 1, 4, 0],
#   [0, 0, 0, 0, 1, 7, 0, 3, 0],
#   [0, 0, 7, 0, 0, 0, 0, 0, 5],
#   [4, 0, 0, 0, 0, 0, 0, 0, 0],
#   [5, 0, 6, 0, 7, 9, 0, 0, 0],
#   [0, 9, 0, 1, 4, 0, 0, 0, 0],
#   [0, 5, 0, 0, 0, 0, 0, 1, 0],
#   [1, 0, 0, 0, 2, 0, 0, 7, 0],
#   [0, 2, 0, 6, 0, 0, 0, 0, 3]
# ]

# #3.
# Board9x9 = [
#   [6, 0, 0, 7, 0, 0, 0, 0, 1],
#   [0, 3, 0, 0, 2, 0, 0, 0, 9],
#   [0, 0, 0, 6, 8, 0, 3, 0, 0],
#   [0, 0, 0, 9, 0, 0, 6, 0, 0],
#   [5, 0, 6, 0, 1, 0, 0, 0, 4],
#   [0, 0, 0, 0, 3, 0, 0, 0, 8],
#   [0, 0, 7, 0, 0, 0, 0, 1, 0],
#   [0, 9, 2, 0, 0, 0, 0, 0, 0],
#   [0, 0, 0, 1, 0, 7, 0, 0, 6]
# ]

# #6x6 Easy ------------------------------------------------------------------------------------------
# 1.
# Board6x6 = [
#     [5, 3, 0, 4, 0, 6],
#     [4, 6, 0, 5, 3, 1],
#     [1, 2, 4, 0, 5, 3],
#     [6, 0, 3, 0, 0, 2],
#     [3, 4, 0, 2, 1, 5],
#     [0, 1, 5, 3, 0, 4]
# ]

# 2.

# Board6x6 = [
#     [0, 4, 1, 0, 0, 0],
#     [3, 2, 0, 6, 4, 1],
#     [5, 6, 0, 6, 4, 1],
#     [5, 6, 0, 0, 1, 0],
#     [0, 1, 6, 4, 3, 5],
#     [4, 5, 3, 1, 0, 6]
# ]

# 3.
# Board6x6 = [
#     [5, 4, 1, 0, 0, 2],
#     [2, 6, 3, 4, 0, 5],
#     [3, 1, 0, 6, 0, 4],
#     [6, 2, 4, 5, 0, 1],
#     [1, 5, 0, 2, 4, 3],
#     [0, 0, 0, 1, 5, 6]
# ]


# #6x6 Medium ------------------------------------------------------------------------------------------
# 1.
# Board6x6 = [
#     [0, 0, 2, 1, 0, 0],
#     [0, 5, 6, 0, 4, 0],
#     [5, 0, 4, 3, 1, 6],
#     [6, 0, 3, 0, 2, 0],
#     [0, 4, 0, 6, 5, 2],
#     [2, 0, 0, 4, 0, 0]
# ]

# 2.
# Board6x6 = [
#     [2, 6, 3, 5, 0, 4],
#     [1, 0, 5, 0, 0, 3],
#     [4, 5, 2, 3, 0, 1],
#     [3, 0, 6, 2, 0, 0],
#     [0, 0, 0, 4, 0, 0],
#     [0, 2, 4, 0, 0, 0]
# ]

# 3.

# Board6x6 = [
#     [0, 4, 0, 1, 0, 2],
#     [1, 0, 3, 0, 6, 0],
#     [0, 3, 0, 6, 5, 0],
#     [6, 0, 5, 4, 2, 3],
#     [2, 0, 0, 3, 1, 0],
#     [3, 0, 0, 0, 0, 6]
# ]


# #6x6 Hard ------------------------------------------------------------------------------------------
# 1.
# Board6x6 = [
#     [0, 0, 0, 0, 5, 0],
#     [2, 3, 5, 0, 4, 0],
#     [0, 0, 0, 4, 2, 6],
#     [0, 4, 2, 0, 3, 0],
#     [3, 0, 1, 5, 0, 0],
#     [0, 0, 6, 0, 1, 0]
# ]

# 2.
# Board6x6 = [
#     [2, 0, 4, 3, 0, 0],
#     [0, 3, 0, 0, 5, 0],
#     [0, 1, 0, 6, 0, 3],
#     [3, 6, 2, 0, 4, 5],
#     [0, 0, 6, 0, 0, 1],
#     [1, 0, 0, 0, 0, 0]
# ]

# 3.
# Board6x6 = [
#     [0, 6, 2, 5, 0, 4],
#     [3, 0, 4, 1, 6, 0],
#     [6, 4, 0, 0, 0, 0],
#     [0, 0, 0, 6, 4, 0],
#     [0, 0, 6, 0, 0, 1],
#     [5, 0, 0, 4, 0, 0]
# ]


# #6x6 Very Hard ------------------------------------------------------------------------------------------
# 1.
# Board6x6 = [
#     [0, 3, 0, 0, 1, 6],
#     [6, 0, 1, 0, 0, 0],
#     [0, 5, 2, 0, 0, 0],
#     [0, 0, 0, 0, 5, 3],
#     [0, 0, 0, 0, 6, 0],
#     [0, 0, 6, 0, 0, 4]
# ]

# 2.
# Board6x6 = [
#     [0, 0, 4, 1, 0, 0],
#     [6, 5, 0, 0, 0, 4],
#     [1, 0, 6, 0, 0, 3],
#     [2, 3, 0, 4, 1, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0]
# ]

# 3.
# Board6x6 = [
#     [2, 0, 5, 0, 0, 3],
#     [0, 0, 6, 0, 0, 1],
#     [0, 3, 0, 2, 0, 0],
#     [0, 0, 0, 0, 0, 0],
#     [0, 6, 4, 0, 1, 0],
#     [0, 2, 0, 6, 0, 0]
# ]


# #4x4 Easy ------------------------------------------------------------------------------------------
# 1.
# Board4x4 = [
#     [0, 0, 0, 0],
#     [1, 3, 2, 4],
#     [0, 0, 4, 0],
#     [2, 0, 3, 0]
# ]

# 2.
# Board4x4 = [
#     [4, 0, 1, 0],
#     [1, 0, 0, 0],
#     [0, 1, 4, 3],
#     [0, 0, 2, 0]
# ]

# 3.
# Board4x4 = [
#     [2, 0, 0, 0],
#     [4, 3, 2, 0],
#     [0, 0, 1, 0],
#     [1, 0, 3, 4]
# ]


# #4x4 Medium ------------------------------------------------------------------------------------------
# 1.
# Board4x4 = [
#     [3, 0, 1, 0],
#     [2, 0, 0, 0],
#     [0, 0, 0, 1],
#     [0, 2, 4, 0]
# ]

# 2.
# Board4x4 = [
#     [0, 0, 0, 3],
#     [0, 4, 0, 0],
#     [0, 3, 0, 2],
#     [1, 0, 0, 4]
# ]

# 3.
# Board4x4 = [
#     [4, 2, 3, 0],
#     [0, 0, 0, 0],
#     [0, 0, 1, 0],
#     [0, 1, 0, 3]
# ]

# #4x4 Hard ------------------------------------------------------------------------------------------
# 1.
# Board4x4 = [
#     [3, 4, 0, 0],
#     [0, 0, 4, 0],
#     [0, 1, 0, 0],
#     [0, 0, 0, 1]
# ]

# 2.
# Board4x4 = [
#     [0, 0, 0, 2],
#     [4, 0, 0, 0],
#     [0, 4, 2, 0],
#     [0, 0, 3, 0]
# ]

# 3.
# Board4x4 = [
#     [0, 4, 3, 0],
#     [0, 0, 0, 4],
#     [0, 0, 0, 0],
#     [3, 0, 0, 2]
# ]


# #4x4 Very Hard ------------------------------------------------------------------------------------------
# 1.
# Board4x4 = [
#     [3, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 4, 0, 3],
#     [0, 0, 0, 1]
# ]

# 2.
# Board4x4 = [
#     [1, 0, 0, 2],
#     [0, 0, 0, 0],
#     [2, 0, 0, 0],
#     [0, 4, 0, 0]
# ]

# 3.
# Board4x4 = [
#     [4, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 0, 3],
#     [1, 0, 4, 0]
# ]
