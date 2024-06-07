# Preface: The brief introduction of how I code the Sliding Puzzle - 2024 Spring semester
# I will write the detailed comments below the particular codes
# All in all, I designed this puzzle including 10 functions
# specially contains check the inverse numbers and the move of space and the puzzle
# These functions are used to initialize conduct and judge the situations
# in some long functions, comments will explain and dividend parts of the function

import math
import random
import turtle

tiles = {}
tile_width = 100
board_size = 0
game_over = False
moving = False


def input_board_size():
    global board_size
    screen = turtle.Screen()
    while True:
        board_size_input = turtle.textinput("Board Size", "Puzzle Level --> ")
        if board_size_input.isdigit():
            board_size = int(board_size_input)
            if board_size in [3, 4, 5]:
                screen.clear()
                return board_size
            else:
                report_error("Please enter 3,4,5 level for the puzzle")
        else:
            report_error("Please enter a valid number, the puzzle provides 3,4,5 level")


# Make sure that the input is valid, which is 3 or 4 or 5
# Any invalid input will be reported error


def report_error(error):
    screen = turtle.Screen()
    screen.clear()
    t = turtle.Turtle()
    t.penup()
    t.hideturtle()
    t.goto(0, 200)
    t.write(error, align="center", font=("Arial", 20, "normal"))
    t.hideturtle()
    # Report the message when the input is invalid


def initialize_the_screen():
    global t, screen
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.setup(width=800, height=800)
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.pencolor('white')
    t.pendown()
    turtle.tracer(0)


# The following function is just what I wrote in Assignment 1
def check_inverse_number(puzzle_number):
    inversion_count = 0
    for i in range(len(puzzle_number)):
        for j in range(i + 1, len(puzzle_number)):
            # the definition about the inverse numbers
            # count inversions by comparing elements to the right
            if puzzle_number[i] > puzzle_number[j] != 0 and puzzle_number[i] != 0:
                inversion_count += 1
    # use this function in order to avoid the possibility of the mistake made by the 0
    # a counter-example: 1,2,3,4,5,6,8,0,7 if calculate the inverse number gets 1 +1 =2
    # because 0 < 8 and 7 < 8, the "inverse number" = 2
    # however, when calculate the inverse number, "0" is not included since it represents as space
    # so, the real inverse number is 1, not an even number which will causes a non-existed puzzle
    # like: 1  2  3
    #       4  5  6
    #       8  7
    return inversion_count


def create_puzzle():
    numbers = list(range(1, board_size * board_size)) + [0]
    random.shuffle(numbers)
    return numbers


def check_solvable_puzzle(numbers):
    inversion_count = check_inverse_number(numbers)
    total_numbers = len(numbers)
    if total_numbers % 2 == 0:
        empty_row_order = numbers.index(0) // 4
        if (3 - empty_row_order + inversion_count) % 2 == 0:
            return inversion_count % 2 == 0
        else:
            return inversion_count % 2 == 1
    else:
        return inversion_count % 2 == 0


# This function is to judge whether the random puzzle is solvable
# Since it is different from the Assignment 1, with even and odd level puzzle
# In even function, which is the level 4 puzzle, the inversion count need to be odd
# The total number of inversion count plus final row minus initial row should be even
# Otherwise, the odd puzzle's inversion count should be even

def populate_tiles(numbers):
    for i in range(board_size):
        for j in range(board_size):
            num = numbers[board_size * i + j]
            x = j * tile_width - (board_size - 1) * tile_width / 2
            y = (board_size - 1) * tile_width / 2 - i * tile_width
            tiles[(i, j)] = num
            draw_puzzle(num, x, y)


def create_solvable_puzzle():
    numbers = create_puzzle()
    while not check_solvable_puzzle(numbers):
        numbers = create_puzzle()
    populate_tiles(numbers)


# Create a solvable puzzle


def draw_tile_background(x, y, color):
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.fillcolor(color)
    for _ in range(4):
        t.forward(tile_width)
        t.right(90)
    t.end_fill()
    t.penup()


# Select the color and draw the tiles

def write_number(num, x, y, color='blue'):
    t.color(color)
    t.goto(x, y)
    t.write(num, align="center", font=("Times New Roman", 24, "normal"))
    t.color('white')


# Write the numbers on the tiles

def draw_puzzle(num, x, y, is_game_over=False):
    if num == 0 or (is_game_over and num == board_size ** 2):
        background_color = "white" if num == 0 else "red"
    elif is_game_over:
        background_color = "red"
    else:
        background_color = "light green"

    draw_tile_background(x, y, background_color)

    if num != 0 and not (is_game_over and num == board_size ** 2):
        write_number(num, x + tile_width / 2, y - tile_width / 2 - 18)


