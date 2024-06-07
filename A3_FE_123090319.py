# Preface: The brief introduction of how I code the Snake - 2024 Spring semester
# I will write the detailed comments below the particular codes
# The Snake Game is quite difficult, I use many separate functions to keep the robotics of the game
# All in all, I cut the Snake Game into five parts as the instructions mentioned
# I write each parts of the in the above of the functions
# The whole functions are based on the instructions, I will put the original details below specific functions
# Thanks for your distinguished check

import turtle
import random
import time

snake_list = [[0, 0]]
snake_direction = 1
tail_count = 5
food_position = {}
remain_or_not = True
create_number = True
eat_how_many = 0
g_list_appear = [1, 2, 3, 4, 5]
g_list_appear_real = [1, 2, 3, 4, 5]
not_end = True
screen = None
border = None
g_indication = None
introduction = None
monster_x_position = 9999
monster_y_position = 9999
g_monster = None
add_or_not = True
hide = True
dic_number_items = {}
g_hide = []
indication = None
start = 0
clock_time = 0
monster_touch_snake = 0
direction = None
one = None
list_two = []
game_started = False


# Part 1 : Create the screen and game area of the game

def create_screen():
    global screen, border, g_indication, introduction
    screen = turtle.Screen()
    screen.setup(500 + 30 * 2, 560 + 30 * 2, 0, 0)
    screen.tracer(False)

    # Create the screen of the play with the board and margin

    border = turtle.Turtle()
    border.hideturtle()
    border.pensize(3)
    border.penup()
    border.goto(250, -280)
    border.pendown()
    border.setheading(90)
    border.forward(500 + 60)
    border.setheading(180)
    border.forward(500)
    border.setheading(270)
    border.forward(500 + 60)
    border.setheading(0)
    border.forward(500)
    border.penup()
    border.goto(250, 280 - 60)
    border.pendown()
    border.pensize(3)
    border.setheading(180)
    border.forward(500)

    # Create the game area with the requirements:
    # i. Upper status area = around 500 (w) x 60 (h)
    # ii. Lower motion area = around 500 (w) x 500 (w)
    # iii. Margins = around 30 pixels

    g_indication = turtle.Turtle()
    g_indication.hideturtle()
    g_indication.penup()
    g_indication.goto(-210, 230)
    g_indication.write("Contact: " + "0" + "   Time: " + "0" "   Motion: " + "Paused", font=("Arial", 18, "bold"))

    # Create the Status Bar in the above of the game area to record the related parameters

    introduction = turtle.Turtle()
    introduction.penup()
    introduction.goto(0, 120)
    introduction.hideturtle()
    introduction.write("Snake by Junpeng Liang\nClick anywhere on the screen to start the game, have fun!!!",
                       align="center", font=("Arial", 12, "bold"))

    # Create the introduction part

    screen.update()


# Part 2 : Create the random food and the random movement of the food


def create_random_food_and_their_position():
    global food_position, dic_number_items
    for num in range(1, 6):
        position_x = random.randrange(-200, 200, 20)
        position_y = random.randrange(-200, 200, 20)
        food_position[num] = [position_x, position_y]
        food = turtle.Turtle()
        food.penup()
        food.goto(position_x, position_y)
        food.write(num, font=("Arial", 12, "bold"))
        food.hideturtle()
        turtle.tracer(False)
        turtle.update()
        dic_number_items[num] = food
    return dic_number_items


def random_hide_and_random_movement():
    global hide, g_list_appear, g_list_appear_real, food_position, g_hide, dic_number_items

    if len(g_list_appear_real) == 0:
        return
    else:
        if hide:
            hide_food = random.choice(g_list_appear)
            g_list_appear.remove(hide_food)
            dic_number_items[hide_food].clear()
            g_hide.append(hide_food)
            hide = False
        else:
            move_food = g_hide[-1]
            g_hide.pop(-1)
            g_list_appear.append(move_food)

            new_position_x = random.randrange(-200, 200, 20)
            new_position_y = random.randrange(-200, 200, 20)
            food_position[move_food] = [new_position_x, new_position_y]

            food = turtle.Turtle()
            food.penup()
            food.goto(new_position_x, new_position_y)
            food.write(move_food, font=("Arial", 12, "bold"))
            food.hideturtle()
            turtle.tracer(False)
            turtle.update()
            dic_number_items[move_food] = food
            hide = True

    screen.ontimer(random_hide_and_random_movement, 5000)


