import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

class LinePlot():

    def __init__(self, m, b):
        self.m = m
        self.b = b

    def plot_line(self):
        glBegin(GL_LINES)
        for x in [-1, 1]:
            y = self.m * x + self.b
            glVertex2f(x, y)
        glEnd()

class PointPlot():

    def __init__(self):
        self.points = []
    
    def add_point(self, x, y):
        self.points.append((x, y))

    def plot_point(self):
        glBegin(GL_LINE_STRIP)
        for x, y in self.points:
            glVertex2f(x, y)
        glEnd()

    def mouse_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            window_size = glfw.get_window_size(window)
            x = x / window_size[0] * 2 - 1
            y = y / window_size[1] * 2 - 1
            self.add_point(x, -y)

class GridVisualizer():
    
    def __init__(self, num_rows=10, num_cols=10, color = (0.3, 0.3, 0.4)):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.color = color
        self.axis_color = (1.0, 1.0, 1.0)
        self.line_thickness = 1
    
    def plot_grid(self):
        glColor3f(*self.color)
        # plot a grid of line
        # make sure to scale based on window size
        glLineWidth(self.line_thickness)
        glBegin(GL_LINES)
        for i in range(-self.num_rows, self.num_rows + 1):
            glVertex2f(-self.num_cols, i / self.num_rows)
            glVertex2f(self.num_cols, i / self.num_rows)
        for i in range(-self.num_cols, self.num_cols + 1):
            glVertex2f(i / self.num_cols, -self.num_rows)
            glVertex2f(i / self.num_cols, self.num_rows)
        glEnd()
    
    def plot_axis(self):
        glColor3f(*self.axis_color)
        glLineWidth(self.line_thickness)
        glBegin(GL_LINES)
        glVertex2f(-self.num_cols, 0)
        glVertex2f(self.num_cols, 0)
        glVertex2f(0, -self.num_rows)
        glVertex2f(0, self.num_rows)
        glEnd()
