# Expert System for Solving Sudoku Puzzles
import random
import json
import time

GENERATE_DATASET = True  # Set to True to generate a dataset of puzzles with solutions
GEN_DATASET_SIZE = 50000  # Number of puzzles to generate for the dataset
GEN_BLANKS = 6  # Number of blanks in each generated puzzle
GEN_MAX_SOLUTIONS = 1  # Maximum number of solutions allowed for each generated puzzle (1 for unique solution)

# The following will be our universal test position for the solvers.
test_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def generate_board():
    # This funtion generates a valid sudoku board.
    digits = list(range(1,10))  # This will be the list of digits from 1 to 9
    random.shuffle(digits) # Randomize the digits to create a unique board each time

    populated_board = []
    for i in range(9):
        # add the digits to the board
        populated_board.append(digits)
        # shift the digits for the next row to prevent block duplicates
        digits = digits[3:] + digits[:3]
        if (i + 1) % 3 == 0:  # Every 3 rows
            # shift the digits for the next block layer
            digits = digits[1:] + digits[:1]
        
    return populated_board

def generate_puzzle(valid_board, num_blanks):
    # This function takes a valid sudoku board and removes a specified number of digits to create a puzzle. The resulting puzzle will have a unique solution.
    # Easy = 30 blanks, Medium = 40 blanks, Hard = 50 blanks, Extreme = 60 blanks, Limit = 64 
    puzzle_board = [row[:] for row in valid_board]  # Create a copy of the valid board
    
    
    # Generate all possible cell positions
    cell_positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cell_positions)  # Shuffle the cell positions to ensure randomness

    # Method 1: Blank out cells from a random selection of positions until the desired number of blanks is reached
    for row, col in cell_positions[:num_blanks]:  # Take the first num_blanks positions from the shuffled list
        puzzle_board[row][col] = 0  # Blank out the cell

    # Method 2: Randomly select cells to blank out until the desired number of blanks is reached
    # Viable method but slower and less efficient than method 1, especially as num_blanks increases, due to potential repeats in random selection.
    blanks_added = 0
    while False and blanks_added < num_blanks:
        row, col = random.randint(0, 8), random.randint(0, 8)

        if puzzle_board[row][col] != 0:  # Only blank out non-empty cells
            puzzle_board[row][col] = 0
            blanks_added += 1

    return puzzle_board

