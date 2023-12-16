import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from display_primitives import draw_quad, draw_quad_p
from display_text import TextBitmap
from math_functions import get_corners
import numpy as np

class GuiElement():
  gui_default_params = {
      "translation": [0, 0],
      "scale": [1, 1],
      "colors": [(1, 0, 1)]
  }
  
  def __init__(self, **kwargs):
    self.parent = None
    self.children = []

    params = {**self.gui_default_params, **kwargs}
    for key, value in params.items():
        setattr(self, key, value)
  
  def get_ancestor_scale(self):
    if self.parent is None:
      return np.array(self.scale)
    else:
      return self.parent.get_ancestor_scale() * np.array(self.scale)
  
  def get_ancestor_translation(self):
    if self.parent is None:
      return np.array(self.translation)
    else:
      return self.parent.get_ancestor_translation() + np.array(self.translation) * self.parent.get_ancestor_scale()

  def add_child(self, child):
    self.children.append(child)
    child.parent = self
  
  def draw(self):
    pass

class TextGuiElement(GuiElement):
  def __init__(self, **kwargs):
    self.text = kwargs["text"]
    kwargs.pop("text")
    super().__init__(**kwargs)
  
  def draw(self):
    color = self.colors[0]
    # int cast color
    color = tuple([int(c*255) for c in color])
    # if no ALPHA channel, add it
    if len(color) == 3:
      color = color + (255,)
    text_bitmap = TextBitmap(self.text, text_color=color)
    text_bitmap.draw(*self.get_ancestor_translation(), scale=self.get_ancestor_scale())
    
class QuadGuiElement(GuiElement):
   
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.setup()
    
  def setup(self):
    self.model_points = [
      [-1, -1],
      [-1, 1],
      [1, 1],
      [1, -1]
    ]
    print("model points: ", self.model_points)

  def get_points(self):
    points = []
    for point in self.model_points:
      point = np.array(point)
      point = point * self.get_ancestor_scale()
      point = point + self.get_ancestor_translation()
      points.append(point)
    return points
  
  def draw(self):
    points = self.get_points()
    draw_quad_p(points, color=self.colors[0])
  

  
  



    

class Slider(QuadGuiElement):

  slider_default_params = {
    "label": "Slider",
    "min_val": 0,
    "max_val": 1,
    "value": 0.5,
    "scale": [0.5, 0.05],
    "colors": [(0.5, 0.5, 0.5)],
    "translation": [-0.5, 0.9]
  }

  def __init__(self, **kwargs):
    combined_params = {**self.slider_default_params, **kwargs}
    super().__init__(**combined_params)

    self.slider_setup()
  
  def setup_tab(self):
    self.tab = QuadGuiElement()
    self.tab.colors = [(0.8, 0.8, 0.8)]
    self.tab_width = 0.1
    self.tab_height = 0.8
    self.tab.scale = [self.tab_width, self.tab_height]

    self.add_child(self.tab)
    self.update_tab_position()
  
  def setup_bar(self):
    self.bar = QuadGuiElement()
    self.bar.colors = [(0.1, 0.1, 0.1)]
    self.bar.scale = [0.8, 0.1]
    self.add_child(self.bar)
  
  def setup_labels(self):
    label_color = (0.0, 0.0, 0.0)
    label_scale = [0.07, 0.7]

    self.min_label = TextGuiElement(text=f'{self.min_val:.2f}', colors=[label_color])
    self.min_label.translation = [-1.0, -0.5]
    self.min_label.scale = label_scale
    self.add_child(self.min_label)


    self.max_label = TextGuiElement(text=f'{self.max_val:.2f}', colors=[label_color])
    self.max_label.translation = [0.8, -0.5]
    self.max_label.scale = label_scale
    self.add_child(self.max_label)

    self.value_label = TextGuiElement(text=f'{self.value:.2f}', colors=[label_color])
    self.value_label.translation = [0.0, -1.0]
    self.value_label.scale = label_scale
    self.add_child(self.value_label)


  def slider_setup(self):
    self.value = self.min_val + self.value * (self.max_val - self.min_val)
    self.is_dragging = False
    self.setup_tab()
    self.setup_bar()
    self.setup_labels()

  
  def update_tab_position(self):
    # tab position is relative to the value, which is between min_val and max_val
    # normalize the value, then see how far the normalized value is from 0.5
    # move the tab by that amount * the scale of ancestors
    slider_start_pos = self.translation[0] - self.get_ancestor_scale()[0]
    slider_end_pos = self.translation[0] + self.get_ancestor_scale()[0]
    normalized_val = (self.value - self.min_val) / (self.max_val - self.min_val)
    normalized_val = normalized_val * 2 - 1
    tab_x_position = normalized_val * (slider_end_pos - slider_start_pos)
    self.tab.translation = [tab_x_position, 0.0]
  
  def draw_labels(self):
    self.value_label.text = f'{self.value:.2f}'
    self.value_label.translation = [self.tab.translation[0] - self.tab_width * 0.5, 0.0]
    self.value_label.draw()
    self.min_label.draw()
    self.max_label.draw()

  def draw(self):
    # draw 
    self.update_tab_position()
    super().draw()
    self.bar.draw()
    self.tab.draw()
    self.draw_labels()

  
  def update_value(self, window):
      x, y = glfw.get_cursor_pos(window)
      window_size = glfw.get_window_size(window)
      x = x / window_size[0] * 2 - 1
      y = y / window_size[1] * 2 - 1

      slider_start_pos = self.translation[0] - self.get_ancestor_scale()[0]
      slider_end_pos = self.translation[0] + self.get_ancestor_scale()[0]
      normalized_h_position = (x - slider_start_pos) / (slider_end_pos - slider_start_pos)
      self.value = self.min_val + normalized_h_position * (self.max_val - self.min_val)
      self.value = min(self.value, self.max_val)
      self.value = max(self.value, self.min_val)

  def mouse_move_callback(self, window, xpos, ypos):
      if self.is_dragging:
          self.update_value(window)

  def mouse_callback(self, window, button, action, mods):
      if button == glfw.MOUSE_BUTTON_LEFT:
          if action == glfw.PRESS:
              self.is_dragging = True
              self.update_value(window)
          elif action == glfw.RELEASE:
              self.is_dragging = False






    

