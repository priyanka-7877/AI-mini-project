import turtle
import random

# Set up the screen
wn = turtle.Screen()
wn.title("MINI PROJECT 2048 game")
wn.bgcolor("black")
wn.setup(width=450, height=500) # Increased height for score display
wn.tracer(0) #Turns off automatic animation → we manually update screen for faster drawing.

# Score
score = 0

# Grid list
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# Pen
pen = turtle.Turtle() #new turtle object called pen.
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup() #prevents unwanted drawing
pen.hideturtle() #hides the turtle arrow icon
pen.turtlesize(stretch_wid=2, stretch_len=2, outline=2)
#This changes the size of the square stamp.
#Normally, a turtle stamp is small (20×20).
#But for the 2048 tiles, you need bigger squares.


# MAIN CODE LOGIC

def _slide_and_merge_line(line):
    """
    Takes a 4-element list (a row or column) and applies the slide and merge logic.
    Returns the processed 4-element list and updates the global score.
    """
    global score
    
    # 1. Slide: Filter out zeros
    new_line = [i for i in line if i != 0]
    
    # 2. Merge: Iterate and combine identical adjacent tiles
    merged_line = []
    skip_next = False
    
    for i in range(len(new_line)):
        if skip_next:
            skip_next = False # if TRUE This block SKIPS the next number
            continue
        
        # If there is a next tile AND both tiles are equal → MERGE THEM
        if i < len(new_line) - 1 and new_line[i] == new_line[i+1]: 
            # Merge
            merged_value = new_line[i] * 2
            merged_line.append(merged_value)
            score += merged_value # Update score
            skip_next = True
        else:
            merged_line.append(new_line[i])

    # 3. Pad: Fill the rest with zeros
    while len(merged_line) < 4:
        merged_line.append(0)
        
    return merged_line

    

# Helpes for UP/DOWN movement, Transpose the grid (rows become columns and vice versa)
def _transpose(g):
    """Returns a transposed copy of the 4x4 grid."""
    #zip = pair elements from multiple lists into tuples
    #*g = unpack g into separate lists
    # zip(*g) swaps rows and columns; (list) converts tuples back to lists
    return [list(t) for t in zip(*g)]


# VISUAL APPERANCE OF GRID

def draw_grid():
    # Draws the tiles and the score on the screen.
    colors = {
        0: "white",
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72", 
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e"
    }

    pen.clear() # Clear everything before drawing the new frame

    # Draw Score Display
    pen.goto(0, 210)
    pen.color("white")
    pen.write("Score: {}".format(score), align="center", font=("Courier", 20, "bold"))
    
    # Draw the grid tiles
    grid_y = 0
    y_start = 100 # Adjusted starting y position
    
    for row in grid:
        grid_x = 0
        x_start = -75
        y = y_start - grid_y * 45
        
        for column in row:
            x = x_start + grid_x * 45
            pen.goto(x, y)
            
            # Set the color based on the value
            value = grid[grid_y][grid_x]
            # Use black for non-zero numbers for contrast, except for 2048 which is black
            text_color = "black" if value <= 512 and value != 0 else "white"

            color = colors.get(value, "black") # Use black for values > 2048 (if they ever occur)
            pen.color(color)
            pen.stamp()

            # Draw the number
            pen.color(text_color)
            if column != 0:
                number = str(column)
                # Center the number vertically in the square
                pen.goto(x, y - 10) 
                pen.write(number, align="center", font=("Courier", 14, "bold"))

            grid_x += 1
            
        grid_y += 1
            # Check for game over
    if is_game_over():
        pen.goto(0, -200)
        pen.color("red")
        pen.write("GAME OVER", align="center", font=("Courier", 30, "bold"))

        pen.goto(0, -240)
        pen.color("white")
        pen.write("Press R to Play Again", align="center", font=("Courier", 18, "bold"))
        wn.update()
        return

        
    wn.update() # Update the screen once after all drawing is done


def get_empty_cells():
    """Returns a list of (row, column) tuples for all empty cells (value 0)."""
    empty = []
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                empty.append((r, c))
    return empty

def add_random():
    """Adds a 2 or a 4 to a random empty cell."""
    empty_cells = get_empty_cells()
    if not empty_cells:
        # No empty cells left (Game Over logic would go here)
        return
        
    y, x = random.choice(empty_cells)
    value = random.choice([2, 4])
    grid[y][x] = value

# --- Movement Functions (Fixed) ---

def left():
    global grid
    moved = False
    new_grid = [[0] * 4 for _ in range(4)]
    
    for r in range(4):
        original_row = list(grid[r])
        processed_row = _slide_and_merge_line(original_row)
        new_grid[r] = processed_row
        
        if original_row != processed_row:
            moved = True
            
    if moved:
        grid = new_grid
        add_random()
    
    draw_grid()

def right():
    global grid
    moved = False
    new_grid = [[0] * 4 for _ in range(4)]

    for r in range(4):
        original_row = list(grid[r])
        
        # Reverse the row, treat as 'left' movement, then reverse back
        reversed_row = original_row[::-1]
        processed_reversed_row = _slide_and_merge_line(reversed_row)
        processed_row = processed_reversed_row[::-1]
        
        new_grid[r] = processed_row
        
        if original_row != processed_row:
            moved = True

    if moved:
        grid = new_grid
        add_random()
    
    draw_grid()

def up():
    global grid
    moved = False
    
    # 1. Transpose the current grid (columns become rows)
    temp_grid = _transpose(grid)
    new_temp_grid = [[0] * 4 for _ in range(4)]
    
    for c in range(4): # c now represents the column index (which is a row in temp_grid)
        original_col = list(temp_grid[c]) 
        processed_col = _slide_and_merge_line(original_col)
        new_temp_grid[c] = processed_col
        
        if original_col != processed_col:
            moved = True

    # 2. Transpose back to update the main grid
    if moved:
        grid = _transpose(new_temp_grid)
        add_random()
    
    draw_grid()

def down():
    global grid
    moved = False
    
    # 1. Transpose the current grid
    temp_grid = _transpose(grid)
    new_temp_grid = [[0] * 4 for _ in range(4)]

    for c in range(4):
        original_col = list(temp_grid[c])
        
        # Reverse the column, treat as 'left' movement, then reverse back
        reversed_col = original_col[::-1]
        processed_reversed_col = _slide_and_merge_line(reversed_col)
        processed_col = processed_reversed_col[::-1]
        
        new_temp_grid[c] = processed_col
        
        if original_col != processed_col:
            moved = True

    # 2. Transpose back to update the main grid
    if moved:
        grid = _transpose(new_temp_grid)
        add_random()
    
    draw_grid()

def is_game_over():
    # 1. Check if empty cells exist
    if get_empty_cells():
        return False

    # 2. Check if any merges are possible (left/right/up/down)
    # Check rows
    for r in range(4):
        for c in range(3):
            if grid[r][c] == grid[r][c+1]:
                return False

    # Check columns
    for c in range(4):
        for r in range(3):
            if grid[r][c] == grid[r+1][c]:
                return False

    return True  # No moves left → Game over

# reset game
def reset_game():
    global grid, score
    score = 0
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    add_random()
    add_random()
    draw_grid()


# --- Initialization ---
# Start the game with two random tiles
add_random()
add_random()
draw_grid()

# Keyboard bindings
wn.onkeypress(reset_game, "r")
wn.listen()
wn.onkeypress(left, "Left")
wn.onkeypress(right, "Right")
wn.onkeypress(up, "Up")
wn.onkeypress(down, "Down")

wn.mainloop()
