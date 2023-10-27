import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import display_text
import numpy as np
from quad_tree import BoundaryQuadTree
from display_primitives import draw_line, draw_quad, draw_quad_frame
from display_text import TextBitmap

class GridVisualizer():
    def __init__(self, x_range=(-10, 10), 
                 y_range=(-10, 10), 
                 x_step=None, 
                 y_step=None, 
                 color=(0.3, 0.3, 0.4)):
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

class GridMeshVisualizer():
    # Divides a range into a grid of cells, and draws a mesh over the grid
    # each cell is a square that can have its own color
    # we also want to allow subdivision of cells in some fashion so we can draw a finer mesh


    #TODO: make sure to scale and translate mesh based on window, needs to have range set to
    # window range right now
    def __init__(self,
                 x_range=(-10, 10), 
                 y_range=(-10, 10), 
                 x_step=None, y_step=None, 
                 color=(0.3, 0.3, 0.4)):
        self.color = color
        self.axis_color = (1.0, 1.0, 1.0)
        self.x_range, self.y_range = x_range, y_range
        self.x_step = x_step or self.default_step(self.x_range)
        self.y_step = y_step or self.default_step(self.y_range)

        self.width = self.x_range[1] - self.x_range[0]
        self.height = self.y_range[1] - self.y_range[0]
        self.position = (self.x_range[0], self.y_range[0])

        self.quad_tree = BoundaryQuadTree(self.position, (self.width, self.height))

    def insert(self, point, value):
        self.quad_tree.insert(point, value)  

    def draw_quad_node_outline(self, quad):
        # draw outline
        if quad.children[0] is None:
            draw_quad_frame(quad.position, quad.dimension, (0, 0, 0), width=4)
        
        for child in quad.children:
            if child is not None:
                self.draw_quad_node_outline(child)
    
    def draw_index(self, quad):
        # draw index
        if quad.children[0] is None:
            x, y = quad.position
            w, h = quad.dimension
            text = TextBitmap(f'{quad.index}', text_color = (0, 0, 0,255))
            text.draw(x, y, scale=(0.1, 0.1))
        for child in quad.children:
            if child is not None:
                self.draw_index(child)
        
     
    def draw_quad_node(self, quad):
        # if the quad has no children, draw it
        # if the quads data_value is not none, draw it
        # if the data value is True, draw red, if it is false, draw blue
        red = (1.0, 0.0, 0.0)
        blue = (0.0, 0.0, 1.0)
        white = (1.0, 1.0, 1.0)
        class_color_map = {
            True: red,
            False: blue,
            None: white
        }

        if quad.children[0] is None:
            draw_quad(quad.position, quad.dimension, class_color_map[quad.data_value])
            return
        
        for child in quad.children:
            self.draw_quad_node(child)
        
    def draw(self):
        self.draw_quad_node(self.quad_tree)
        # self.draw_quad_node_outline(self.quad_tree)
        # self.draw_index(self.quad_tree)
