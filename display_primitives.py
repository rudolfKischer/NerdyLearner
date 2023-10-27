from OpenGL.GL import *
from OpenGL.GLU import *

def draw_point(point, color=(1.0, 0.0, 0.0), size=5):
    glColor3f(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(*point)
    glEnd()

def draw_pointRound(point, color=(1.0, 0.0, 0.0), size=0.01):
    # draw a point as a circle
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(point[0], point[1], 0)
    gluSphere(gluNewQuadric(), size, 15, 15)
    glPopMatrix()


def draw_line(start, end, color=(1.0, 0.0, 0.0), width=1):
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(*start)
    glVertex2f(*end)
    glEnd()

def draw_quad(position, dimension, color=(1.0, 0.0, 0.0), width=1):
    # quad should be filled in with color
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_QUADS)
    glVertex2f(*position)
    glVertex2f(position[0], position[1] + dimension[1])
    glVertex2f(position[0] + dimension[0], position[1] + dimension[1])
    glVertex2f(position[0] + dimension[0], position[1])
    glEnd()

def draw_quad_frame(position, dimension, color=(1.0, 0.0, 0.0), width=1):
    # quad should be filled in with color
    glColor3f(*color)
    glLineWidth(width)
    glBegin(GL_LINE_LOOP)
    glVertex2f(*position)
    glVertex2f(position[0], position[1] + dimension[1])
    glVertex2f(position[0] + dimension[0], position[1] + dimension[1])
    glVertex2f(position[0] + dimension[0], position[1])
    glEnd()
