import tkinter
from canvas import *
from polygons import *
import math

DELAY = 100
N = 3

def initialization():
    first_window = tkinter.Tk()
    first_window.title("Billiards in the hyperbolic plane")
    frame = tkinter.Frame(first_window)
    frame.pack()

    #Enter position
    label_pos = tkinter.Label(frame, text="Please enter an initial position with (x, y) values:")
    label_pos.pack()

    #Enter a value for x
    frame_x = tkinter.Frame(frame)
    frame_x.pack()
    xLabel = tkinter.Label(frame_x, text = "x")
    xLabel.pack(side = "left")
    x_e = tkinter.Entry(frame_x, textvariable = tkinter.StringVar(), exportselection = 0)
    x_e.pack(side = "left")

    #Enter a value for y
    frame_y = tkinter.Frame(frame)
    frame_y.pack()
    yLabel = tkinter.Label(frame_y, text = "y")
    yLabel.pack(side = "left")
    y_e = tkinter.Entry(frame_y, textvariable = tkinter.StringVar(), exportselection = 0)
    y_e.pack(side = "left")

    #Enter angle of tangency
    frame_ang = tkinter.Frame(frame)
    frame_ang.pack()
    label_angle = tkinter.Label(frame_ang, text = "Please enter a value for the angle:")
    label_angle.pack(side = "left")
    angle_e = tkinter.Entry(frame_ang, textvariable = tkinter.StringVar(), exportselection = 0)
    angle_e.pack(side = "left")

    def get_and_check():
        #Get the values of (x, y) and angle
        x = x_e.get()
        y = y_e.get()
        angle = angle_e.get()

        z = float(x) + float(y) * 1j
        if on_the_table(z) == False:
            label = tkinter.Label(frame, text = "The starting position should be within the table!", fg = "red")
            label.pack()
        else:
            first_window.destroy()
            start_billiards(z, float(angle))

    #Check the introduced values
    printButton = tkinter.Button(first_window, text = "Enter", command = get_and_check)
    printButton.pack()
    first_window.bind('<Return>', get_and_check)
    first_window.mainloop()


def on_the_table(z):
    min_x = min([table.vertices[i].real for i in range(table.nr)])
    max_x = max([table.vertices[i].real for i in range(table.nr)])
    min_y = min([table.vertices[i].imag for i in range(table.nr)])
    max_y = max([table.vertices[i].imag for i in range(table.nr)])
    if not(z.real <= max_x and z.real >= min_x and z.imag <= max_y and z.imag >= min_y):
        return False
    for i in range(table.nr):
        s = H2_segment(table.vertices[i], table.vertices[(i+1) % table.nr])
        r, c = s.get_circle()
        if normsq(z - c) <= r ** 2:
            return False
    return True

def start_billiards(z, angle):
    window = Window()
    window.canvas.draw_polygon(table, "green")
    #z is the starting position 
    window.canvas.draw_point(z)
    #an object of type Ball and a graphical object looking like a ball
    ball_obj = Ball(z, angle, "blue")
    ball = window.canvas.draw_billiard_ball(ball_obj)

    for i in range(N):
        if i == 0:
            #find the trajectory of the ball
            c, radius = ball_obj.trajectory()
            #search for the collision point coll_p of the ball with one side s of the table
            s, coll_p = ball_obj.collision(window.canvas, table, ball_obj.position, c, radius, True)
        else:
            s, coll_p = change_direction(window, ball_obj, s, coll_p, c, radius)
            radius, c = H2_segment(coll_p, ball_obj.position).get_circle()

        window.canvas.draw_H2_segment(ball_obj.position, coll_p, color="orange", complete = False)
        path_iter = ball_obj.mov(window.canvas, table, c, radius, coll_p)
        ball_obj_copy = ball_obj
        window.top.after(DELAY, window.canvas.move_ball, ball, ball_obj_copy, path_iter, DELAY)
    window.run()

def change_direction(window, ball_obj, s, coll_point, c_traj, r_traj):
    refl_table = table.reflect(s)
    #window.canvas.draw_polygon(refl_table, color = "blue")
    s2, z2 = ball_obj.collision(window.canvas, refl_table, coll_point, c_traj, r_traj, False)
    #print("z2=", z2)
    #window.canvas.draw_point(z2, color = "purple")
    #window.canvas.draw_H2_segment(coll_point, z2, color = "red", complete=False)
    z2_ref = H2_reflection(s).reflect(z2)
    a, b = s2.z1, s2.z2
    a_ref = H2_reflection(s).reflect(a)
    b_ref = H2_reflection(s).reflect(b)
    s2_ref = H2_segment(a_ref, b_ref)
    ball_obj.position = coll_point
    return s2_ref, z2_ref

nr = 5
vertices = [math.e ** ((2 * math.pi * l) / nr * 1j) for l in range(1,nr + 1)]
table = Polygon(nr, vertices)
initialization()

