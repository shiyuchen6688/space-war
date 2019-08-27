import turtle
import os
import random

turtle.fd(0)
# no animation, just draw it immediatly
turtle.speed(0)
turtle.bgcolor("black")
# hide default turtle
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(1)


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
            return True
        else:
            return False;


class Player(Monster):
    def __init__(self, monster_shape, color, init_x, init_y):
        Monster.__init__(self, monster_shape, color, init_x, init_y)
        self.speed = 4
        # Only player have lives, monster does not
        self.lives = 3

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


# Create my Game
game = Game()
# draw border of the game
game.draw_border()

# Create my Player
player = Player("triangle", "red", 0, 0)
# Create weapon for player
weapon = Weapon("circle", "yellow", 0, 0)

# Create my Bad Monster
bm = BadMonster("square", "green", -100, 200)
# Create my Good Monster
gm = GoodMonster("square", "orange", -100, 200)

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
    # Player is a child of Monster, so player can move
    player.move()
    weapon.move()
    bm.move()
    gm.move()

    # check if player touched bad monster
    if (player.touch(bm)):
        bm.setpos(random.randint(0, 300), random.randint(0, 300))

    # check if weapon hit bad monster
    if (weapon.touch(bm)):
        bm.setpos(random.randint(-280, 280), random.randint(-280, 280))
        weapon.status = "ready"
        game.score += 1

    # check if weapon hit good monster
    if (weapon.touch(gm)):
        gm.setpos(random.randint(-280, 280), random.randint(-280, 280))
        weapon.status = "ready"
        game.score -= 1



# show until user press enter
delay = input("Press enter to quit")
