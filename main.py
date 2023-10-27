
from display import Display
from plotter import PointPlot, FunctionPlotter
import data_gen
from math_functions import getSinWaveFn, getLinearFn, uniform_random_sample
from grid_visualizer import GridMeshVisualizer

if __name__ == "__main__":

    display = Display()
    pointPlot = PointPlot()
    sin_func = getSinWaveFn(frequency=1, amplitude=1, phase=0)
    functionPlot = FunctionPlotter(sin_func, (-1, 1), (-1, 1))

    # random sample split
    
    g1, g2 = data_gen.gridSampleSplit(sin_func, (-1, 1), (-1, 1), 1080).values()
    g1PointPlot = PointPlot(g1, color=(1.0, 1.0, 1.0), point_size=0.001, line_width=1, connect=False)
    g2PointPlot = PointPlot(g2, color=(1.0, 1.0, 1.0), point_size=0.001, line_width=1, connect=False)


    # grid mesh
    gridMesh = GridMeshVisualizer((-1.0, 1.0), (-1.0, 1.0), 0.1, 0.1)
    for point in g1:
        gridMesh.insert(point, True)
    for point in g2:
        gridMesh.insert(point, False)
    display.add_draw_func(gridMesh.draw)
    del g1, g2
    

    display.add_draw_func(functionPlot.draw)
    display.add_draw_func(pointPlot.draw)

    #uniform random sample
    # points = uniform_random_sample(sin_func, (-1, 1), 100)
    # samplePointPlot = PointPlot(points, color=(0.0, 1.0, 0.0), point_size=0.01, line_width=1, connect=False)
    # display.add_draw_func(samplePointPlot.draw)

    # display.add_draw_func(g1PointPlot.draw)
    # display.add_draw_func(g2PointPlot.draw)

    display.add_mouse_callback(pointPlot.mouse_callback)
    display.render()