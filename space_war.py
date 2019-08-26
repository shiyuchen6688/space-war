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

class Player(Monster):
    # TODO start here making the player class

# Create my monster
player = Monster("triangle", "red", 0, 0)


# Main Game
while True:
    player.move()


# show until user press enter
delay = input("Press enter to quit")


