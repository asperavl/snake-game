#importing all the modules we need

import random
import time
import turtle
import mysql.connector as mys
from datetime import datetime
import csv

passkey = input("Enter mysql root password ")



def Game():

    # Setting some basic values for our game

    score = 0
    speed = 0.1

    # This list will house all parts of the snake object

    bodies = []

    # Setting up the surface on which the snake and apple spawn

    screen = turtle.Screen()
    turtle.TurtleScreen._RUNNING = True
    screen.title("Snake Game!")
    screen.bgcolor('#4b5320')
    screen.setup(width=800, height=600)

    # Defining characteristics of the snake's head onto our surface

    head = turtle.Turtle()
    head.speed(0)
    head.shape('square')
    head.color('red')                        #
    head.fillcolor('blue')
    head.penup()
    head.goto(0,0)
    head.direction = 'stop'

    # Initialising the apple onto our surface

    apple = turtle.Turtle()
    apple.speed(0)
    apple.shape('circle')
    apple.color('green')
    apple.fillcolor('red')
    apple.penup()
    apple.ht()
    apple.goto(200,200)
    apple.st()

    # Creating a rudimentary scoreboard on the top right of the screen

    score_board = turtle.Turtle()
    score_board.penup()
    score_board.goto(300,200)
    score_board.write("Your Score: {}".format(score))

    # This section of code basically ensures that the snake can never do a 180 degree turn directly
    # and it makes sure that the snake keeps moving in the same direction unless the player changes it explicitly

    def move_up():
        if head.direction != "down":
            head.direction = "up"

    def move_down():
        if head.direction != "up":
            head.direction = "down"

    def move_left():
        if head.direction != "right":
            head.direction = "left"

    def move_right():
        if head.direction != "left":
            head.direction = "right"

    # This function defines the amount of pixels the snake moves per movement

    def move():
        if head.direction == "up":
            y=head.ycor()
            head.sety(y+30)

        if head.direction == "down":
            y=head.ycor()
            head.sety(y-30)

        if head.direction == "left":
            x=head.xcor()
            head.setx(x-30)

        if head.direction == "right":
            x=head.xcor()
            head.setx(x+30)

    # These commands bind the snake's movement to the arrow keys on the keyboard

    screen.listen()
    screen.onkey(move_up, "Up")
    screen.onkey(move_down, "Down")
    screen.onkey(move_left, "Left")
    screen.onkey(move_right, "Right")

    # This function defines what happens when a game over scenario occurs
    # Once it is called, it ends the program along with giving the user a 5-second window before it autocloses

    def quit():
        global running
        time.sleep(5)
        running = False
        turtle.bye()

    # This is our main game execution loop

    running = True

    while running:


        # This command displays changes on the screen

        screen.update()

        # These lines of code ensure that the snake cannot escape the borders of our game

        if head.xcor() > 390:
            head.setx(-390)
        if head.xcor() < -390:
            head.setx(390)
        if head.ycor() > 290:
            head.sety(-290)
        if head.ycor() < -290:
            head.sety(290)

        # These lines of code are the logic involved when the snake "eats" an apple

        if head.distance(apple) < 25:

           # Spawns an apple on another part of the screen using random module

            x=random.randint(-390,391)
            y=random.randint(-290,291)
            apple.goto(x,y)

            # This adds a block to the snake every time it eats an apple

            body=turtle.Turtle()
            body.speed(0)
            body.penup()
            body.shape('square')
            body.color('blue')
            body.fillcolor('black')
            bodies.append(body)

            #Scoring system, where score is the total amount of apples eaten

            score += 1
            score_board.clear()
            score_board.write("Your Score: {}".format(score))

            # Speed increased by small increments to increase difficulty (involves time.sleep() command)

            speed -= 0.005

        # These lines of code shows how the snake turns when the snake exceeds the length of one block

        for i in range(len(bodies)-1, 0, -1):
            x=bodies[i-1].xcor()
            y=bodies[i-1].ycor()
            bodies[i].goto(x,y)

        if len(bodies) > 0:
            x=head.xcor()
            y=head.ycor()
            bodies[0].goto(x,y)

        # Calling move() function

        move()

        # Game over logic (When the head of the snake tries to 'eat' its own body)

        for body in bodies:
            if body.distance(head) < 20:

                head.goto(0,0)
                head.direction = 'stop'

                # Clears the bodies from the screen

                for body in bodies:
                    body.ht()
                bodies.clear()

                # The entire screen is wiped to create a new surface to show results

                screen.clear()

                # Initialising a surface 'Results' to show the final score of the player

                Result = turtle.Turtle()
                Result.penup()
                Result.write(" Game Over! \nYour Final Score is: {}, "
                             "\nGame will autoclose.".format(score),
                             align='center',
                             font=('Arial', 35, 'bold'))
                # Calling quit() function

                quit()

                # Final score is returned to enter it into the database

                return score

        # This is the delay involved during continuous movement of the block

        time.sleep(speed)
    # This keeps the screen active until the game is over

    screen.mainloop()


