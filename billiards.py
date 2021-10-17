from h2geometry import *
import math
import numpy as np
from parametrization import *
from tools import *

class Polygon:
    def __init__(self, nr, angles):
        self.nr = nr
        self.angles = angles
    
    def reflect(self, s):
        '''It reflects a polygon across a given geodesic s and returns the new polygon'''
        new_angles = []
        for angle in self.angles:
            vertex = math.e ** (angle * 1j)
            ref = H2_reflection(s).reflect(vertex)
            new_ang = np.angle(ref)
            new_angles.append(new_ang)
        return Polygon(self.nr, new_angles)


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