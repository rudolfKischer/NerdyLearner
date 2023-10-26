import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from grid_visualizer import GridVisualizer
import numpy as np
from display_primitives import draw_point, draw_line, draw_pointRound

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

    def __init__(self, 
                 points = None, 
                 color=(1.0, 0.0, 0.0), 
                 point_size=0.02,
                 line_width=1,
                 show_points=True, 
                 connect=True):
        self.points = points
        if self.points is None:
            self.points = []
        self.color = color
        self.point_size = point_size
        self.connect = connect
        self.line_width = line_width
        self.show_points = show_points
    
    def add_point(self, x, y):
        self.points.append((x, y))
    
    def clear_points(self):
        self.points = []
    
    def set_points(self, points):
        self.clear_points()
        for point in points:
            self.add_point(*point)
    
    def draw(self):
        if self.show_points:
            for point in self.points:
                draw_pointRound(point, self.color, self.point_size)
        
        if self.connect:
            for i in range(len(self.points) - 1):
                    draw_line(self.points[i], self.points[i+1], self.color, self.line_width)


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
        self.pointPlot = PointPlot([], color=self.color, point_size=0.01, line_width=1, connect=True, show_points=True)

    
    def compute_slope_changes(self, x_points, y_values):
        slopes = np.diff(y_values) / np.diff(x_points)
        return np.abs(np.diff(slopes))

    def identify_indices(self, slope_changes):
        # Sort segments based on slope changes
        sorted_indices = np.argsort(slope_changes)
        
        # Half of the segments to modify will be from the smallest slope changes
        remove_indices = sorted_indices[:self.segments//20]  # example: 5% of total segments
        
        # The other half will be from the largest slope changes
        add_indices = sorted_indices[-self.segments//20:]
        
        return add_indices, remove_indices

    def reallocate_points(self, x_points, add_indices, remove_indices):
        for index in add_indices:
            x_mid = 0.5 * (x_points[index] + x_points[index + 1])
            x_points = np.insert(x_points, index + 1, x_mid)
        
        for index in reversed(remove_indices):
            x_points = np.delete(x_points, index + 1)

        return x_points

    def adapt_points(self, x_range):
        x_points = np.linspace(x_range[0], x_range[1], self.segments)
        y_values = np.array([self.fn(x) for x in x_points])
        
        slope_changes = self.compute_slope_changes(x_points, y_values)
        add_indices, remove_indices = self.identify_indices(slope_changes)
        
        return self.reallocate_points(x_points, add_indices, remove_indices)

    def get_seg_points(self, x_range):
        x_points = self.adapt_points(x_range)
        seg_points = [(x, self.fn(x)) for x in x_points]
        return seg_points

    def plot_fn(self):
        seg_points = self.get_seg_points(self.x_range)
        self.pointPlot.set_points(seg_points)
        self.pointPlot.draw()
    
    def draw(self):
        self.grid.draw()
        self.plot_fn()
    

    


        

