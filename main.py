

import time
import tkinter
import random
import math
from PIL import ImageTk
from PIL import Image


CANVAS_WIDTH = 1300
CANVAS_HEIGHT = 700

BALL_SIZE = 40

PADDLE_Y = CANVAS_HEIGHT - 125
PADDLE_WIDTH_EASY = 250
PADDLE_WIDTH = 150
PADDLE_WIDTH_HARD = 100

BOTTOM_LINE_POS = CANVAS_HEIGHT - 100

PLAYERS = {}


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, title="Don't let the ball fall")
    image = ImageTk.PhotoImage(Image.open("Howtoplay.jpg"))
    canvas.create_image(0, 0, anchor='nw', image=image)

    # User choose the difficulty level
    paddle_width = choose_difficulty_level()

    # User choose how many players
    choose_number_of_players()

    print_new_line()

    # to show players' names
    print_players(PLAYERS)

    print_new_line()

    highest_score = 0
    for player in PLAYERS:
        start_game = input(str(player) + " Press Enter to start \n")

        # A counter of 3 seconds to start the game
        sec_to_start(3)

        change_x = random.randint(6, 10)
        change_y = random.randint(6, 10)
        respawn_x = random.randint(1, CANVAS_WIDTH - BALL_SIZE)
        player_points = 0
        # Make the canvas
        canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, title="Don't let the ball fall")
        # Create the ball
        ball = canvas.create_oval(respawn_x, 0, respawn_x + BALL_SIZE, BALL_SIZE, fill='black', outline='orange')
        # Create the paddle
        paddle = canvas.create_rectangle(0, PADDLE_Y, paddle_width, CANVAS_HEIGHT - 120, fill='orange', outline='black')
        # Create the protected line
        line_bottom = canvas.create_line(0, BOTTOM_LINE_POS, CANVAS_WIDTH, BOTTOM_LINE_POS)
        # Show the player name in the left corner
        canvas.create_text(10, 10, anchor='nw', font='Courier 20',
                           text=str(player))
        # Show the player score in the bottom
        live_score = canvas.create_text(CANVAS_WIDTH / 2 - 90, CANVAS_HEIGHT - 75, anchor='nw', font='Courier 40', text=("Score " + str(player_points)))

        while True:
            mouse_x = canvas.winfo_pointerx()
            canvas.moveto(paddle, mouse_x, PADDLE_Y)
            canvas.move(ball, change_x, change_y)

            if hit_top_wall(canvas, ball):
                change_y *= -1

            if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
                change_x *= -1

            if hit_paddle(canvas, ball, paddle):
                # To increase the ball speed
                change_y *= -1.1
                change_x *= 1.1
                player_points += 6

                # Refresh the player score
                canvas.delete(live_score)
                live_score = canvas.create_text(CANVAS_WIDTH / 2 - 90, CANVAS_HEIGHT - 75, anchor='nw',
                                                font='Courier 40', text=("Score " + str(player_points)))
            if hit_bottom_line(canvas, ball, line_bottom):
                canvas.delete(live_score)
                canvas.delete(paddle)

                # Print GameOver and show the score
                canvas.create_text(250, CANVAS_HEIGHT / 2 - 50, anchor='nw', font='Cooper-Black 40',
                                   text='GameOver, the ball hit the ground')
                live_score = canvas.create_text(CANVAS_WIDTH / 2 - 180, CANVAS_HEIGHT / 2 + 40, anchor='nw',
                                                font='Cooper-Black 35', text=("You've Scored " + str(player_points)))

                break

            canvas.update()
            time.sleep(1/50)

        if player_points > highest_score:
            highest_score = player_points
        PLAYERS[player] = player_points
        print(player, " has scored ", PLAYERS[player], " points \n")

    print("The Scoreboard: ")

    for name, score in PLAYERS.items():
        print(name, " --> ", score)

    print_new_line()
    for name, score in PLAYERS.items():
        if score == highest_score:
            print("The winner is --> ", name, "\n with '", highest_score, "' points")



    canvas.mainloop()


def choose_difficulty_level():
    choose_difficulty = str(input("Choose the difficulty: \n Enter the difficulty level number:"
                                  "\n 1 for Easy\n 2 for Medium\n 3 for Hard \n   "))
    if choose_difficulty == '1':
        print("(Easy) level was chosen \n")
        return PADDLE_WIDTH_EASY
    elif choose_difficulty == '3':
        print("(Hard) level was chosen \n")
        return PADDLE_WIDTH_HARD
    else:
        print("(Medium) level was chosen")
        return PADDLE_WIDTH


def choose_number_of_players():
    num_players = int(input("How many players? "))
    for i in range(num_players):
        n = i + 1
        player_name = input("Enter player " + str(n) + ' name: ')
        PLAYERS[player_name] = 0


def print_players(players_dict):
    i = 1
    for player in players_dict:
        print("Player", i, ": ", player)
        i += 1


def sec_to_start(n):
    seconds = n
    while seconds > 0:
        print("Game stars in ", seconds)
        time.sleep(1)
        seconds -= 1


def print_new_line():
    print("\n")


def hit_bottom_wall(canvas, object):
    return get_top_y(canvas, object) >= CANVAS_HEIGHT - BALL_SIZE


def hit_top_wall(canvas, object):
    ball_top_y = get_top_y(canvas, object)
    return ball_top_y <= 0


def hit_right_wall(canvas, object):
    ball_left_x = get_left_x(canvas, object)
    return ball_left_x >= CANVAS_WIDTH - BALL_SIZE


def hit_left_wall(canvas, object):
    ball_left_x = get_left_x(canvas, object)
    return ball_left_x <= 0


def hit_paddle(canvas, ball, paddle):
    paddle_coords = canvas.coords(paddle)
    x1 = paddle_coords[0]
    y1 = paddle_coords[1]
    x2 = paddle_coords[2]
    y2 = paddle_coords[3]
    results = canvas.find_overlapping(x1, y1, x2, y2)
    return len(results) > 1


def hit_bottom_line(canvas, ball, line):
    line_coords = canvas.coords(line)
    x1 = line_coords[0]
    y1 = line_coords[1]
    x2 = line_coords[2]
    y2 = line_coords[3]
    results = canvas.find_overlapping(x1, y1, x2, y2)
    return len(results) > 1


def get_left_x(canvas, object):
    return canvas.coords(object)[0]


def get_top_y(canvas, object):
    return canvas.coords(object)[1]


def get_right_x(canvas, object):
    return canvas.coords(object)[2]


def get_bottom_y(canvas, object):
    return canvas.coords(object)[3]


def make_canvas(width, height, title):

    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
