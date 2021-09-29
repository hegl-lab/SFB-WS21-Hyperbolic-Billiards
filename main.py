import tkinter
from canvas import *
from polygons import *

DELAY = 100

#Goal: given a starting position and a direction, simulate the movement of a ball on a polygon in the Poincare disk
#Still TO DO:
#  * a separate window where the user sets valid values for a staring position and the direction/angle and perhaps also how the table/polygon looks like -- a list of vertices perhaps
#  * a function which takes as parameters a tuple (x, y) for a position and an angle and moves the ball until it has hit the sides of the table a certain number of times (also a parameter)
#  * a method called 'collision' of the class Ball, which changes the direction of the moving ball when it hits a side of the polygon

window = Window()
#PROBLEM: z1 = 0 + 0j
z1 = 0.3 + 0.5j
window.canvas.draw_point(z1)
angle = 45
ball_obj = Ball(z1, angle, "green")
ball = window.canvas.draw_billiard_ball(ball_obj)
c, radius = ball_obj.trajectory()
delta_ang = 1
path_iter = ball_obj.movement(window.canvas, c, radius, delta_ang)
X, Y = next(path_iter)
x2, y2 = window.canvas.px_to_math(X, Y)
z2 = x2 + y2 * 1j
window.canvas.draw_H2_segment(z1, z2,'red')
window.top.after(DELAY, window.canvas.move_ball, ball, ball_obj, path_iter, DELAY)
window.run()
