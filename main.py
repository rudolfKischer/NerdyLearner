
from display import Display
from plotter import PointPlot, FunctionPlotter
import data_gen
from math_functions import getSinWaveFn, getLinearFn, uniform_random_sample
from grid_visualizer import GridMeshVisualizer
from gui_elements import Slider, GuiElement, QuadGuiElement
import random
from tex_tools import draw_texture
import numpy as np
from functools import lru_cache

if __name__ == "__main__":

    display = Display()
    pointPlot = PointPlot()
    sin_func_1 = getSinWaveFn(frequency=0.6, amplitude=0.1, phase=0, velocity=0.4)
    sin_func_2 = getSinWaveFn(frequency=0.4, amplitude=0.25, phase=0, velocity=0.3)
    sin_func_3 = getSinWaveFn(frequency=0.7, amplitude=0.2, phase=0, velocity=0.1)
    

    def circleClassifier(point, pos=(0.0, 0.0), radius=1.0):
        # checks if a given point is inside a circle
        return (point[0] - pos[0])**2 + (point[1] - pos[1])**2 < radius**2
    
    def getRandomCricles(n, radius_range=(0.05, 0.5), pos_range=(-1.0, 1.0)):
        # returns a list of positions and radii for n circles
        positions = [(random.uniform(*pos_range), random.uniform(*pos_range)) for _ in range(n)]
        # random radii using rand
        radii = [random.uniform(*radius_range) for _ in range(n)]
        return [(pos, radius) for pos, radius in zip(positions, radii)]
    
    random_circles = getRandomCricles(10)

    def circlesClassifier(point):
        circles = random_circles
        # checks if a given point is inside any of the circles
        for pos, radius in circles:
            if circleClassifier(point, pos, radius):
                return True
        return False

    slider = Slider()


    def sin_func(x):
        return (sin_func_1(x) + sin_func_2(x) + sin_func_3(x)) * slider.value
    lin_func = getLinearFn(-2, 1)
    functionPlot = FunctionPlotter(sin_func, (-1, 1), (-1, 1))

    
    def gridMeshCallback():
        g1, g2 = data_gen.gridSampleSplit(sin_func, (-1, 1), (-1, 1), 580).values()
        gridMesh = GridMeshVisualizer((-1.0, 1.0), (-1.0, 1.0), 0.1, 0.1)

        for point in g1:
            gridMesh.insert(point, True)
        for point in g2:
            gridMesh.insert(point, False)
        gridMesh.draw()

    maroon = (0.502, 0.122, 0.192)
    seafoam = (0.09, 0.639, 0.427)  
    
    def drawClassifier(resolution=(100, 100)):
        
        #resolution
        width, height = 150, 150
        classifications = np.zeros((width, height, 3), dtype=np.float32)
        #texture coords
        tex_coords = np.array([(-1.0, -1.0), (-1.0, 1.0), (1.0, 1.0), (1, -1.0)], dtype=np.float32)

        tex_width = tex_coords[2][0] - tex_coords[0][0]
        tex_height = tex_coords[1][1] - tex_coords[0][1]

        color_1 = seafoam
        color_2 = maroon

        # use the position in the array relative to  the texture coords to get the coordinates
        for x in range(width):
            x_coord = x / width
            x_pos = tex_coords[0][0] + x_coord * tex_width
            threshold_val = sin_func(x_pos)
            for y in range(height):

                y_coord = y / height
                y_pos = tex_coords[0][1] + y_coord * tex_height
                # make position relative to the texture coords
                classifications[y][x] = color_1 if y_pos < threshold_val else color_2
        
        draw_texture(classifications, tex_coords)


    

    display.add_draw_func(drawClassifier)
    # display.add_draw_func(gridMeshCallback)
    

    # display.add_draw_func(functionPlot.draw)

    display.add_draw_func(slider.draw)
    display.add_callback(slider.mouse_callback, "mouse")
    display.add_callback(slider.mouse_move_callback, "mouse_move")
    # display.add_draw_func(pointPlot.draw)

    # add noise texture



    # test quad
    # quad = QuadGuiElement()
    # quad.colors = [(0.0, 1.0, 0.0)]
    # display.add_draw_func(quad.draw)
    # quad.scale = (0.5, 0.5)
    # quad.translation = (0.5, 0.2)




    #uniform random sample
    # points = uniform_random_sample(sin_func, (-1, 1), 100)
    # samplePointPlot = PointPlot(points, color=(0.0, 1.0, 0.0), point_size=0.01, line_width=1, connect=False)
    # display.add_draw_func(samplePointPlot.draw)

    # display.add_draw_func(g1PointPlot.draw)
    # display.add_draw_func(g2PointPlot.draw)

    # display.add_mouse_callback(pointPlot.mouse_callback, "mouse")
    display.render()