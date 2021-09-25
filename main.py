import tkinter
from canvas import *
from polygons import *


#Goal: given a starting position and a direction, simulate the movement of a ball on a polygon in the Poincare disk
#Still TO DO:
#  * a separate window where the user sets valid values for a staring position and the direction/angle and perhaps also how the table/polygon looks like -- a list of vertices perhaps
#  * a function which takes as parameters a tuple (x, y) for a position and an angle and moves the ball until it has hit the sides of the table a certain number of times (also a parameter)
#  * a method called 'collision' of the class Ball, which changes the direction of the moving ball when it hits a side of the polygon

#This was just for experimenting
window = Window()
#an example for a polygon
vertices = [0.5 + 0.5j, -0.5 + 0.5j, -0.5 -0.5j, 0.5 - 0.5j]
p = Polygon(len(vertices), vertices)
window.canvas.draw_polygon(p, "blue")
ball = Ball(0+0j, 0, "green")
window.canvas.draw_billiard_ball(ball)
window.run()
