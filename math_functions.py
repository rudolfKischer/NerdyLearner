
import numpy as np
import time as time
import random as random



def getSinWaveFn(frequency=1, amplitude=1, phase=0):
  def fn(x):
    return amplitude * np.sin( 2 * np.pi * frequency * x + phase)
  return fn

def getLinearFn(m=1, b=0):
  def fn(x):
    return m * x + b
  return fn
  

def uniform_random_sample(fn, interval, n):
  # sample n random points from fn in range, range is a tuple (min, max)
  # return a list of (x, y) tuples
  points = []
  for i in range(n):
    x = random.uniform(*interval)
    points.append((x, fn(x)))
  return points
