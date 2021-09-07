# Python Graphics Set by Ollie Robinson, 2021.
# Using a GPL-3.0 License. Feel free to use this
# in any project you like! Please remember to give credit
# in your project if you use it! (Preferably as a small note
# in your game.)

# This version is the in-development version of the PGS using
# an OpenGL renderer backend.
# Some PGS features may not be supported.

import OpenGL.GL as _gl
import glfw as _glfw
import abc as _abc

class Vector2:
    """Represents a 2-dimensional vector, with an x and y position."""
    @staticmethod
    def zero():
        return Vector2(0, 0)

    @staticmethod
    def one():
        return Vector2(1, 1)

    def __init__(self, x: float, y: float):
        #if (type(x) != float and type(x) != int):
        #    raise TypeError(f"Argument 'x' expected type 'float', got '{type(x).__name__}' instead.")
        #if (type(y) != float and type(y) != int):
        #    raise TypeError(f"Argument 'y' expected type 'float', got '{type(x).__name__}' instead.")
        self.x: float = x
        self.y: float = y

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other) -> 'Vector2':
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        elif type(other) == float or type(other) == int:
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError(f"unsupported operand type(s) for *: 'Vector2' and '{type(other).__name__}'")

    def __rmul__(self, other) -> 'Vector2':
        if (type(other) != Vector2 and type(other) != int and type(other) != float):
            raise TypeError(f"unsupported operand type(s) for *: '{type(other).__name__}' and 'Vector2'")
        else:
            return self * other

    def __truediv__(self, other) -> 'Vector2':
        if type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        elif type(other) == float or type(other) == int:
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError(f"unsupported operand type(s) for /: 'Vector2' and '{type(other).__name__}'")

    def __floordiv__(self, other) -> 'Vector2':
        vec: Vector2 = self / other
        vec.x //= 1
        vec.y //= 1
        return vec

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __str__(self):
        return f"Vector2(x: {self.x}, y: {self.y})"

    #@staticmethod
    #def lerp(value1: 'Vector2', value2: 'Vector2', amount: float) -> 'Vector2':
        #lerp_val = _mg.Vector2.Lerp(_mg.Vector2(float(value1.x), float(value1.y)), _mg.Vector2(float(value2.x), float(value2.y)), float(amount))
        #return Vector2(lerp_val.X, lerp_val.Y)

class Size:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

    def to_vector2(self) -> Vector2:
        return Vector2(self.width, self.height)

class Matrix:
    @staticmethod
    def identity():
        return Matrix(1, 0, 0, 0,
                      0, 1, 0, 0,
                      0, 0, 1, 0,
                      0, 0, 0, 1)

    def __init__(self, m11: float, m12: float, m13: float, m14: float, m21: float, m22: float, m23: float, m24: float,
                 m31: float, m32: float, m33: float, m34: float, m41: float, m42: float, m43: float, m44: float):
        self.m11: float = m11
        self.m12: float = m12
        self.m13: float = m13
        self.m14: float = m14
        self.m21: float = m21
        self.m22: float = m22
        self.m23: float = m23
        self.m24: float = m24
        self.m31: float = m31
        self.m32: float = m32
        self.m33: float = m33
        self.m34: float = m34
        self.m41: float = m41
        self.m42: float = m42
        self.m43: float = m43
        self.m44: float = m44

    @staticmethod
    def transform(value: Vector2) -> 'Matrix':
        #return Matrix._to_pgs_matrix(_mg.Matrix.CreateTranslation(float(value.x), float(value.y), float(0)))
        pass

    @staticmethod
    def rotate(value: float) -> 'Matrix':
        #return Matrix._to_pgs_matrix(_mg.Matrix.CreateRotationZ(value))
        pass

    @staticmethod
    def scale(value: Vector2) -> 'Matrix':
        #return Matrix._to_pgs_matrix(_mg.Matrix.CreateScale(_mg.Vector3(float(value.x), float(value.y), float(1))))
        pass

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        #return Matrix._to_pgs_matrix(_mg.Matrix.Multiply(self._to_mg_matrix(), other._to_mg_matrix()))
        pass


    #def _to_mg_matrix(self) -> _mg.Matrix:
        #return _mg.Matrix(float(self.m11), float(self.m12), float(self.m13), float(self.m14), float(self.m21),
        #                  float(self.m22), float(self.m23), float(self.m24), float(self.m31), float(self.m32),
        #                  float(self.m33), float(self.m34), float(self.m41), float(self.m42), float(self.m43),
        #                  float(self.m44))

    #@staticmethod
    #def _to_pgs_matrix(matrix: _mg.Matrix) -> 'Matrix':
    #    return Matrix(matrix.M11, matrix.M12, matrix.M13, matrix.M14, matrix.M21, matrix.M22, matrix.M23, matrix.M24,
    #                  matrix.M31, matrix.M32, matrix.M33, matrix.M34, matrix.M41, matrix.M42, matrix.M43, matrix.M44)


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r: int = r
        self.g: int = g
        self.b: int = b
        self.a: int = a

    @staticmethod
    def from_hex(hex_value: int):
        return Color(hex_value >> 16, (hex_value & 0xFF00) >> 8, hex_value & 255)


