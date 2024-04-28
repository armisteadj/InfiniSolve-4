import tkinter as tk
from tkinter import messagebox, Frame, Entry, simpledialog, Label
import random
import time

def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

def is_valid_move(grid, row, col, num):
    if num in grid[row]:
        return False
    for i in range(9):
        if grid[i][col] == num or grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
            return False
    return True

def solve_sudoku(grid):
    empty = find_empty_location(grid)
    if not empty:
        return True  # No empty location means puzzle is solved
    row, col = empty
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            if solve_sudoku(grid):
                return True
            grid[row][col] = 0  # Undo the move
    return False

def find_empty_location(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return None

def generate_sudoku():
    grid = [[0] * 9 for _ in range(9)]
    solve_sudoku(grid)  # First solve it completely
    remove_count = random.randint(20, 40)  # Amount of numbers to remove
    attempts = 0
    while remove_count > 0 and attempts < 100:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            backup = grid[row][col]
            grid[row][col] = 0
            copy_grid = [r[:] for r in grid]
            if not solve_sudoku(copy_grid):
                grid[row][col] = backup  # Restore the number if removal makes it unsolvable
            else:
                remove_count -= 1
        attempts += 1
    return grid

def auto_solve():
    global sudoku_grid, solution_grid, start_time
    copy_grid = [row[:] for row in sudoku_grid]  # Make a copy of the current puzzle
    if solve_sudoku(copy_grid):
        for i in range(9):
            for j in range(9):
                entry_grid[i][j].delete(0, tk.END)
                entry_grid[i][j].insert(0, copy_grid[i][j])
                entry_grid[i][j].config(state='disabled', disabledforeground='black')
        end_time = time.time()
        solve_duration = round(end_time - start_time, 2)
        scores.append(solve_duration)
        update_scores_label()
        messagebox.showinfo("Sudoku Solved", f"Puzzle solved in {solve_duration} seconds.")
    else:
        messagebox.showerror("Unable to solve", "This Sudoku puzzle cannot be solved.")

def draw_grid(play_frame):
    global sudoku_grid, entry_grid, start_time
    entry_grid = [[None for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            e = Entry(play_frame, width=3, font=('Arial', 18), justify='center')
            e.grid(row=i, column=j, sticky='news', padx=1, pady=1)
            if sudoku_grid[i][j] != 0:
                e.insert(0, sudoku_grid[i][j])
                e.config(state='disabled', disabledforeground='black')
            else:
                e.insert(0, '')
                e.bind('<FocusOut>', lambda event, row=i, col=j: update_cell(row, col, entry_grid[row][col]))
            entry_grid[i][j] = e
    start_time = time.time()  # Start timing when the grid is drawn

def check_valid_move(row, col, val):
    global sudoku_grid
    for i in range(9):
        if sudoku_grid[row][i] == val and i != col:
            return False
        if sudoku_grid[i][col] == val and i != row:
            return False
    box_row = row // 3
    box_col = col // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if sudoku_grid[i][j] == val and (i, j) != (row, col):
                return False
    return True

def update_cell(row, col, entry):
    global sudoku_grid
    try:
        val = int(entry.get())
        print(f"User entered: {val}, Expected: {sudoku_grid[row][col]}")  # Debug output
        if val == sudoku_grid[row][col]:
            entry.config(state='disabled', disabledforeground='black')
        else:
            #messagebox.showerror("Incorrect", "This number is incorrect.")
            entry.delete(0, 'end')
    except ValueError:
        #messagebox.showerror("Invalid Input", "Please enter a valid number (1-9).")
        entry.delete(0, 'end')

def finished():
    global sudoku_grid, solution_grid, start_time
    copy_grid = [row[:] for row in sudoku_grid]  # Make a copy of the current puzzle
    if solve_sudoku(copy_grid):
        for i in range(9):
            for j in range(9):
                entry_grid[i][j].delete(0, tk.END)
                entry_grid[i][j].insert(0, copy_grid[i][j])
                entry_grid[i][j].config(state='disabled', disabledforeground='black')
        end_time = time.time()
        solve_duration = round(end_time - start_time, 2)
        scores.append(solve_duration)
        update_scores_label()
        messagebox.showinfo("Sudoku Solved", f"Puzzle solved in {solve_duration} seconds.")
    else:
        messagebox.showerror("Unable to solve", "This Sudoku puzzle cannot be solved.")

def generate_and_solve():
    global sudoku_grid, solution_grid, start_time, play_frame
    start_time = time.time()  # Start timing when the grid is drawn
    solution_grid = generate_sudoku()  # Store the solution
    sudoku_grid = [row[:] for row in solution_grid]  # Copy for mutable version
    play_frame = Frame(play_screen)  # Define play_frame here
    play_frame.grid(row=1, column=0, sticky='news')  # Place it in the play_screen
    draw_grid(play_frame)  # Draw the Sudoku grid

 # Add the "Finished" button next to the other buttons
    tk.Button(play_screen, text="Finished", command=finished).grid(row=0, column=3, sticky='ew', padx=10, pady=10)


def input_custom_sudoku():
    input_data = simpledialog.askstring("Input", "Enter your Sudoku as a string using '0' for empty cells. Extra characters after the first 81 will be ignored.")
    if input_data:
        # Ensure there's at least some data to process and trim to the first 81 characters if longer
        trimmed_data = input_data[:81]

        processed_input = []
        try:
            for ch in trimmed_data:
                val = int(ch)  # Converts character to integer
                if val < 0 or val > 9:
                    raise ValueError("Please ensure all characters are digits from 0 to 9.")
                processed_input.append(val)

            # Ensure we have exactly 81 digits
            if len(processed_input) != 81:
                messagebox.showerror("Error", "Not enough digits. Please provide at least 81 digits.")
                return

            global sudoku_grid, solution_grid
            sudoku_grid = [processed_input[i*9:(i+1)*9] for i in range(9)]
            if all(v == 0 for row in sudoku_grid for v in row):  # Check if the grid is entirely empty
                solution_grid = generate_sudoku()  # Generate a complete puzzle if input is all zeros
                sudoku_grid = [row[:] for row in solution_grid]  # Copy for mutable version
            else:
                solution_grid = [row[:] for row in sudoku_grid]
                if not solve_sudoku(solution_grid):  # Try solving the provided grid
                    messagebox.showerror("Error", "Sudoku cannot be solved from this configuration.")
                    return

            draw_grid(play_frame)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

def show_hints():
    hints_text = (
        "Welcome to Sudoku Hints!\n\n"
        "1. **Scanning**: Start by scanning rows, columns, and blocks for missing numbers.\n"
        "2. **Cross-hatching**: Check each square to see which numbers are missing and eliminate possibilities.\n"
        "3. **Penciling In**: Temporarily write all possible numbers in each empty cell.\n"
        "4. **Naked Pairs/Triples**: If two or three cells in a row, column, or block have the same two or three possible numbers, those numbers can be removed from other cells in that row, column, or block.\n"
        "5. **Backtracking**: When stuck, start making educated guesses for a cell, and continue solving based on that guess. If a contradiction is reached, backtrack and try the next possibility."
    )
    messagebox.showinfo("Sudoku Hints", hints_text)

def update_scores_label():
    scores_text = "Top Solve Times (s): " + ", ".join(map(str, sorted(scores)))
    scores_label.config(text=scores_text)

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Self-Solving Sudoku")

main_menu = Frame(root)
hints_menu = Frame(root)
play_screen = Frame(root)
scores_screen = Frame(root)
play_frame = Frame(play_screen)

scores = []  # List to keep track of solve times
scores_label = Label(scores_screen, text="No scores yet.")

for frame in (main_menu, hints_menu, play_screen, scores_screen, play_frame):
    frame.grid(row=0, column=0, sticky='news')

play_frame.grid(row=1, column=0, sticky='news')

# Back button for the play screen
tk.Button(play_screen, text="Back to Menu", command=lambda: show_frame(main_menu)).grid(row=2, column=0, columnspan=3, sticky='ew')

tk.Button(main_menu, text="Hints", command=lambda: show_frame(hints_menu)).grid(row=0, column=0)
tk.Button(main_menu, text="Play", command=lambda: show_frame(play_screen)).grid(row=1, column=0)
tk.Button(main_menu, text="Scores", command=lambda: show_frame(scores_screen)).grid(row=2, column=0)
# Adding a Quit Button to the Main Menu
tk.Button(main_menu, text="Quit", command=root.destroy).grid(row=3, column=0)


tk.Button(hints_menu, text="Show Hints", command=show_hints).grid(row=0, column=0)
tk.Button(hints_menu, text="Back", command=lambda: show_frame(main_menu)).grid(row=1, column=0)

tk.Button(play_screen, text="Generate Sudoku", command=generate_and_solve).grid(row=0, column=0, sticky='ew', padx=10, pady=10)
tk.Button(play_screen, text="Automatically Solve", command=auto_solve).grid(row=0, column=1, sticky='ew', padx=10, pady=10)
tk.Button(play_screen, text="Input Custom Sudoku", command=input_custom_sudoku).grid(row=0, column=2, sticky='ew', padx=10, pady=10)

scores_label.grid(row=0, column=0)
tk.Button(scores_screen, text="Back", command=lambda: show_frame(main_menu)).grid(row=1, column=0)

show_frame(main_menu)

root.mainloop()