# Part 3 : Create the Snake

def create_head_of_snake(x, y):
    head_of_snake = turtle.Turtle()
    head_of_snake.pensize(2)
    head_of_snake.pencolor("red")
    head_of_snake.fillcolor("red")
    head_of_snake.penup()
    head_of_snake.goto(x, y)
    head_of_snake.pendown()
    head_of_snake.hideturtle()
    head_of_snake.begin_fill()
    head_of_snake.setheading(0)
    head_of_snake.forward(20)
    head_of_snake.setheading(270)
    head_of_snake.forward(20)
    head_of_snake.setheading(180)
    head_of_snake.forward(20)
    head_of_snake.setheading(90)
    head_of_snake.forward(20)
    head_of_snake.end_fill()
    turtle.update()
    return head_of_snake
# Draw the head of the snake


def create_tail_of_snake(x, y):
    tail_of_snake = turtle.Turtle()
    tail_of_snake.pensize(2)
    tail_of_snake.fillcolor("black")
    tail_of_snake.pencolor("blue")
    tail_of_snake.penup()
    tail_of_snake.goto(x, y)
    tail_of_snake.pendown()
    tail_of_snake.hideturtle()
    tail_of_snake.begin_fill()
    tail_of_snake.setheading(0)
    tail_of_snake.forward(20)
    tail_of_snake.setheading(270)
    tail_of_snake.forward(20)
    tail_of_snake.setheading(180)
    tail_of_snake.forward(20)
    tail_of_snake.setheading(90)
    tail_of_snake.forward(20)
    tail_of_snake.end_fill()
    turtle.update()
    return tail_of_snake
# Draw the tail of the snake


def create_initial_monster(numbers_of_monsters):
    global g_monster
    g_monster = []

    for _ in range(numbers_of_monsters):
        list_x = []
        list_y = []

        list_x.append(random.randrange(-220, -160, 20))
        list_x.append(random.randrange(160, 220, 20))

        list_y.append(random.randrange(-250, -180, 20))
        list_y.append(random.randrange(120, 210, 20))

        monster_x_position = random.choice(list_x)
        monster_y_position = random.choice(list_y)

        monster = turtle.Turtle("square")
        monster.color("purple")
        monster.penup()
        monster.goto(monster_x_position, monster_y_position)

        g_monster.append(monster)
# Using two random position of x and y, can create four corners' monsters


def snake_move():
    global snake_list, snake_direction, one, list_two
    change_indication()
    eat_number()
    win_check()
    if remain_or_not:
        if one is None:
            pass
        else:
            one.clear()
            for second in list_two:
                second.clear()
        if snake_direction == 1:
            if snake_list[0][1] + 20 > 220:
                pass
            elif snake_list[0][1] + 20 == snake_list[1][1]:
                pass
            else:
                snake_list.insert(0, [snake_list[0][0], snake_list[0][1] + 20])
                snake_list.pop(-1)

        elif snake_direction == 2:
            if snake_list[0][0] + 20 > 235:
                pass
            elif snake_list[0][0] + 20 == snake_list[1][0]:
                pass
            else:
                snake_list.insert(0, [snake_list[0][0] + 20, snake_list[0][1]])
                snake_list.pop(-1)

        elif snake_direction == 3:
            if snake_list[0][1] - 20 < -260:
                pass
            elif snake_list[0][1] - 20 == snake_list[1][1]:
                pass
            else:
                snake_list.insert(0, [snake_list[0][0], snake_list[0][1] - 20])
                snake_list.pop(-1)

        elif snake_direction == 4:
            if snake_list[0][0] - 20 < -240:
                pass
            elif snake_list[0][0] - 20 == snake_list[1][0]:
                pass
            else:
                snake_list.insert(0, [snake_list[0][0] - 20, snake_list[0][1]])
                snake_list.pop(-1)

        elif snake_direction == 0:
            pass
        for each in range(len(snake_list) - 1, -1, -1):
            if each == 0:
                one = create_head_of_snake(snake_list[each][0], snake_list[each][1])
            else:
                two = create_tail_of_snake(snake_list[each][0], snake_list[each][1])
                list_two.append(two)
    else:
        return

    screen.ontimer(snake_move, 200)