def is_valid_move(board, row, col, num):
    # This function checks if placing a number in a specific cell is valid

    # Check for duplicates
    for i in range(9):
        # Check the row
        if board[row][i] == num and i != col:
            return False
        # Check the column
        if board[i][col] == num and i != row:
            return False
    
    # Check the 3x3 block
    block_row_start = (row // 3) * 3
    block_col_start = (col // 3) * 3
    for r in range(block_row_start, block_row_start + 3):
        for c in range(block_col_start, block_col_start + 3):
            if board[r][c] == num and (r != row or c != col):
                return False
    
    return True

def brute_force_solve(board):
    # This function solves most sudoku puzzles using a brute-force backtracking algorithm. It is not the most efficient method, but it is guaranteed to find a solution if one exists.
    solved_board = [row[:] for row in board]  # Create a copy of the board to solve
    for row in range(9):
        for col in range(9):
            if solved_board[row][col] == 0:  # If the cell is empty
                for num in range(1, 10):  # Try numbers 1-9
                    if is_valid_move(solved_board, row, col, num):
                        solved_board[row][col] = num  # Place the number

                        result = brute_force_solve(solved_board)
                        if result is not False:
                            return result  # Return the solved board
                        
                        solved_board[row][col] = 0  # Reset the cell (backtrack)

                return False  # Trigger backtracking
    
    return solved_board  # Return the solved board when complete

def brute_force_solve_with_limit(board, max_depth=100):
    # Safer version with recursion depth limit
    def solve_recursive(board_state, depth):
        if depth > max_depth:
            return False
        
        for row in range(9):
            for col in range(9):
                if board_state[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid_move(board_state, row, col, num):
                            board_state[row][col] = num
                            result = solve_recursive(board_state, depth + 1)
                            if result is not False:
                                return result
                            board_state[row][col] = 0
                    return False
        return board_state
    
    solved = [row[:] for row in board]
    return solve_recursive(solved, 0)

def count_solutions(board, solutions_found, max_solutions=2):
    # This loop searches for the next empty cell (0)
    # Early exit: stop searching once we have enough solutions
    if len(solutions_found) >= max_solutions:
        return
    
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num  # Place the number
                        
                        # Recursively move to the next empty cell
                        count_solutions(board, solutions_found, max_solutions)
                        
                        # --- THE RESET BUTTON ---
                        # We erase the number and try the next loop index (e.g., trying 4 after 3).
                        # If the loop hits 9, this cell finishes and passes control backward.
                        board[row][col] = 0
                        
                        # Early exit check
                        if len(solutions_found) >= max_solutions:
                            return
                        
                return  # Force a backtrack if 1-9 are all exhausted
                
    # --- VICTORY CONDITION ---
    # If the loops finish and never found a '0', the board is 100% full!
    # We append a copy of this solution to our list.
    solutions_found.append([row[:] for row in board])

def validate_solution(puzzle_board, solution_board):
    # This function checks if a given board is a valid solution to a sudoku puzzle.
    for row in range(9):
        for col in range(9):
            #if puzzle_board[row][col] != 0 and puzzle_board[row][col] != solution_board[row][col]:
                #print(f"Potentially new solution at ({row}, {col}): puzzle has {puzzle_board[row][col]}, but original has {solution_board[row][col]}.")
                

            if not is_valid_move(solution_board, row, col, solution_board[row][col]):
                print(f"Invalid move at cell ({row}, {col}): {solution_board[row][col]} is not valid.")
                return False  # The solution violates sudoku rules
    return True

def generate_puzzles_with_solution_count(num_puzzles, num_blanks, max_solutions):
    # Generate a specific number of puzzles with a max solution count
    generated_puzzles = []
    
    while len(generated_puzzles) < num_puzzles:
        valid_board = generate_board()
        puzzle = generate_puzzle(valid_board, num_blanks)
        
        # Make a copy to avoid modifying original
        puzzle_copy = [row[:] for row in puzzle]
        solutions_tracker = []
        # Use max_solutions + 1 to detect if there are too many solutions
        count_solutions(puzzle_copy, solutions_tracker, max_solutions + 1)
        
        if len(solutions_tracker) <= max_solutions:
            # Solve the puzzle to get the unique solution
            solution = brute_force_solve(puzzle)
            generated_puzzles.append({
                "puzzle": puzzle,
                "solution": solution,
                "num_solutions": len(solutions_tracker)
            })
    
    return generated_puzzles



if __name__ == "__main__":
    if GENERATE_DATASET:
        # Create a puzzle dataset with X puzzles each having Y blanks and at most Z solution
        print("\nGenerating puzzle dataset (this may take a while)...")
        puzzle_dataset = generate_puzzles_with_solution_count(GEN_DATASET_SIZE, GEN_BLANKS, GEN_MAX_SOLUTIONS)
        print(f"Generated {len(puzzle_dataset)} puzzles with 10 blanks and at most 1 solution.")

        # Export the dataset to a json file
        timestamp = int(time.time())
        dataset_path = f"data/sudoku_puzzle_dataset_{GEN_DATASET_SIZE}_{GEN_BLANKS}_{GEN_MAX_SOLUTIONS}_{timestamp}.json"
        with open(dataset_path, 'w') as f:
            json.dump(puzzle_dataset, f, indent=2)
        print(f"Dataset saved to {dataset_path}")
    else:
        # Test functionality
        print("Testing Sudoku Solver with a sample board:")
        generated_board = generate_board()
        print("Generated Board:")
        for row in generated_board:
            print(row)

        puzzle = generate_puzzle(generated_board, 40)
        print("\nGenerated Puzzle:")
        for row in puzzle:
            print(row)

        solution = brute_force_solve(puzzle)
        print("\nSolved Puzzle:")
        for row in solution:
            print(row)

        solution_check = "Yes" if validate_solution(puzzle, solution) else "No"
        print(f"\nIs the solution valid? {solution_check}")

        solutions_tracker = []
        count_solutions_copy = [row[:] for row in puzzle]
        count_solutions(count_solutions_copy, solutions_tracker)
        print(f"Number of solutions found: {len(solutions_tracker)}")