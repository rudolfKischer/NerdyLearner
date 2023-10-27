
count = 0
quad_count = 0
class QuadTreeNode:

  def __init__(self, position, dimension):
    global quad_count

    self.position = position
    self.dimension = dimension
    self.children = [None, None, None, None]
    self.data_value = None
    self.data = None
    self.index = quad_count
    quad_count += 1
  
  def subdivide(self):
    global quad_count
    x, y = self.position
    w, h = self.dimension
    new_dim = (w/2, h/2)
    self.children[0] = self.__class__((x , y), new_dim)
    self.children[1] = self.__class__((x + w/2, y), new_dim)
    self.children[2] = self.__class__((x + w/2, y + h/2), new_dim)
    self.children[3] = self.__class__((x, y + h/2), new_dim)
  
class BoundaryQuadTree(QuadTreeNode):
    # we want to insert values at specific points
    # if we go to insert a value at a point that already has a value which is not the same, we need to subdivide
    # When we subdivide, we need to move the old value to the appropriate child node


  def inBounds(self, point):
    x, y = point
    x0, y0 = self.position
    w, h = self.dimension
    return x0 < x and x <= x0 + w and y0 < y and y <= y0 + h


  def insert(self, point, value):
      
    # if the point doesnt belong return false
    if not self.inBounds(point):

      return False
    
    if self.children[0]:
      for child in self.children:
        if child.insert(point, value):
          return True
      return False
    
    # if the point belongs, and there is no data, set data and return true
    if self.data is None:
      self.data_value = value
      self.data = [(point, value)]
      return True
    
    # if the point belongs, and there is data, and the data is the same, append and return true
    if self.data_value == value:
      self.data.append((point, value))
      return True
    
    # if the point belongs, and there is data, and the data is not the same, subdivide and return self.insert(point, value)
    if self.children[0] is None:
      d_temp = self.data.copy()
      self.data.clear()
      self.subdivide()
      for child in self.children:
        child.data_value = self.data_value
      for d_point, d_value in d_temp:
        self.insert(d_point, d_value)
      return self.insert(point, value)
    
    return False
