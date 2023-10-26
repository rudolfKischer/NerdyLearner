import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import display_text
import numpy as np

class GridVisualizer():
    default_x_range = (-10, 10.0)
    default_y_range = (-10.0, 10.0)
    
    def __init__(self, 
                  x_range=None, 
                  y_range=None,
                  x_step_size=None,
                  y_step_size=None,
                  color = (0.3, 0.3, 0.4)):
        self.color = color
        self.axis_color = (1.0, 1.0, 1.0)
        self.line_thickness = 1
        self.x_range = x_range if x_range is not None else self.default_x_range
        self.y_range = y_range if y_range is not None else self.default_y_range
        self.relative_origin_x, self.relative_origin_y = self.relative_origin()

        self.x_step_size = x_step_size
        self.y_step_size = y_step_size
        if self.x_step_size is None:
            self.x_step_size = (self.x_range[1] - self.x_range[0]) / 10
        if self.y_step_size is None:
            self.y_step_size = (self.y_range[1] - self.y_range[0]) / 10
    

    def relative_origin(self):
        # compute where the origion will be relative to the ranges for x and y
        relative_origin_x = -(self.x_range[0] + self.x_range[1]) / (self.x_range[1] - self.x_range[0])
        relative_origin_y = -(self.y_range[0] + self.y_range[1]) / (self.y_range[1] - self.y_range[0])
        return relative_origin_x, relative_origin_y

    def draw_label(self, value, position, is_x_axis):
        text_size = 0.03
        text_tex = display_text.TextBitmap(f'{value:.2f}')
        x, y = (position, self.relative_origin_y) if is_x_axis else (self.relative_origin_x, position)
        # clamp x and y to be within the window
        x = max(-1.0, min(0.93, x))
        y = max(-1.0, min(0.95, y))
        text_tex.draw(x, y, scale=(text_size, text_size))
    
    def draw_grid_line(self, position, is_x_axis):
        glLineWidth(self.line_thickness)
        glBegin(GL_LINES)

        if is_x_axis:
            glVertex2f(position, -1.0)
            glVertex2f(position, 1.0)
        else:
            glVertex2f(-1.0, position)
            glVertex2f(1.0, position)
        glEnd()
        pass
    
    def compute_values(self, value_range, step_size):
        start_value = value_range[0] + step_size - (value_range[0] % step_size)
        num = start_value - step_size
        while num < value_range[1] + step_size:
            normalized_pos = (num - value_range[0]) / (value_range[1] - value_range[0])
            position = 2*normalized_pos - 1
            yield num, position
            num += step_size
    
    def origin_tolerance(self, is_x_axis):
        if is_x_axis:
            return self.x_step_size / 100
        else:
            return self.y_step_size / 100
    
        

    def draw_labeled_gridlines(self, val, pos, is_x_axis):
        is_origin = abs(val) < self.origin_tolerance(is_x_axis)
        if is_origin:
            glColor3f(*self.axis_color)
            glLineWidth(3)
        else:
            glColor3f(*self.color)
            glLineWidth(self.line_thickness)
        
        self.draw_grid_line(pos, is_x_axis)

        if is_origin and not is_x_axis:
            return
            
        glColor3f(*self.axis_color)
        self.draw_label(val, pos, is_x_axis)

                
    def draw(self):
        for val, pos in self.compute_values(self.x_range, self.x_step_size):
            self.draw_labeled_gridlines(val, pos, True)
        for val, pos in self.compute_values(self.y_range, self.y_step_size):
            self.draw_labeled_gridlines(val, pos, False)