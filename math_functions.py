
import numpy as np
import time as time
import random as random



def getSinWaveFn(frequency=1, amplitude=1, phase=0, velocity=0):
  def fn(x):
    # make the phase a function of time
    phase = time.time() * 2 * np.pi * velocity
    return amplitude * np.sin( 2 * np.pi * frequency * x + phase)
  return fn

def getLinearFn(m=1, b=0):
  def fn(x):
    return m * x + b
  return fn

def get_corners(position, dimension):
    return [
      (position[0], position[1]),
      (position[0] + dimension[0], position[1]),
      (position[0] + dimension[0], position[1] + dimension[1]),
      (position[0], position[1] + dimension[1])
    ]
  

def uniform_random_sample(fn, interval, n):
  # sample n random points from fn in range, range is a tuple (min, max)
  # return a list of (x, y) tuples
  points = []
  for i in range(n):
    x = random.uniform(*interval)
    points.append((x, fn(x)))
  return points