# From https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
# Colors enum. Defines a list of commonly used colors.
class Colors:
    ALICE_BLUE = Color.from_hex(0xF0F8FF)
    ANTIQUE_WHITE = Color.from_hex(0xFAEBD7)
    AQUA = Color.from_hex(0x00FFFF)
    AQUAMARINE = Color.from_hex(0x7FFFD4)
    AZURE = Color.from_hex(0xF0FFFF)
    BEIGE = Color.from_hex(0xF5F5DC)
    BISQUE = Color.from_hex(0xFFE4C4)
    BLACK = Color.from_hex(0x000000)
    BLANCHED_ALMOND = Color.from_hex(0xFFEBCD)
    BLUE = Color.from_hex(0x0000FF)
    BLUE_VIOLET = Color.from_hex(0x8A2BE2)
    BROWN = Color.from_hex(0xA52A2A)
    BURLY_WOOD = Color.from_hex(0xDEB887)
    CADET_BLUE = Color.from_hex(0x5F9EA0)
    CHARTREUSE = Color.from_hex(0x7FFF00)
    CHOCOLATE = Color.from_hex(0xD2691E)
    CORAL = Color.from_hex(0xFF7F50)
    CORNFLOWER_BLUE = Color.from_hex(0x6495ED)
    CORNSILK = Color.from_hex(0xFFF8DC)
    CRIMSON = Color.from_hex(0xDC143C)
    CYAN = Color.from_hex(0x00FFFF)
    DARK_BLUE = Color.from_hex(0x00008B)
    DARK_CYAN = Color.from_hex(0x008B8B)
    DARK_GOLDEN_ROD = Color.from_hex(0xB8860B)
    DARK_GRAY = Color.from_hex(0xA9A9A9)
    DARK_GREY = Color.from_hex(0xA9A9A9)
    DARK_GREEN = Color.from_hex(0x006400)
    DARK_KHAKI = Color.from_hex(0xBDB76B)
    DARK_MAGENTA = Color.from_hex(0x8B008B)
    DARK_OLIVE_GREEN = Color.from_hex(0x556B2F)
    DARK_ORANGE = Color.from_hex(0xFF8C00)
    DARK_ORCHID = Color.from_hex(0x9932CC)
    DARK_RED = Color.from_hex(0x8B0000)
    DARK_SALMON = Color.from_hex(0xE9967A)
    DARK_SEA_GREEN = Color.from_hex(0x8FBC8F)
    DARK_SLATE_BLUE = Color.from_hex(0x483D8B)
    DARK_SLATE_GRAY = Color.from_hex(0x2F4F4F)
    DARK_SLATE_GREY = Color.from_hex(0x2F4F4F)
    DARK_TURQUOISE = Color.from_hex(0x00CED1)
    DARK_VIOLET = Color.from_hex(0x9400D3)
    DEEP_PINK = Color.from_hex(0xFF1493)
    DEEP_SKY_BLUE = Color.from_hex(0x00BFFF)
    DIM_GRAY = Color.from_hex(0x696969)
    DIM_GREY = Color.from_hex(0x696969)
    DODGER_BLUE = Color.from_hex(0x1E90FF)
    FIRE_BRICK = Color.from_hex(0xB22222)
    FLORAL_WHITE = Color.from_hex(0xFFFAF0)
    FOREST_GREEN = Color.from_hex(0x228B22)
    FUCHSIA = Color.from_hex(0xFF00FF)
    GAINSBORO = Color.from_hex(0xDCDCDC)
    GHOST_WHITE = Color.from_hex(0xF8F8FF)
    GOLD = Color.from_hex(0xFFD700)
    GOLDEN_ROD = Color.from_hex(0xDAA520)
    GRAY = Color.from_hex(0x808080)
    GREY = Color.from_hex(0x808080)
    GREEN = Color.from_hex(0x008000)
    GREEN_YELLOW = Color.from_hex(0xADFF2F)
    HONEY_DEW = Color.from_hex(0xF0FFF0)
    HOT_PINK = Color.from_hex(0xFF69B4)
    INDIAN_RED = Color.from_hex(0xCD5C5C)
    INDIGO = Color.from_hex(0x4B0082)
    IVORY = Color.from_hex(0xFFFFF0)
    KHAKI = Color.from_hex(0xF0E68C)
    LAVENDER = Color.from_hex(0xE6E6FA)
    LAVENDER_BLUSH = Color.from_hex(0xFFF0F5)
    LAWN_GREEN = Color.from_hex(0x7CFC00)
    LEMON_CHIFFON = Color.from_hex(0xFFFACD)
    LIGHT_BLUE = Color.from_hex(0xADD8E6)
    LIGHT_CORAL = Color.from_hex(0xF08080)
    LIGHT_CYAN = Color.from_hex(0xE0FFFF)
    LIGHT_GOLDEN_ROD_YELLOW = Color.from_hex(0xFAFAD2)
    LIGHT_GRAY = Color.from_hex(0xD3D3D3)
    LIGHT_GREY = Color.from_hex(0xD3D3D3)
    LIGHT_GREEN = Color.from_hex(0x90EE90)
    LIGHT_PINK = Color.from_hex(0xFFB6C1)
    LIGHT_SALMON = Color.from_hex(0xFFA07A)
    LIGHT_SEA_GREEN = Color.from_hex(0x20B2AA)
    LIGHT_SKY_BLUE = Color.from_hex(0x87CEFA)
    LIGHT_SLATE_GRAY = Color.from_hex(0x778899)
    LIGHT_SLATE_GREY = Color.from_hex(0x778899)
    LIGHT_STEEL_BLUE = Color.from_hex(0xB0C4DE)
    LIGHT_YELLOW = Color.from_hex(0xFFFFE0)
    LIME = Color.from_hex(0x00FF00)
    LIME_GREEN = Color.from_hex(0x32CD32)
    LINEN = Color.from_hex(0xFAF0E6)
    MAGENTA = Color.from_hex(0xFF00FF)
    MAROON = Color.from_hex(0x800000)
    MEDIUM_AQUA_MARINE = Color.from_hex(0x66CDAA)
    MEDIUM_BLUE = Color.from_hex(0x0000CD)
    MEDIUM_ORCHID = Color.from_hex(0xBA55D3)
    MEDIUM_PURPLE = Color.from_hex(0x9370DB)
    MEDIUM_SEA_GREEN = Color.from_hex(0x3CB371)
    MEDIUM_SLATE_BLUE = Color.from_hex(0x7B68EE)
    MEDIUM_SPRING_GREEN = Color.from_hex(0x00FA9A)
    MEDIUM_TURQUOISE = Color.from_hex(0x48D1CC)
    MEDIUM_VIOLET_RED = Color.from_hex(0xC71585)
    MIDNIGHT_BLUE = Color.from_hex(0x191970)
    MINT_CREAM = Color.from_hex(0xF5FFFA)
    MISTY_ROSE = Color.from_hex(0xFFE4E1)
    MOCCASIN = Color.from_hex(0xFFE4B5)
    NAVAJO_WHITE = Color.from_hex(0xFFDEAD)
    NAVY = Color.from_hex(0x000080)
    OLD_LACE = Color.from_hex(0xFDF5E6)
    OLIVE = Color.from_hex(0x808000)
    OLIVE_DRAB = Color.from_hex(0x6B8E23)
    ORANGE = Color.from_hex(0xFFA500)
    ORANGE_RED = Color.from_hex(0xFF4500)
    ORCHID = Color.from_hex(0xDA70D6)
    PALE_GOLDEN_ROD = Color.from_hex(0xEEE8AA)
    PALE_GREEN = Color.from_hex(0x98FB98)
    PALE_TURQUOISE = Color.from_hex(0xAFEEEE)
    PALE_VIOLET_RED = Color.from_hex(0xDB7093)
    PAPAYA_WHIP = Color.from_hex(0xFFEFD5)
    PEACH_PUFF = Color.from_hex(0xFFDAB9)
    PERU = Color.from_hex(0xCD853F)
    PINK = Color.from_hex(0xFFC0CB)
    PLUM = Color.from_hex(0xDDA0DD)
    POWDER_BLUE = Color.from_hex(0xB0E0E6)
    PURPLE = Color.from_hex(0x800080)
    REBECCA_PURPLE = Color.from_hex(0x663399)
    RED = Color.from_hex(0xFF0000)
    ROSY_BROWN = Color.from_hex(0xBC8F8F)
    ROYAL_BLUE = Color.from_hex(0x4169E1)
    SADDLE_BROWN = Color.from_hex(0x8B4513)
    SALMON = Color.from_hex(0xFA8072)
    SANDY_BROWN = Color.from_hex(0xF4A460)
    SEA_GREEN = Color.from_hex(0x2E8B57)
    SEA_SHELL = Color.from_hex(0xFFF5EE)
    SIENNA = Color.from_hex(0xA0522D)
    SILVER = Color.from_hex(0xC0C0C0)
    SKY_BLUE = Color.from_hex(0x87CEEB)
    SLATE_BLUE = Color.from_hex(0x6A5ACD)
    SLATE_GRAY = Color.from_hex(0x708090)
    SLATE_GREY = Color.from_hex(0x708090)
    SNOW = Color.from_hex(0xFFFAFA)
    SPRING_GREEN = Color.from_hex(0x00FF7F)
    STEEL_BLUE = Color.from_hex(0x4682B4)
    TAN = Color.from_hex(0xD2B48C)
    TEAL = Color.from_hex(0x008080)
    THISTLE = Color.from_hex(0xD8BFD8)
    TOMATO = Color.from_hex(0xFF6347)
    TURQUOISE = Color.from_hex(0x40E0D0)
    VIOLET = Color.from_hex(0xEE82EE)
    WHEAT = Color.from_hex(0xF5DEB3)
    WHITE = Color.from_hex(0xFFFFFF)
    WHITE_SMOKE = Color.from_hex(0xF5F5F5)
    YELLOW = Color.from_hex(0xFFFF00)
    YELLOW_GREEN = Color.from_hex(0x9ACD32)
    TRANSPARENT = Color(0, 0, 0, 0)

