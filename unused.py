def collision(self, canvas, table, prev_point, c_traj, r_traj, first_iter):
        for i in range(table.nr):
            s = H2_segment(table.vertices[i], table.vertices[(i + 1) % table.nr])
            z, ok = self.intersection_ball_geodesic(s, c_traj, r_traj, first_iter, prev_point)
            if ok == True:
                e1, e2 = self.trajectory_ideal_endpoints(c_traj, r_traj)
                if first_iter == True:
                    t1, t2, ok = intersection_points_line_circle_angle(1, 0 + 0j, self.position, self.angle)
                    assert ok == True
                    ang1 = np.angle(t1 - self.position, deg = True)
                    if abs(abs(ang1) - abs(self.angle)) <= 1.0:
                        t = t1
                    else:
                        t = t2
                    #canvas.draw_point(t, color = "green")
                    if math.sqrt(normsq(t - e1)) < math.sqrt(normsq(t - e2)):
                        e = e1
                    else:
                        e = e2
                else:
                    if z != prev_point:
                        r_s, c_s = s.get_circle()
                        if math.sqrt(normsq(c_s - e1)) <= r_s:
                            e = e1
                        else:
                            e = e2    
                    else:
                        continue           
                #canvas.draw_point(e, color = "yellow") 
                if r_traj != -1:
                    ang_self_c = np.angle(c_traj - self.position)
                    ang_e_c = np.angle(c_traj - e)
                    ang_z_c = np.angle(c_traj - z)
                    if ang_z_c >= min(ang_self_c, ang_e_c) and ang_z_c <= max(ang_self_c, ang_e_c):
                        return s, z
                else:
                    if abs(math.sqrt(normsq(z - c_traj)) + math.sqrt(normsq(z - e)) - math.sqrt(normsq(c_traj - e))) < 1e-4:
                        return s, z
        #if the ball has not hit any side of the table, then it must have hit a vertex
        print("Check if it has hit a vertex")
        return H2_segment(0 + 0j, 0 + 0j), -2 + 0j



def change_direction(window, ball_obj, s, coll_point, c_traj, r_traj):
    refl_table = table.reflect(s)
    window.canvas.draw_polygon(refl_table, color = "blue")
    s2, z2 = ball_obj.collision(window.canvas, refl_table, coll_point, c_traj, r_traj, False)
    #print("z2=", z2)
    window.canvas.draw_point(z2, color = "purple")
    window.canvas.draw_H2_segment(coll_point, z2, color = "red", complete=False)
    z2_ref = H2_reflection(s).reflect(z2)
    a, b = s2.z1, s2.z2
    a_ref = H2_reflection(s).reflect(a)
    b_ref = H2_reflection(s).reflect(b)
    s2_ref = H2_segment(a_ref, b_ref)
    ball_obj.position = coll_point
    return s2_ref, z2_ref