# Computing the distance of the snake head and the board to stop the snake movement
# And checking the keyboard direction to control snake's movement


def add_tail():
    global snake_list, snake_direction, tail_count, screen, add_or_not
    list_tail = []
    num = 0

    while add_or_not:
        change_indication()
        dx, dy = {1: (0, 20), 2: (20, 0), 3: (0, -20), 4: (-20, 0), 0: (0, 0)}.get(snake_direction, (0, 0))

        if len(snake_list) == 1 or (dx, dy) != (0, 0):
            x, y = snake_list[0][0] + dx, snake_list[0][1] + dy
            if -260 <= x <= 240 and -280 <= y <= 220 and (len(snake_list) == 1 or (x, y) != snake_list[1]):
                num += 1
                snake_list.insert(0, [x, y])

        for each in range(len(snake_list) - 1, -1, -1):
            if each == 0:
                head = create_head_of_snake(snake_list[0][0], snake_list[0][1])
            else:
                tail = create_tail_of_snake(snake_list[each][0], snake_list[each][1])
                list_tail.append(tail)
        head.clear()
        for tail in list_tail:
            tail.clear()
        time.sleep(0.4)

        if num == tail_count:
            add_or_not = False
# If the snake has eaten one of the food, by checking the food number and add it to the tail of the snake
# Using time.sleep function in order to avoid the situation that the snake eats more than one food in a short time


def eat_number():
    global snake_list, food_position, tail_count, dic_number_items
    global eat_how_many, g_list_appear, g_list_appear_real, add_or_not
    for i in g_list_appear:
        snake_head_x, snake_head_y = snake_list[0]
        food_x, food_y = food_position[i]
        distance = ((snake_head_x - food_x) ** 2 + (snake_head_y - food_y) ** 2) ** 0.5
        if distance < 40:
            g_list_appear.remove(i)
            g_list_appear_real.remove(i)
            dic_number_items[i].clear()
            tail_count = i
            add_or_not = True
            add_tail()
            eat_how_many += 1
            break
# Once the snake's head distance is smaller than forty, it means the food is eaten by the snake
# Here, I use forty as the interval because I want to make food eaten more sensitively


# Part 4 : Create four monsters
def monster_move():
    global g_monster, not_end, snake_list, screen, add_or_not, monster_touch_snake, remain_or_not

    for monster in g_monster:
        if not not_end:
            break

        list_monster_move = []
        monster_x_position, monster_y_position = monster.position()

        for each in snake_list:
            if -10 < monster_x_position - each[0] < 30 and -30 < monster_y_position - each[1] < 10:
                monster_touch_snake += 1
                break

        if not not_end:
            break

        monster.speed(2)

        if monster_x_position < snake_list[0][0] - 5:
            list_monster_move.append(1)
        elif monster_x_position > snake_list[0][0] + 5:
            list_monster_move.append(2)

        if monster_y_position < snake_list[0][1] - 5:
            list_monster_move.append(3)
        elif monster_y_position > snake_list[0][1] + 5:
            list_monster_move.append(4)

        move = random.choice(list_monster_move)
        if move == 1:
            if 239 < monster_x_position < 248:
                pass
            else:
                monster.goto(monster_x_position + 10, monster_y_position)
        elif move == 2:
            if -260 < monster_x_position < -239:
                pass
            else:
                monster.goto(monster_x_position - 10, monster_y_position)
        elif move == 3:
            if 205 < monster_y_position < 215:
                pass
            else:
                monster.goto(monster_x_position, monster_y_position + 10)
        elif move == 4:
            if -340 < monster_y_position < -287:
                pass
            else:
                monster.goto(monster_x_position, monster_y_position - 10)

        if (snake_list[0][0] - 5 < monster_x_position < snake_list[0][0] + 28 and
                snake_list[0][1] - 20 < monster_y_position < snake_list[0][1] + 5):
            not_end = False
            add_or_not = False
            remain_or_not = False

            for i in range(len(snake_list)):
                if i == 0:
                    create_head_of_snake(snake_list[0][0], snake_list[0][1])
                else:
                    create_tail_of_snake(snake_list[i][0], snake_list[i][1])
            turtle.tracer(False)

            lose_words = turtle.Turtle()
            lose_words.pencolor("red")
            lose_words.penup()
            lose_words.goto(0, 0)
            lose_words.write("Game Over!!", align="center", font=("Arial", 24, "bold"))
            lose_words.hideturtle()
            # To make the sign of game over on the top of the game area
            turtle.update()
            return

    screen.ontimer(monster_move, random.randint(200, 400))