class Disposable(_abc.ABC):
    """
    Represents a way to clean and remove unmanaged memory.
    """

    @_abc.abstractmethod
    def dispose(self):
        pass

class Texture:
    pass


class Shader(Disposable):
    """
    Create a custom GLSL shader that can be used.
    """

    def __init__(self, vertex: str, fragment: str):
        """
        Create a new shader.
        :param vertex: The vertex shader.
        :param fragment: The fragment shader.
        """
        vertex_shader = _gl.glCreateShader(_gl.GL_VERTEX_SHADER)
        _gl.glShaderSource(vertex_shader, 1, vertex, None)
        self.__compile_shader(vertex_shader)

        fragment_shader = _gl.glCreateShader(_gl.GL_FRAGMENT_SHADER)
        _gl.glShaderSource(fragment_shader, 1, fragment, None)
        self.__compile_shader(fragment_shader)

        self.__handle = _gl.glCreateProgram()
        _gl.glAttachShader(self.__handle, vertex_shader)
        _gl.glAttachShader(self.__handle, fragment_shader)
        self.__link_program(self.__handle)
        _gl.glDetachShader(self.__handle, vertex_shader)
        _gl.glDetachShader(self.__handle, fragment_shader)
        _gl.glDeleteShader(self.__handle, vertex_shader)
        _gl.glDeleteShader(self.__handle, fragment_shader)

        self.__uniform_locations = {}
        num_uniforms = None
        _gl.glGetProgramiv(self.__handle, _gl.GL_ACTIVE_UNIFORMS, num_uniforms)
        for i in range(num_uniforms):
            name = _gl.glGetActiveUniform(self.__handle, i, None)
            location = _gl.glGetUniformLocation(self.__handle, name[0])
            self.__uniform_locations[name] = location


    def __compile_shader(self, shader):
        _gl.glCompileShader(shader)

        status = None
        _gl.glGetShaderiv(shader, _gl.GL_COMPILE_STATUS, status)
        if status != 1:
            raise Exception(f"Error compiling shader '{shader}'.\n\n{_gl.glGetShaderInfoLog(shader, None)}")

    def __link_program(self, program):
        _gl.glLinkProgram(program)

        status = None
        _gl.glGetProgramiv(program, _gl.GL_LINK_STATUS, status)
        if status != 1:
            raise Exception(f"Error linking program '{program}'.\n\n{_gl.glGetProgramInfoLog(program, None)}")

    def set_uniform(self, uniform_name, value):
        name = self.__get_uniform_location(uniform_name)

        if type(value) == bool:
            _gl.glUniform1i(name, 1 if value == True else 0)
        elif type(value) == int:
            _gl.glUniform1i(name, value)
        elif type(value) == float:
            _gl.glUniform1f(name, value)
        elif type(value) == Vector2:
            _gl.glUniform2f(name, value.x, value.y)
        #elif type(value) == Matrix:
            #_gl.glUniformMatrix4fv(name, 1, True, )

    def __get_uniform_location(self, name):
        if name not in self.__uniform_locations:
            raise Exception("Given uniform name is not valid.")
        return self.__uniform_locations[name]

    def dispose(self):
        _gl.glDeleteProgram(self.__handle)


