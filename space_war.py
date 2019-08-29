import turtle
import os
import random
import time

turtle.fd(0)
# no animation, just draw it immediatly
turtle.speed(0)
# setup background and title
turtle.bgcolor("black")
turtle.bgpic("background.gif")
turtle.title("Very Fun Space War")
# play music in the background
os.system("afplay background_music.wav&")
# hide default turtle
turtle.ht()
turtle.setundobuffer(1)
# how many time you want to update your screen
# seted to no auto update now
turtle.tracer(0)


# Monster class
class Monster(turtle.Turtle):
    def __init__(self, monster_shape, color, init_x, init_y):
        turtle.Turtle.__init__(self, shape=monster_shape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(init_x, init_y)
        self.speed = 1

    # self is the current Monster object
    def move(self):
        self.fd(self.speed)

        # Only inside boundary
        # width of screen 700, border from -300 to 300
        if self.xcor() > 290:
            # just to make sure it does not go off the border
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def touch(self, other):
        if ((self.xcor() >= other.xcor() - 20) and
                (self.xcor() <= other.xcor() + 20) and
                (self.ycor() >= other.ycor() - 20) and
                (self.ycor() <= other.ycor() + 20)):
            # play explosion sound when Mosnters touch each other
            os.system("afplay explosion.wav&")
            return True
        else:
            return False;


class Player(Monster):
    def __init__(self, monster_shape, color, init_x, init_y):
        Monster.__init__(self, monster_shape, color, init_x, init_y)
        self.speed = 4
        # make player thinner and longer
        self.shapesize(0.6, 1.5, None)

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def speed_up(self):
        self.speed += 1

    def slow_down(self):
        self.speed -= 1


# weapon player can use to kill the enemy
class Weapon(Monster):
    def __init__(self, monster_shape, color, init_x, init_y):
        Monster.__init__(self, monster_shape, color, init_x, init_y)
        self.speed = 25
        self.status = "ready"
        self.shapesize(0.5, 0.5, None)
        self.setpos(-20000, -20000)

    def fire(self):
        if self.status == "ready":
            # play sound fire when fire a weapon
            # for some reason .mp3 do not work all the time, prefer .wav
            # add & so that game won't pause when sound is playing, sound will play in background
            os.system("afplay fire.wav&")
            # when fire, set pos and dir of weapon to player's
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "fire"

    def move(self):
        if self.status == "fire":
            self.fd(self.speed)
        if self.status == "ready":
            self.setpos(-1000, 1000)
        # Only inside boundary
        # width of screen 700, border from -300 to 300
        if self.xcor() > 290 or self.xcor() < -290 or \
                self.ycor() > 290 or self.ycor() < -290:
            self.status = "ready"
            self.setpos(-1000, 1000)


# probably need a better name
class BadMonster(Monster):
    def __init__(self, monster_shape, color, init_x, init_y):
        Monster.__init__(self, monster_shape, color, init_x, init_y)
        self.speed = 5
        self.setheading(random.randint(0, 360))


class GoodMonster(Monster):
    def __init__(self, monster_shape, color, init_x, init_y):
        Monster.__init__(self, monster_shape, color, init_x, init_y)
        self.speed = 5
        self.setheading(random.randint(0, 360))

    # Override move method in GoodMonster class
    def move(self):
        self.fd(self.speed)

        # Only inside boundary
        # width of screen 700, border from -300 to 300
        if self.xcor() > 290:
            # just to make sure it does not go off the border
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 5

    def draw_border(self):
        self.pen.speed(0)
        self.pen.penup()
        self.pen.pensize(5)
        self.pen.color("white")
        self.pen.setposition(-300, -300)
        self.pen.pendown()
        for i in range(0, 4):
            self.pen.fd(600)
            self.pen.lt(90)
        self.pen.penup()
        self.pen.ht()
        # when calling game_status the first time after draw_border, need to give it something to undo
        self.pen.pendown()

    def game_status(self):
        self.pen.undo()
        msg = "Level = " + str(self.level) + " " + \
              "Score = " + str(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

    # TODO update level and notify when up and down level
    def update_level(self):
        self.pen.undo()
        init_level = self.level
        self.level = self.score // 20
        if init_level != self.level:
            if init_level < self.level:
                msg = "Great! Level up. from " + str(init_level) + " to " + str(self.level)
            elif init_level > self.level:
                msg = "Not That Great! Level down. from " + str(init_level) + " to " + str(self.level)
                self.pen.goto(0, 0)
            self.pen.penup()
            self.pen.write(msg, font=("Arial", 16, "normal"))

    # TODO: add win and lost
    # def check_lost_or_win(self):
    #     if (self.level > 10):
    #         self.pen


# Create my Game
game = Game()
# draw border of the game
game.draw_border()
# show game status
game.game_status()


# Create my Player
player = Player("triangle", "red", 0, 0)
# Create weapon for player
weapon = Weapon("circle", "yellow", 0, 0)

# Create my Bad Monster(s)
# bm = BadMonster("square", "green", -100, 200)
bad_monsters = []
for _ in range(5):
    bad_monsters.append(BadMonster("square", "green", -100, 200))

# Create my Good Monster(s)
#gm = GoodMonster("square", "orange", -100, 200)
good_monsters = []
for _ in range(3):
    good_monsters.append(GoodMonster("square", "orange", -100, 200))

# Keyboard bindings
# !!! no () after turn_left !!!
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.speed_up, "Up")
turtle.onkey(player.slow_down, "Down")
# Surprisingly, space is lower case
turtle.onkey(weapon.fire, "space")
# after create binding, we need to tell turtle to listen
turtle.listen()

# Game Loop
while True:
    # update screen in game loop, after each round of calculation
    turtle.update()
    time.sleep(0.02)

    # Player is a child of Monster, so player can move
    player.move()
    weapon.move()
    for bm in bad_monsters:
        bm.move()
        # check if player touched bad monster
        if (player.touch(bm)):
            bm.setpos(random.randint(0, 300), random.randint(0, 300))
            game.score -= 10
            game.game_status()
            # game.update_level()
        # check if weapon hit bad monster
        if (weapon.touch(bm)):
            bm.setpos(random.randint(-280, 280), random.randint(-280, 280))
            weapon.status = "ready"
            game.score += 10
            game.game_status()
            # game.update_level()

    for gm in good_monsters:
        gm.move()
        # check if weapon hit good monster
        if (weapon.touch(gm)):
            gm.setpos(random.randint(-280, 280), random.randint(-280, 280))
            weapon.status = "ready"
            game.score -= 5
            game.game_status()
            # game.update_level()






# show until user press enter
delay = input("Press enter to quit")
