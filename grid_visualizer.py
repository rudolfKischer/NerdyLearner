import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import display_text
import numpy as np

class GridVisualizer():
    def __init__(self, x_range=(-10, 10), y_range=(-10, 10), x_step=None, y_step=None, color=(0.3, 0.3, 0.4)):
        self.color = color
        self.axis_color = (1.0, 1.0, 1.0)
        self.x_range, self.y_range = x_range, y_range
        self.x_step = x_step or self.default_step(self.x_range)
        self.y_step = y_step or self.default_step(self.y_range)

    @staticmethod
    def default_step(rng):
        return (rng[1] - rng[0]) / 10

    @staticmethod
    def rel_pos(val, rng):
        return 2 * (val - rng[0]) / (rng[1] - rng[0]) - 1

    def draw_text(self, val, is_x_axis):
        if is_x_axis:
            x_pos = self.rel_pos(val, self.x_range)
            y_pos = self.rel_pos(0, self.y_range)
        else:
            x_pos = self.rel_pos(0, self.x_range)
            y_pos = self.rel_pos(val, self.y_range)
        
        display_text.TextBitmap(f'{val:.2f}').draw(x_pos, y_pos, scale=(0.03, 0.03))
    
    def draw_line(self, start, end, is_origin):
        glColor3f(*(self.axis_color if is_origin else self.color))
        glLineWidth(3 if is_origin else 1)
        glBegin(GL_LINES)
        glVertex2f(*start)
        glVertex2f(*end)
        glEnd()

    def grid_values(self, rng, step):
        num = rng[0] + step - (rng[0] % step)
        while num < rng[1] + step:
            yield num
            num += step

    def draw_gridlines(self, val, axis_step, is_x_axis):
        pos = self.rel_pos(val, self.x_range) if is_x_axis else self.rel_pos(val, self.y_range)
        is_origin = abs(val) < axis_step / 100
        line_coords = [(pos, -1), (pos, 1)] if is_x_axis else [(-1, pos), (1, pos)]
        self.draw_line(*line_coords, is_origin)
        self.draw_text(val, is_x_axis)
                
    def draw(self):
        for val in self.grid_values(self.x_range, self.x_step):
            self.draw_gridlines(val, self.x_step, True)
        for val in self.grid_values(self.y_range, self.y_step):
            self.draw_gridlines(val, self.y_step, False)

