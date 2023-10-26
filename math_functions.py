
import numpy as np
import time as time



def getSinWaveFn(frequency=1, amplitude=1, phase=0):
  def fn(x):
    return amplitude * np.sin( 2 * np.pi * frequency * x + phase)
  return fn
  