import tkinter
import math
import numpy as np
from polygons import *
from h2geometry import *
from tools import *

sin = lambda degs: math.sin(math.radians(degs))
cos = lambda degs: math.cos(math.radians(degs))
arctan = lambda degs: math.atan(math.radians(degs))
arcsin = lambda degs: math.asin(math.radians(degs))

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
        segment = H2_segment(z1, z2)
        #self.draw_point(z1,"red")
        #self.draw_point(z2,"red")
        #find the Euclidean circle that includes z1 and z2 and is centered on the boundary of the disk
        if z1 != z2:
            r, c = segment.get_circle()
            #get the corresponding ideal endpoints if complete == True
            if complete == True:
                e1, e2 = segment.get_ideal_endpoints()
                self.draw_point(e1,"blue")
                self.draw_point(e2,"blue")
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r == -1 and c == 0 + 0j:
                    self.draw_segment(e1, e2, color)
                else:
                    self.draw_circle_arc(c, r, e1, e2, color)
            else:
                #draw only the arc circle between z1 and z2
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r == -1 and c == 0 + 0j:
                    self.draw_segment(z1, z2, color)
                else:
                    self.draw_circle_arc(c, r, z1, z2, color)

    def draw_polygon(self, p, color):
        ''' Draws a hyperbolic polygon '''
        for i in range(p.nr):
            self.draw_H2_segment(p.vertices[i % p.nr],p.vertices[(i + 1) % p.nr], color, complete = False)

    def draw_billiard_ball(self, ball_obj):
        '''Draws the ball at its initial position'''
        x, y = self.math_to_px(ball_obj.position.real, ball_obj.position.imag)
        ball = self.cv.create_oval(x-10, y-10, x+10, y+10, fill=ball_obj.color, outline=ball_obj.color)
        return ball
    
    def move_ball(self, ball, ball_obj, path_iter, delay):
        #update the position of the ball object
        X, Y = next(path_iter, (-2,-2))
        x, y = self.px_to_math(X, Y)
        ball_obj.position = x + y * 1j
        #-2 tells us that the iterator has been exhausted --> collision with one side
        if ball_obj.position.real != -2:
            #update the position of the corresponding canvas object
            X0, Y0, X1, Y1 = self.cv.coords(ball)
            Oldx, Oldy = (X0+X1) // 2, (Y0+Y1) // 2 #current center point
            Dx, Dy = X - Oldx, Y - Oldy #amount of movement
            self.cv.move(ball, Dx, Dy)
            self.cv.after(delay, self.move_ball, ball, ball_obj, path_iter, delay)

class Ball:
    def __init__(self, position, angle, color):
        self.position = position
        self.angle = angle
        self.color = color
    
    def trajectory(self):
        ''' Returns the centre and the radius of the corresponding geodesic '''
        x, y = self.position.real, self.position.imag
        z = x + y * 1j
        ang = self.angle
        if abs(-x * sin(ang) + y * cos(ang)) > 1e-5:
            c1 = x - (1 - normsq(z)) * sin(ang) / (2 * (-x * sin(ang) + y * cos(ang)))
            c2 = y + (1 - normsq(z)) * cos(ang) / (2 * (-x * sin(ang) + y * cos(ang)))
            c = c1 + c2 * 1j
            radius = (1 - normsq(z)) / abs(2 * (-x * sin(ang) + y * cos(ang)))
        else:
            c = 0 + 0j
            radius = -1
        return c, radius

    def movement(self, canvas, c, radius, delta_ang):
        """ Generates coordinates corresponding to the geodesic it is moving along"""
        if radius > 0:
            start_ang = np.angle(c - self.position, deg=True) 
            ang = start_ang
            while True:
                x = c.real + radius * cos(ang)
                y = c.imag + radius * sin(ang)
                z = x + y * 1j
                #generate only points that remain within the billiard table -->condition here
                #just stay within the Poincare disk for the moment
                ang = ang + delta_ang
                if math.sqrt(normsq(z)) > 1:
                    continue
                else:
                    X, Y = canvas.math_to_px(x, y)
                    yield X, Y
        else:
            #Geodesic is a euclidean line through the origin
            z1 = 0 + 0j
            X, Y = canvas.math_to_px(0, 0)
            yield X, Y
            z2 = self.position
            s = H2_segment(z1, z2)
            e1, e2 = s.get_ideal_endpoints()
            dx = 0.1
            if e1.real < e2.real:
                x, y = e1.real, e1.imag
            else:
                x, y = e2.real, e2.imag
            X, Y = canvas.math_to_px(x, y)
            yield X, Y
            while True:
                x = x + dx
                y = x * sin(self.angle) / cos(self.angle)
                z = x + y * 1j
                if math.sqrt(normsq(z)) > 1:
                    print('here')
                    break
                else:
                    X, Y = canvas.math_to_px(x, y)
                    yield X, Y