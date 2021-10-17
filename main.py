import tkinter
from canvas import *
from billiards import *
import math

DELAY = 500
N = 10

def initialization():
    first_window = tkinter.Tk()
    first_window.title("Billiards in the hyperbolic plane")
    frame = tkinter.Frame(first_window, width = 600, height = 600)

    frame.pack()

    #Enter position
    label_pos = tkinter.Label(frame, text="Please enter an initial position with (x, y) values:", font = ("Helvetica", 18))
    label_pos.grid(row = 0)

    #Enter a value for x
    xLabel = tkinter.Label(frame, text = "x", font = ("Helvetica", 18))
    xLabel.grid(row = 1)
    x_e = tkinter.Entry(frame, textvariable = tkinter.StringVar(),font = ("Helvetica", 18), exportselection = 0)
    x_e.grid(row = 1, column = 1)

    #Enter a value for y
    yLabel = tkinter.Label(frame, text = "y", font = ("Helvetica", 18))
    yLabel.grid(row = 2)
    y_e = tkinter.Entry(frame, textvariable = tkinter.StringVar(),font = ("Helvetica", 18), exportselection = 0)
    y_e.grid(row = 2, column = 1)

    #Enter angle of tangency
    label_angle = tkinter.Label(frame, text = "Please enter a value for the angle:", font = ("Helvetica", 18))
    label_angle.grid(row = 3)
    angle_e = tkinter.Entry(frame, textvariable = tkinter.StringVar(),font = ("Helvetica", 18), exportselection = 0)
    angle_e.grid(row = 3, column = 1)

    def get_and_check():
        #Get the values of (x, y) and angle
        x = x_e.get()
        y = y_e.get()
        angle = angle_e.get()

        z = float(x) + float(y) * 1j
        if on_the_table(z) == False:
            label_error = tkinter.Label(frame, text = "The starting position should be within the table!", fg = "red", font = ("Helvetica", 18))
            label_error.grid(row = 4)
        else:
            first_window.destroy()
            start_billiards(z, (float(angle) + 360) % 360)

    #Check the introduced values
    printButton = tkinter.Button(first_window, text = "Enter", font = ("Helvetica", 18), command = get_and_check)
    printButton.pack(pady = 20)
    first_window.bind('<Return>', get_and_check)
    first_window.mainloop()


def on_the_table(z):
    min_x = min([(math.e ** (table.angles[i] * 1j)).real for i in range(table.nr)])
    max_x = max([(math.e ** (table.angles[i] * 1j)).real for i in range(table.nr)])
    min_y = min([(math.e ** (table.angles[i] * 1j)).imag for i in range(table.nr)])
    max_y = max([(math.e ** (table.angles[i] * 1j)).imag for i in range(table.nr)])
    if not(z.real <= max_x and z.real >= min_x and z.imag <= max_y and z.imag >= min_y):
        return False
    for i in range(table.nr):
        s = H2_segment(math.e ** (table.angles[i] * 1j), (math.e ** (table.angles[(i + 1) % table.nr] * 1j)))
        r, c = s.get_circle()
        if normsq(z - c) <= r ** 2:
            return False
    return True

def start_billiards(z, angle):
    window = Window()
    window.canvas.draw_polygon(table, "green")
    window.canvas.draw_point(z)
    ball_obj = Ball(z, angle, "blue")
    ball_copy = ball_obj
    ball = window.canvas.draw_billiard_ball(ball_obj)
    #coords is a list of points along the trajectory of the ball
    coords = []

    for i in range(N):
        if i == 0:
            #find the trajectory of the ball
            c, radius = ball_obj.trajectory()
            e1, e2 = ball_obj.trajectory_ideal_endpoints(c, radius)
            #search for the collision point coll_p of the ball with one side s of the table
            s, coll_p, e = ball_obj.collision(table, True, e1, e2)
        else:
            ball_obj.position = coll_p
            e = H2_reflection(s).reflect(e)
            s, coll_p, dummy_e = ball_obj.collision(table, False, e)
            window.canvas.draw_point(coll_p, "pink")
            radius, c = H2_segment(coll_p, ball_obj.position).get_circle()

        window.canvas.draw_H2_segment(ball_obj.position, coll_p, color="orange", complete = False)
        coords = coords + window.canvas.mov(ball_obj, c, radius, coll_p)
    
    window.canvas.move_ball(ball, ball_copy, coords, DELAY)
    window.run()

nr = 6
angles = [2 * math.pi * l / nr for l in range(1, nr + 1)]
table = Polygon(nr, angles)
initialization()

