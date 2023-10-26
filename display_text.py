import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

FONT_PATH = "/Users/rudolfkischer/Projects/NerdyLearner/arial.ttf"

class TextBitmap:
    
    default_params = {
        "bitmap_size": 120,
        "text_color": (255, 255, 255, 255),
        "text_bg_color": (0, 0, 0, 0),

    }

    def __init__(self, text, **kwargs):
        self.text = text
        self.texture_id = None
        for key, value in self.default_params.items():
            setattr(self, key, value)
        for key, value in kwargs.items():
            if key not in self.default_params:
                raise Exception(f"Invalid parameter: {key}")
            setattr(self, key, value)
    

    def create_text_img(self):
        font = ImageFont.truetype(FONT_PATH, self.bitmap_size)

        self.text_width, self.text_height = font.getsize(self.text)

        img = Image.new('RGBA', (self.text_width, self.text_height), self.text_bg_color)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), self.text, font=font, fill=self.text_color)

        return img
    
    def create_text_texture(self):
        image = self.create_text_img()
        image_data = np.array(image.convert("RGBA"), np.uint8)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        return texture_id
        
    def draw(self, x, y, scale = (1.0, 1.0)):
        if self.texture_id is None:
            self.texture_id = self.create_text_texture()

        # enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glPushMatrix()
        glTranslatef(x, y, 0)

        bottom_left = (0, 0)
        top_right = (self.text_width, self.text_height)
        # normalize so that the hieght always equals 1
        # scale x accordingly
        normal_factor = 1.0 / self.text_height
        scale_x = normal_factor * scale[0]
        scale_y = normal_factor * scale[1]
        glScalef(scale_x, scale_y, 1.0)
        

        # get glfw aspect ratio
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1); glVertex2f(*bottom_left)
        glTexCoord2f(1, 1); glVertex2f(top_right[0], bottom_left[1])
        glTexCoord2f(1, 0); glVertex2f(*top_right)
        glTexCoord2f(0, 0); glVertex2f(bottom_left[0], top_right[1])
        glEnd()
        glPopMatrix()

        glDisable(GL_TEXTURE_2D)

        # disable blending
        glDisable(GL_BLEND)

    
        