class SpriteBase:
    pass

class SpriteDrawer:
    # Primary sprite vertex shader
    __SPRITE_VERT = """
    #version 330 core
    
    in vec2 aPosition;
    in vec2 aTexCoords;
    
    out vec2 frag_texCoords;
    
    uniform mat4 uModel;
    uniform mat4 uTransform;
    uniform mat4 uProjection;
    
    void main()
    {
        gl_Position = vec4(aPosition, 0.0, 1.0) * uModel * uView * uProjection;
        frag_texCoords = aTexCoords;
    }"""

    # Primary sprite fragment shader
    __SPRITE_FRAG = """
    #version 330 core
    
    in vec2 frag_texCoords;
    
    out vec4 out_color;
    
    uniform sampler2D uTexture;
    uniform vec4 uColor;
    
    void main()
    {
        out_color = texture(uTexture, frag_texCoords) * uColor;
    }"""

    def __init__(self):
        pass

class DrawError:
    pass

class _GameBackend:
    def __init__(self, game, width: int, height: int, title: str, show_credits: bool, vsync: bool):
        self.game: Game = game
        self.width = width
        self.height = height
        self.title = title
        self.vsync = vsync

    def run(self, target_fps):
        if not _glfw.init():
            raise Exception("GLFW window could not be initialized! (Is there something wrong with your GLFW installation?)")

        self.window = _glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            _glfw.terminate()
            raise Exception("Window does not exist.")

        # Create an OpenGL context.
        _glfw.make_context_current(self.window)
        # We clear the window to black here, just in case a clear colour is not set.
        _gl.glClearColor(0.0, 0.0, 0.0, 1.0)

        self.game.initialize()

        # Game loop.
        while not _glfw.window_should_close(self.window):
            _gl.glClear(_gl.GL_COLOR_BUFFER_BIT)

            _glfw.swap_buffers(self.window)

            _glfw.poll_events()

        _glfw.terminate()


class Game:
    @property
    def clear_color(self) -> Color:
        return None

    @clear_color.setter
    def clear_color(self, value: Color):
        _gl.glClearColor(value.r / 255, value.g / 255, value.b / 255, value.a / 255)

    def __init__(self, width: int, height: int, title: str = "PGS Window", show_credits=True, vsync: bool = True):
        """
        Create a new instance of the Game class. This will in turn create a window, which will launch once 'run()' is called.
        :param width: The width, in pixels, of the game window.
        :param height: The height, in pixels, of the game window.
        :param title: The title, if any, of the game window.
        :param show_credits: Whether the PGS should show "Python Graphics Set" in the title, and the "Hello!" message on launch. Leave this set to 'True' if you want to show some support!
        """
        self.__game: _GameBackend = _GameBackend(self, width, height, title, show_credits, vsync)

    def initialize(self):
        pass

    def unload(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self, target_fps: int = None):
        self.__game.run(target_fps)