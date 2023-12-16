import glfw
from OpenGL.GL import *
from OpenGL.GLU import *




class NerdyWindow:
    
    default_params = {
        "width": 800,
        "height": 600,
        "title": "y = mx + b Plot",
        "color": (0.0, 0.0, 0.0, 1.0),
        "window_coordinates": (-1, 1, -1, 1)
        
    }
    
    def __init__(self, **kwargs):
        for key, value in self.default_params.items():
            setattr(self, key, value)

        for key, value in kwargs.items():
            if key not in self.default_params:
                raise Exception(f"Invalid parameter: {key}")
            setattr(self, key, value)
        
        self.setup()

    def setup(self):
        if not glfw.init():
            raise Exception("GLFW initialization failed!")

        self.glfw_window = glfw.create_window(
            self.width, self.height, self.title, None, None
        )
        if not self.glfw_window:
            glfw.terminate()
            raise Exception("GLFW window creation failed!")

        glfw.make_context_current(self.glfw_window)
        glClearColor(*self.color)
        gluOrtho2D(*self.window_coordinates)
    
    def get(self):
        return self.glfw_window

class InputWindow(NerdyWindow):
    
    def __init__(self, **kwargs):
            super().__init__(**kwargs)
    
    def setup(self):
        super().setup()
        self.listeners = {
            "mouse": [],
            "mouse_move": [],
            "key": []
        }
        glfw.set_mouse_button_callback(self.glfw_window, self.mouse_callback)
        glfw.set_cursor_pos_callback(self.glfw_window, self.mouse_move_callback)
        glfw.set_key_callback(self.glfw_window, self.key_callback)
    
    def add_listener(self, listener, event_type):
        if event_type not in self.listeners:
            raise Exception(f"Invalid event type: {event_type}")
        self.listeners[event_type].append(listener)


    def key_callback(self, window, key, scancode, action, mods):
        for listener in self.listeners["key"]:
            listener(key, scancode, action, mods)
    
    def mouse_callback(self, window, button, action, mods):
        for listener in self.listeners["mouse"]:
            listener(window, button, action, mods)
    
    def mouse_move_callback(self, window, x, y):
        for listener in self.listeners["mouse_move"]:
            listener(window, x, y)

class Display:
    
    def __init__(self, window = None):
        self.window = window
        if window is None:
            self.window = InputWindow()
            self.glfw_window = self.window.get()
        self.draw_funcs = []
        
    
    def update(self):
        glClear(GL_COLOR_BUFFER_BIT)
        for func in self.draw_funcs:
            func()
        glfw.swap_buffers(self.glfw_window)
    
    def add_callback(self, callback, event_type):
        """
        event_type: "key", "mouse", "mouse_move"
        """
        self.window.add_listener(callback, event_type)
    
    def add_draw_func(self, func):
        self.draw_funcs.append(func)

    
    def render(self):
        while not glfw.window_should_close(self.glfw_window):
            glfw.poll_events()
            self.update()
        glfw.terminate()