# By computing the distance between the snake and the monster to judge whether the game is over


# Part 5 : Create the game indications

def up():
    global snake_direction
    snake_direction = 1


def right():
    global snake_direction
    snake_direction = 2


def down():
    global snake_direction
    snake_direction = 3


def left():
    global snake_direction
    snake_direction = 4


def space():
    global snake_direction, direction
    if snake_direction == 0:
        snake_direction = direction
    else:
        direction = snake_direction
        snake_direction = 0


# Determine four direction and the pause of the snake movement


def begin(x, y):
    global introduction, snake_direction, create_number, dic_number_items, start, game_started
    if not game_started and -500 < x < 500:
        game_started = True
        first = create_head_of_snake(0, 0)
        start = time.time()
        introduction.clear()
        snake_direction = random.randint(1, 4)
        turtle.onkeypress(up, "Up")
        turtle.onkeypress(right, "Right")
        turtle.onkeypress(down, "Down")
        turtle.onkeypress(left, "Left")
        turtle.onkeypress(space, "space")
        turtle.listen()

        while create_number:
            dic_number_items = create_random_food_and_their_position()
            create_number = False

        monster_move()
        add_tail()
        first.clear()
        snake_move()
        random_hide_and_random_movement()
        screen.onscreenclick(None)
        # To avoid the situation of quick, continue of the mouse click
    else:
        pass


def win_check():
    global eat_how_many, remain_or_not, not_end
    if eat_how_many == 5:
        remain_or_not = False
        not_end = False

        for i in range(len(snake_list)):
            if i == 0:
                create_head_of_snake(snake_list[0][0], snake_list[0][1])
            else:
                create_tail_of_snake(snake_list[i][0], snake_list[i][1])
        turtle.tracer(False)

        win_words = turtle.Turtle()
        win_words.pencolor("red")
        win_words.penup()
        win_words.goto(0, 0)
        win_words.write("Winner!!", align="center", font=("Arial", 24, "bold"))
        win_words.hideturtle()
        turtle.update()
        # To make the sign of winner on the top of the game area
    else:
        pass
# Once all the food has been eaten, the game is won


def change_indication():
    global snake_direction, g_indication, start, clock_time, screen, monster_touch_snake, remain_or_not

    if remain_or_not:
        g_indication.clear()
        if snake_direction == 1:
            motion = "Up"
        elif snake_direction == 2:
            motion = "Right"
        elif snake_direction == 3:
            motion = "Down"
        elif snake_direction == 4:
            motion = "Left"
        else:
            motion = "Paused"

        end = time.time()
        if 0.7 <= end - start <= 1.3:
            start += 1
            clock_time += 1

        else:
            pass

        g_indication = turtle.Turtle()
        g_indication.hideturtle()
        g_indication.penup()
        g_indication.goto(-210, 230)
        g_indication.write("Contact: " + str(monster_touch_snake) + "   Time: "
                           + str(clock_time) + "   Motion: " + motion, font=("Arial", 18, "bold"))
    else:
        return
# To show the essential indication in the game, including contact,time and direction


def main():
    create_screen()
    create_initial_monster(4)
    screen.onscreenclick(begin)
    turtle.mainloop()


if __name__ == "__main__":
    main()