# Check whether the puzzle is completed, if yes, turn the background color to red, otherwise stay light green


def draw_moving_puzzle(num, x, y, is_game_over=False):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    t.fillcolor("light green")
    for _ in range(4):
        t.forward(tile_width)
        t.right(90)
    t.end_fill()
    t.hideturtle()


def update_board():
    t.clear()
    for i in range(board_size):
        y = (board_size - 1) * tile_width / 2 - i * tile_width
        for j in range(board_size):
            x = j * tile_width - (board_size - 1) * tile_width / 2
            num = tiles[(i, j)]
            draw_puzzle(num, x, y, game_over)

            # Clean the board and update the puzzle after the valid click


def find_empty_tile():
    for blank, value in tiles.items():
        if value == 0:
            return blank
        # Find the blank tile in the puzzle


def is_valid_move(row, col, blank_row, blank_col):
    is_row_adjacent = row == blank_row and abs(col - blank_col) == 1
    is_col_adjacent = col == blank_col and abs(row - blank_row) == 1
    return is_row_adjacent or is_col_adjacent


# Check whether the color tile is next to the blank tile
# By computing the distance between the selected color tile and the blank tile
# Only the distance is one can be valid for the movement

def smooth_animation(row, col, blank_row, blank_col):
    smooth = 100
    start_x = col * tile_width - (board_size - 1) * tile_width / 2
    start_y = (board_size - 1) * tile_width / 2 - row * tile_width
    target_x = blank_col * tile_width - (board_size - 1) * tile_width / 2
    target_y = (board_size - 1) * tile_width / 2 - blank_row * tile_width
    delta_x = (target_x - start_x) / smooth
    delta_y = (target_y - start_y) / smooth

    actual_x = start_x
    actual_y = start_y

    for i in range(smooth):
        actual_x = start_x + delta_x * i
        actual_y = start_y + delta_y * i
        draw_moving_puzzle(tiles[(row, col)], actual_x, actual_y, game_over)
        turtle.update()


# Using the smooth to achieve the slide animation


def update_tiles(blank_row, blank_col, row, col):
    tiles[(blank_row, blank_col)] = tiles[(row, col)]
    tiles[(row, col)] = 0


def check_game_over():
    global game_over
    expected_numbers = [i % (board_size * board_size) for i in range(1, board_size * board_size)] + [0]
    for i in range(board_size):
        for j in range(board_size):
            if tiles[(i, j)] != expected_numbers[board_size * i + j]:
                return False
    # Check all the tile and judge whether it is completed, if yes, turn all the tile red
    for i in range(board_size):
        for j in range(board_size):
            draw_puzzle(tiles[(i, j)], j * tile_width - (board_size - 1) * tile_width / 2,
                        (board_size - 1) * tile_width / 2 - i * tile_width, True)
    game_over = True
    return True


# Check whether the updated puzzle's order satisfied the final situation
# Just by comparing whether the number is on the proper position

def move(row, col):
    global moving, game_over
    if moving or game_over:
        # If the puzzle is over or the tile is moving, stop any control
        return
    blank_row, blank_col = find_empty_tile()
    if is_valid_move(row, col, blank_row, blank_col):
        moving = True
        smooth_animation(row, col, blank_row, blank_col)
        update_tiles(blank_row, blank_col, row, col)
        update_board()
        game_over = check_game_over()
        moving = False
        # This function is quite important in the movement of the tile
        # In case the multiple clicks to cause errors, once the tile is moving, nothing can be done


def solve_puzzle():
    global board_size
    for row in range(board_size):
        for col in range(board_size):
            x_coordinate = col * tile_width - (board_size - 1) * tile_width / 2
            y_coordinate = (board_size - 1) * tile_width / 2 - row * tile_width
            draw_puzzle(board_size * row + col + 1, x_coordinate, y_coordinate, True)


def mouse_click(x, y):
    global game_over
    if not game_over:
        col = math.floor((x + (board_size - 1) * tile_width / 2) / tile_width)
        row = math.floor(((board_size - 1) * tile_width / 2 - y) / tile_width)
        if (row, col) in tiles:
            move(row, col)
    elif game_over:
        solve_puzzle()
        # Check when the puzzle is not completed, the area mouse click is valid
        # Make sure that the area mouse click is valid for a specific tile


def main():
    create_solvable_puzzle()
    input_board_size()
    initialize_the_screen()
    create_solvable_puzzle()
    screen.onclick(mouse_click)
    turtle.done()


if __name__ == "__main__":
    main()
