import tkinter
import math
import numpy as np
from polygons import *
from h2geometry import *
from parametrization import *
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
                    #print("here")
                    #print("z1=", z1)
                    #print("z2=", z2)
                    #print("segment.z1=", segment.z1)
                    #print("segment.z2=", segment.z2)
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
            vertex1 = math.e ** (p.angles[i] * 1j)
            vertex2 = math.e ** (p.angles[(i + 1) % p.nr] * 1j)
            self.draw_H2_segment(vertex1, vertex2, color, complete = False)

    def draw_billiard_ball(self, ball_obj):
        '''Draws the ball at its initial position'''
        x, y = self.math_to_px(ball_obj.position.real, ball_obj.position.imag)
        ball = self.cv.create_oval(x-10, y-10, x+10, y+10, fill=ball_obj.color, outline=ball_obj.color)
        return ball
    
    def move_ball(self, ball, ball_obj, coords, delay):
        #update the position of the ball object
        for X, Y in coords:
            x, y = self.px_to_math(X, Y)
            ball_obj.position = x + y * 1j
            #update the position of the corresponding canvas object
            X0, Y0, X1, Y1 = self.cv.coords(ball)
            Oldx, Oldy = (X0 + X1) / 2, (Y0 + Y1) / 2 #current center point
            Dx, Dy = X - Oldx, Y - Oldy #amount of movement
            self.cv.move(ball, Dx, Dy)
            self.cv.update()

    def mov(self, ball, c, radius, coll_p):
        coords = []
        s = ball.position
        e = coll_p
        if e != -2 + 0j:
            a, b = ball.trajectory_ideal_endpoints(c, radius)
            delta_t = 0.005
            t = 0
            t_hit = abs(math.log(m(a,b,e).imag / m(a,b,s).imag))
            for j in range(math.floor(t_hit / delta_t)):
                z = gamma_D(s,e,a,b,t)
                x, y = z.real, z.imag
                X, Y = self.math_to_px(x, y)
                coords.append((X, Y))
                t = t + delta_t
        return coords

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
    
    def trajectory_ideal_endpoints(self, c_traj, r_traj):
        c, r = c_traj, r_traj
        if r != -1:
            p1, p2, ok = intersection_points_of_circles(r, 1, c, 0 + 0j)
        else:
            p1 = cos(self.angle) + sin(self.angle) * 1j
            p2 = -p1
        return p1, p2

    def intersection_ball_geodesic(self, s, c_traj, r_traj, first_iter, coll_p):
        r1, c1 = s.get_circle()
        r2, c2 =  r_traj, c_traj
        if r1 == -1 and r2 == -1:
            return 0 + 0j, True
        else:
            if r1 != -1 and r2 != -1:
                p1, p2, ok = intersection_points_of_circles(r1, r2, c1, c2)
            elif r1 != -1:
                if first_iter == True:
                    p1, p2, ok = intersection_points_line_circle_angle(r1, c1, self.position, self.angle)
                else:
                    p1, p2, ok = intersection_points_line_circle(r1, c1, coll_p, 0 + 0j)
            else:
                p1, p2, ok = intersection_points_line_circle(r2, c2, s.z1, s.z2)
            if math.sqrt(normsq(p1)) < 1:
                return p1, ok
            else:
                return p2, ok


    def collision(self, table, first_iter, e1, e2 = 0 + 0j):
        '''Finds the next collision point '''
        #1. Find the ideal endpoint that corresponds to our direction on the given trajectory 
        if first_iter == True:
            #e2 will not have the default value
            assert e2 != 0 + 0j
            c_traj, r_traj = self.trajectory()
            t1, t2, ok = intersection_points_line_circle_angle(1, 0 + 0j, self.position, self.angle)
            assert ok == True
            ang_t1 = (np.angle(t1 - self.position, deg=True) + 360) % 360
            if abs(ang_t1 - self.angle) <= 1.0:
                t = t1
            else:
                t = t2
            #e is the ideal endpoint we will be working with next
            if math.sqrt(normsq(t - e1)) < math.sqrt(normsq(t - e2)):
                e = e1
            else:
                e = e2
        else:
            assert e2 == 0 + 0j
            r_traj, c_traj = H2_segment(e1, self.position).get_circle()
            e = e1
        
        #2. Find out which side is being hit using the angle corresponding to e
        ang_e = (np.angle(e, deg=True) + 360) % 360
        for i in range(table.nr):
            if i != table.nr - 1:
                if math.degrees(table.angles[i]) <= ang_e and math.degrees(table.angles[i + 1]) >= ang_e:
                    vertex1 = math.e ** (table.angles[i] * 1j)
                    vertex2 = math.e ** (table.angles[i + 1] * 1j)
                    side = H2_segment(vertex1, vertex2)
                    break
            else:
                if math.degrees(table.angles[i]) % 360 <= ang_e and ang_e <= math.degrees(table.angles[0]):
                    vertex1 = math.e ** (table.angles[i] * 1j)
                    vertex2 = math.e ** (table.angles[0] * 1j)
                    side = H2_segment(vertex1, vertex2)
        
        coll_p, ok = self.intersection_ball_geodesic(side, c_traj, r_traj, first_iter, self.position)
        assert ok == True
        return side, coll_p, e
            
