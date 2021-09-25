import tkinter
import math
import numpy as np
from polygons import *
from h2geometry import *
from tools import *

class Window:
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("Billiards in the Poincare Disk")
        self.canvas = Canvas(self.top)

    def run(self):
        self.top.mainloop()

class Canvas:
    def __init__(self, top):
        self.size_math = 2 * 1.2
        self.size_px = 0.9 * min(top.winfo_screenwidth(), top.winfo_screenheight())
        self.origin_X = self.size_px/2
        self.origin_Y = self.size_px/2
        self.scale = self.size_px/self.size_math
        self.next = "red"
        
        self.cv = tkinter.Canvas(top, width=self.size_px, height=self.size_px, bg="white")
        self.cv.focus_set()
        self.cv.pack()
        self.draw_circle(0, 1, "purple")

    def px_to_math(self, X, Y):
        x = (X - self.origin_X)/self.scale
        y = -(Y - self.origin_Y)/self.scale
        return x, y
        
    def math_to_px(self, x, y):
        X = np.rint(x*self.scale + self.origin_X)
        Y = np.rint(-(y*self.scale) + self.origin_Y)
        return X, Y
    
    def draw_point(self, z, color="black"):
        ''' Here z is a point in the plane given by a complex coordinate '''
        X, Y = self.math_to_px(z.real, z.imag)
        self.cv.create_oval(X-1, Y-1, X+2, Y+2, fill=color, outline=color, width=3)
        
    def draw_segment(self, z1, z2, color):
        self.draw_broken_line([z1, z2], color)

    def draw_broken_line(self, z, color):
        ''' Here z is a list of points given by their complex coordinates '''
        X, Y = self.math_to_px(np.real(z), np.imag(z))
        points = [[X[i], Y[i]] for i in range(len(X))]
        self.cv.create_line(points, fill=color, width=2)
        
    def draw_circle(self, c, r, color):
        X, Y = self.math_to_px(c.real, c.imag)
        R = np.rint(self.scale*r)
        self.cv.create_oval(X-R, Y-R, X+R+1, Y+R+1, outline=color, width=2)
        
    def draw_circle_arc(self, c, r, z1, z2, color):
        angle1 = mod2pi(np.angle(z1 - c))
        angle2 = mod2pi(np.angle(z2 - c))
        if ((z2-c)*((z1-c).conjugate())).imag < 0:
            angle1, angle2 = angle2, angle1
        X, Y = self.math_to_px(c.real,c.imag)
        R = self.scale*r
        self.cv.create_arc(X-R, Y-R, X+R+1, Y+R+1, start=angle1*180/np.pi, extent=mod2pi(angle2-angle1)*180/np.pi, outline=color, style=tkinter.ARC, width=1)
        
    def draw_H2_segment(self, z1, z2, color="blue", complete=True):
        ''' Draws the hyperbolic segment between two points '''
        #define an H2_segment object
        segment=H2_segment(z1, z2)
        #self.draw_point(z1,"red")
        #self.draw_point(z2,"red")
        #find the Euclidean circle that includes z1 and z2 and is centered on the boundary of the disk
        if z1!=z2:
            r, c=segment.get_circle()
            #get the corresponding ideal endpoints if complete == True
            if complete == True:
                e1, e2=segment.get_ideal_endpoints()
                self.draw_point(e1,"blue")
                self.draw_point(e2,"blue")
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r==-1 and c==0+0*1j:
                    self.draw_segment(e1, e2, color)
                else:
                    self.draw_circle_arc(c, r, e1, e2, color)
            else:
                #draw only the arc circle between z1 and z2
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r==-1 and c==0+0*1j:
                    self.draw_segment(z1, z2, color)
                else:
                    self.draw_circle_arc(c, r, z1, z2, color)

    def draw_polygon(self, p, color):
        ''' Draws a hyperbolic polygon '''
        for i in range(p.nr):
            self.draw_H2_segment(p.vertices[i % p.nr],p.vertices[(i + 1) % p.nr], color, complete = False)

    def draw_billiard_ball(self, ball):
        '''Draws the ball at its initial position'''
        x, y = self.math_to_px(ball.position.real, ball.position.imag)
        self.cv.create_oval(x-10, y-10, x+10, y+10, fill=ball.color, outline=ball.color)

    def move_billiard_ball(self, ball):
        self.cv.move(ball, )
    
class Ball:
    def __init__(self, position, direction, color):
        self.position = position
        self.direction = direction
        self.color = color

    #def collision(self, tableSide):
