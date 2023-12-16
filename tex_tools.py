from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np



def generate_white_noise(width, height):
    return np.random.rand(width, height, 3).astype(np.float32)



def get_texture(texture_array):
    width = texture_array.shape[0]
    height = texture_array.shape[1]
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_FLOAT, texture_array)
    return texture_id

def draw_noise_texture():
    width, height = 200, 200

    # texture coords
    tr = 1.0, 1.0
    br = 1.0, -1.0
    bl = -1.0, -1.0
    tl = -1.0, 1.0

    vtx_coords = np.array([bl, tl, tr, br], dtype=np.float32)
    vtx_coords *= 0.5
    noise_array = generate_white_noise(width, height)
    draw_texture(noise_array, vtx_coords)


def draw_texture(tex_array, vtx_coords):
    texture_id = get_texture(tex_array)
    tex_coords = np.array([(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1, 0.0)], dtype=np.float32)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_2D)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    for vtx, tex in zip(vtx_coords, tex_coords):
        glTexCoord2f(*tex)
        glVertex2f(*vtx)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    