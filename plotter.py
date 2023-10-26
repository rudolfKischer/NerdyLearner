import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from grid_visualizer import GridVisualizer

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
        glColor3f(1.0, 1.0, 1.0)
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

class FunctionPlotter():
    
    def __init__(self, fn, x_range=None, y_range=None, segments=100, color=(1.0, 0.0, 0.0)):
        self.fn = fn
        self.x_range = x_range
        self.y_range = y_range
        if self.x_range is None:
            self.x_range = (-10, 10)
        if self.y_range is None:
            self.y_range = (-10, 10)
        self.segments = segments
        self.color = color
        self.grid = GridVisualizer(x_range, y_range)

    def plot_fn(self, fn, x_range, y_range):
        glColor3f(*self.color)
        glBegin(GL_LINE_STRIP)
        for seg in range(self.segments):
            x = x_range[0] + seg * (x_range[1] - x_range[0]) / self.segments
            y = fn(x)
            normalized_x = (x - x_range[0]) / (x_range[1] - x_range[0])
            normalized_y = (y - y_range[0]) / (y_range[1] - y_range[0])
            glVertex2f(2*normalized_x - 1, 2*normalized_y - 1)
        glEnd()
    
    def draw(self):
        self.grid.draw()
        self.plot_fn(self.fn, self.x_range, self.y_range)
    

    


        