# Basic MySQL function to add a score to the database every time a person plays the game

def score_add():
    finalscore = Game()
    con = mys.connect(host='localhost',user='root',password=passkey,database='snake')
    cur = con.cursor()
    name = input("Enter your name: ")
    s = datetime.now()
    nowdate = s.strftime("%Y-%m-%d")
    query = "insert into snake_scores values('{}',{},'{}')".format(name,finalscore,nowdate)
    cur.execute(query)
    print("New score added to the database!")
    con.commit()
    con.close()

# Basic MySQL function to express the scores from the database from latest to earliest score

def show_scores_by_date():
    con = mys.connect(host='localhost', user='root', password=passkey, database='snake')
    cur = con.cursor()
    cur.execute("select * from snake_scores ORDER BY Date_of_Score asc")
    info = cur.fetchall()
    if len(info) == 0:
        print("No scores...")
    else:
        for i in info:
            s = i[2]
            date = s.strftime("%Y-%m-%d")
            print([i[0],i[1],date])
    con.close()

# MySQL function to express the scores from the database from the highest score to the lowest score

def show_scores_by_highscores():
    con = mys.connect(host='localhost', user='root', password=passkey, database='snake')
    cur = con.cursor()
    cur.execute("select * from snake_scores ORDER BY Score desc")
    info = cur.fetchall()
    if len(info) == 0:
        print("No scores...")
    else:
        for i in info:
            s = i[2]
            date = s.strftime("%Y-%m-%d")
            print([i[0], i[1], date])
    con.close()

# MySQL function to delete every score from the database to start fresh

def delete_all_scores():
    con = mys.connect(host='localhost', user='root', password=passkey, database='snake')
    cur = con.cursor()
    cur.execute("DELETE from snake_scores")
    print("All scores DELETED!")
    con.commit()
    con.close()

# Function to export scores from the database to a .csv file

def score_export():
    con = mys.connect(host='localhost', user='root', password=passkey, database='snake')
    cur = con.cursor()
    cur.execute("select * from snake_scores")
    info = cur.fetchall()
    f = open("scores.csv", "w")
    x = csv.writer(f)
    x.writerow(["Name", "Score", "Date_of_Score"])
    for i in info:
        s = i[2]
        date = s.strftime("%Y-%m-%d")
        single_score=([i[0], i[1], date])
        x.writerow(single_score)
    f.close()

# Main loop (Menu Driven loop)

while True:
    print("Here are your choices!")
    print("1. Play the snake game!")
    print("2. Display scores!")
    print("3. Delete all scores!")
    print("4. Export scores to a .csv file")
    print("5. Exit the program... ")
    time.sleep(0.5)
    choice = int(input("Enter your choice: "))

    if choice == 1:
        score_add()
        time.sleep(0.05)

    elif choice == 2:
        while True:
            print("You can display scores by either: ")
            print("1. From latest to earliest scores")
            print("or")
            print("2. From highest score to lowest score")
            time.sleep(0.05)
            ch = int(input("Enter mode of display (Enter either 1 or 2) "))

            if ch == 1:
                show_scores_by_date()
                time.sleep(0.05)
                break
            elif ch == 2:
                show_scores_by_highscores()
                time.sleep(0.05)
                break
            else:
                print("Invalid choice, choose from the given options!")
                time.sleep(0.05)

    elif choice == 3:
        del_ch = input("Are you sure you want to delete all your scores? (enter 'y' to delete) ")
        if del_ch == 'y':
            delete_all_scores()
        time.sleep(0.05)

    elif choice == 4:
        score_export()
        print("Scores exported successfully!")
        time.sleep(0.05)

    elif choice == 5:
        print("This session has ended, see you next time!")
        time.sleep(2.5)
        break

    else:
        print("Invalid choice... Try selecting from the given choices!")
        time.sleep(0.05)


# End of the program
