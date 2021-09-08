# Python Graphics Set by Ollie Robinson, 2021.
# Using a GPL-3.0 License. Feel free to use this
# in any project you like! Please remember to give credit
# in your project if you use it! (Preferably as a small note
# in your game.)

# Please also note, don't use this code as a python tutorial!
# It breaks many many many rules of python, including private
# and protected attribute rules. But I do it because I find
# Python's lack of true private, & especially internal (C#)
# method support. So I cheat. Don't do what I do. Please.
# It's not good python.
# It works though. And if you're just using the PGS you won't
# notice anything off, it follows PEP-8 when you're using the PGS.

import os as _os
import clr as __clr
import sys as __sys
__sys.path.append(_os.path.dirname(__file__) + "/lib")
__clr.AddReference("MonoGame.Framework")
__clr.AddReference("PGS")
__clr.AddReference("FontStashSharp.Monogame")
import Microsoft.Xna.Framework as _mg
import Microsoft.Xna.Framework.Graphics as _mgGraphics
import Microsoft.Xna.Framework.Input as _mgInput
import FontStashSharp as _fontStash
from System import TimeSpan as _timeSpan
from System.IO import File as _file
from System.IO import Path as _path
import PRS as _prs
import abc as _abc
import math as _math
from enum import Enum as _enum

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

    @staticmethod
    def lerp(value1: 'Vector2', value2: 'Vector2', amount: float) -> 'Vector2':
        lerp_val = _mg.Vector2.Lerp(_mg.Vector2(float(value1.x), float(value1.y)), _mg.Vector2(float(value2.x), float(value2.y)), float(amount))
        return Vector2(lerp_val.X, lerp_val.Y)

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
        return Matrix._to_pgs_matrix(_mg.Matrix.CreateTranslation(float(value.x), float(value.y), float(0)))

    @staticmethod
    def rotate(value: float) -> 'Matrix':
        return Matrix._to_pgs_matrix(_mg.Matrix.CreateRotationZ(value))

    @staticmethod
    def scale(value: Vector2) -> 'Matrix':
        return Matrix._to_pgs_matrix(_mg.Matrix.CreateScale(_mg.Vector3(float(value.x), float(value.y), float(1))))

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        return Matrix._to_pgs_matrix(_mg.Matrix.Multiply(self._to_mg_matrix(), other._to_mg_matrix()))


    def _to_mg_matrix(self) -> _mg.Matrix:
        return _mg.Matrix(float(self.m11), float(self.m12), float(self.m13), float(self.m14), float(self.m21),
                          float(self.m22), float(self.m23), float(self.m24), float(self.m31), float(self.m32),
                          float(self.m33), float(self.m34), float(self.m41), float(self.m42), float(self.m43),
                          float(self.m44))

    @staticmethod
    def _to_pgs_matrix(matrix: _mg.Matrix) -> 'Matrix':
        return Matrix(matrix.M11, matrix.M12, matrix.M13, matrix.M14, matrix.M21, matrix.M22, matrix.M23, matrix.M24,
                      matrix.M31, matrix.M32, matrix.M33, matrix.M34, matrix.M41, matrix.M42, matrix.M43, matrix.M44)


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

class Texture:
    @property
    def size(self) -> Size:
        return Size(self._texture.Width, self._texture.Height)

    def __init__(self, path: str):
        if (path == "CUSTOM"):
            self._texture = None
        else:
            try:
                self._texture = _mgGraphics.Texture2D.FromFile(_GameBackend.graphics_device, path)
            except:
                raise AttributeError("Path cannot be an empty string." if path == "" else "Could not find file with the given path.")

    @staticmethod
    def custom(width: int, height: int):
        tex = Texture("CUSTOM")
        tex._texture = _mgGraphics.Texture2D(_GameBackend.graphics_device, width, height)
        return tex

    def set_pixels(self, data: list[Color]):
        colors = []
        for i in range(len(data)):
            colors.append(_mg.Color(data[i].r, data[i].g, data[i].b, data[i].a))
        _prs.PGSUtils.SetTexturePixels(self._texture, colors)

class SpriteBase(_abc.ABC):
    def __init__(self):
        self.position: Vector2 = Vector2.zero()
        self.rotation: float = 0
        self.scale: Vector2 = Vector2.one()
        self.color: Color = Colors.WHITE
        self.origin: Vector2 = Vector2.zero()

    @_abc.abstractmethod
    def _draw(self, spriteBatch):
        pass

class Sprite(SpriteBase):
    def __init__(self, texture: Texture, position: Vector2):
        super().__init__()
        self.texture: Texture = texture
        self.position: Vector2 = position

    @staticmethod
    def from_sprite(sprite: 'Sprite'):
        new_sprite = Sprite(sprite.texture, sprite.position)
        new_sprite.origin = sprite.origin
        new_sprite.color = sprite.color
        new_sprite.scale = sprite.scale
        new_sprite.rotation = sprite.rotation
        return new_sprite

    def _draw(self, spriteBatch):
        spriteBatch.Draw(self.texture._texture, _mg.Vector2(float(self.position.x), float(self.position.y)), None,
            _mg.Color(self.color.r, self.color.g, self.color.b, self.color.a), float(self.rotation),
            _mg.Vector2(float(self.origin.x), float(self.origin.y)), _mg.Vector2(float(self.scale.x), float(self.scale.y)),
            _mgGraphics.SpriteEffects(0), float(0))

class PixelMode(_enum):
    Linear = 0
    Clamp = 1

class SpriteDrawer:
    def __init__(self):
        self.__spriteBatch = _mgGraphics.SpriteBatch(_GameBackend.graphics_device)
        self.__statics: dict = {}
        self.__dynamics: dict = {}
        self.__begin: bool = False

    def start(self, transform_matrix: Matrix = Matrix.identity(), pixel_mode: PixelMode = PixelMode.Linear):
        if self.__begin:
            raise DrawError("You must call 'end()' first, before you can call 'start()' again.")
        self.__spriteBatch.Begin(_mgGraphics.SpriteSortMode.Deferred, None,
                                 _mgGraphics.SamplerState.LinearClamp if pixel_mode == PixelMode.Linear else _mgGraphics.SamplerState.PointClamp,
                                 None, None, None, transform_matrix._to_mg_matrix());
        self.__begin = True

    def end(self):
        if not self.__begin:
            raise DrawError("You must call 'start()' before you can call 'end()'.")
        self.__spriteBatch.End();
        self.__begin = False

    def draw_texture(self, texture: Texture, position: Vector2, color: Color = Colors.WHITE, origin: Vector2 = Vector2.zero(),
                    scale: Vector2 = Vector2.one(), rotation: float = 0, flipped: bool = False):
        if not self.__begin:
            raise DrawError("You must call 'start()' before you can draw to the screen.")
        self.__spriteBatch.Draw(texture._texture, _mg.Vector2(float(position.x), float(position.y)), None,
            _mg.Color(color.r, color.g, color.b, color.a), float(rotation), _mg.Vector2(float(origin.x), float(origin.y)),
            _mg.Vector2(float(scale.x), float(scale.y)), _mgGraphics.SpriteEffects(0), float(0))

    def draw_sprite(self, sprite: SpriteBase):
        if not self.__begin:
            raise DrawError("You must call 'start()' before you can draw to the screen.")
        sprite._draw(self.__spriteBatch)

    def draw_text(self, font_name: str, font_size: int, text: str, position: Vector2, color: Color = Colors.WHITE, origin: Vector2 = Vector2.zero()):
        _FontManager.get_font(font_name, font_size).DrawText(self.__spriteBatch, text,
                                                             _mg.Vector2(float(position.x), float(position.y)),
                                                             _mg.Color(color.r, color.g, color.b, color.a),
                                                             _mg.Vector2.One, 0.0, _mg.Vector2(float(origin.x), float(origin.y)))

    def add_static(self, sprite_name: str, sprite: SpriteBase):
        self.__statics[sprite_name] = sprite

    def get_static(self, sprite_name: str):
        return self.__statics[sprite_name]

    def delete_static(self, sprite_name: str):
        self.__statics.pop(sprite_name)

    def draw_statics(self, transform_matrix: Matrix = Matrix.identity()):
        if (self.__begin):
            raise DrawError("Static sprite drawing must occur seperately to regular sprite drawing.")
        # TODO: Fix whatever weird transparency issues is going on
        self.__spriteBatch.Begin(_mgGraphics.SpriteSortMode.Deferred, None, None, None, None, None, transform_matrix._to_mg_matrix())
        for sprite in self.__statics:
            self.__statics[sprite]._draw(self.__spriteBatch)
        self.__spriteBatch.End()

class DrawError(Exception):
    pass

class _FontManager:
    __fonts: dict[str, _fontStash.FontSystem] = {}

    @staticmethod
    def get_font(name: str, size: int):
        if not name in _FontManager.__fonts:
            settings: _fontStash.FontSystemSettings = _fontStash.FontSystemSettings()
            settings.TextureWidth = 1024
            settings.TextureHeight = 1024
            system: _fontStash.FontSystem = _fontStash.FontSystem(settings)
            system.AddFont(_file.ReadAllBytes(_os.path.dirname(__file__) + f"/lib/Fonts/{name}.ttf"))
            _FontManager.__fonts[name] = system
        return _FontManager.__fonts[name].GetFont(size)


class _GameBackend(_prs.PGSGame):
    graphics_device = None

    def __init__(self, game, width: int, height: int, title: str, show_credits: bool, vsync: bool, resizable: bool):
        self.game: Game = game
        self.graphics: _mg.GraphicsDeviceManager = _mg.GraphicsDeviceManager(self)
        self.graphics.PreferredBackBufferWidth = width
        self.graphics.PreferredBackBufferHeight = height
        self.titleText = title
        self.show_credits = show_credits
        self.Window.Title = self.titleText + " - Python Graphics Set - FPS: " if self.show_credits else self.titleText
        self.IsMouseVisible = True
        self.Window.AllowUserResizing = resizable
        if (self.show_credits):
            print("Hey there, from the Python Graphics Set!\nhttps://github.com/ohtrobinson/PGS")

        self.InitializeEvent += self.initialize
        self.UpdateEvent += self.update
        self.DrawEvent += self.draw

        self.graphics.SynchronizeWithVerticalRetrace = vsync
        self.IsFixedTimeStep = False

        self.Window.KeyDown += Input._set_key_down
        self.Window.KeyUp += Input._set_key_up
        self.Window.ClientSizeChanged += self.__resize
        self.clear_color = _mg.Color(0, 0, 0)
        self.counter = 0

    def initialize(self):
        # TODO: Enable MSAA
        #self.graphics.GraphicsProfile = _mgGraphics.GraphicsProfile.HiDef;
        #self.graphics.PreferMultiSampling = False
        #self.GraphicsDevice.PresentationParameters.MultiSampleCount = 32
        #self.graphics.ApplyChanges()
        _GameBackend.graphics_device = self.GraphicsDevice
        self.game.initialize()

    def update(self, gameTime):
        Input._update()
        Time._update(gameTime)
        if (Time.elapsed_milliseconds() - self.counter > 1000):
            self.counter = Time.elapsed_milliseconds()
            self.Window.Title = self.titleText + " - Python Graphics Set - FPS: " + str(Time.fps()) if self.show_credits else self.titleText
        self.game.update()

    def draw(self):
        self.GraphicsDevice.Clear(self.clear_color)
        self.game.draw()

    def __resize(self, sender, args):
        #self.graphics.PreferredBackBufferWidth = self.Window.ClientBounds.Width
        #self.graphics.PreferredBackBufferHeight = self.Window.ClientBounds.Width
        self.game.resize()

class Game:
    @property
    def clear_color(self) -> Color:
        return Color(self.__game.clear_color.R, self.__game.clear_color.G, self.__game.clear_color.B)

    @clear_color.setter
    def clear_color(self, value: Color):
        self.__game.clear_color = _mg.Color(value.r, value.g, value.b)

    @property
    def fullscreen(self) -> bool:
        return self.__game.graphics.IsFullScreen

    @fullscreen.setter
    def fullscreen(self, value: bool):
        self.__game.graphics.IsFullScreen = value
        self.__game.graphics.ApplyChanges()

    @property
    def window_size(self) -> Size:
        return Size(self.__game.graphics.PreferredBackBufferWidth, self.__game.graphics.PreferredBackBufferHeight)

    @window_size.setter
    def window_size(self, size: Size):
        self.__game.graphics.PreferredBackBufferWidth = size.width
        self.__game.graphics.PreferredBackBufferHeight = size.height

    def __init__(self, width: int, height: int, title: str = "PGS Window", show_credits = True, vsync: bool = True,
                 resizable: bool = False):
        """
        Create a new instance of the Game class. This will in turn create a window, which will launch once 'run()' is called.
        :param width: The width, in pixels, of the game window.
        :param height: The height, in pixels, of the game window.
        :param title: The title, if any, of the game window.
        :param show_credits: Whether the PGS should show "Python Graphics Set" in the title, and the "Hello!" message on launch. Leave this set to 'True' if you want to show some support!
        """
        self.__game: _GameBackend = _GameBackend(self, width, height, title, show_credits, vsync, resizable)
        self.clear_color = Colors.BLACK

    def initialize(self):
        pass

    def unload(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def resize(self):
        pass

    def run(self, target_fps: int = None):
        #try:
        if target_fps is not None:
            self.__game.IsFixedTimeStep = True
            self.__game.TargetElapsedTime = _timeSpan.FromMilliseconds(1000.0 / target_fps)
        self.__game.Run()
        #except Exception as e:
        #    raise Exception(f"UNKNOWN ERROR OCCURRED.\n\n{e}\n\nPlease leave this message as an issue on the github, so it can either be fixed, or the appropriate error can get raised! Thank you! :)")

    def exit(self):
        self.unload()
        self.__game.Exit()


class PGSMath:
    @staticmethod
    def pi():
        return 3.1415926535897931

    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        return degrees * (PGSMath.pi() / 180)

    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        return radians * (180 / PGSMath.pi())

    @staticmethod
    def clamp(value: float, min: float, max: float) -> float:
        if value <= min:
            return min
        elif value >= max:
            return max
        else:
            return value

    @staticmethod
    def max(value1: float, value2: float) -> float:
        return value1 if value1 > value2 else value2

    @staticmethod
    def min(value1: float, value2: float) -> float:
        return value1 if value1 < value2 else value2

    @staticmethod
    def lerp(value1: float, value2: float, amount: float) -> float:
        return value1 + amount * (value2 - value1)



class Keys(_enum):
    K_ENTER = 13
    K_ESCAPE = 27
    K_SPACE = 32

    K_LEFT = 37
    K_UP = 38
    K_RIGHT = 39
    K_DOWN = 40

    K_A = 65
    K_B = 66
    K_C = 67
    K_D = 68
    K_E = 69
    K_F = 70
    K_G = 71
    K_H = 72
    K_I = 73
    K_J = 74
    K_K = 75
    K_L = 76
    K_M = 77
    K_N = 78
    K_O = 79
    K_P = 80
    K_Q = 81
    K_R = 82
    K_S = 83
    K_T = 84
    K_U = 85
    K_V = 86
    K_W = 87
    K_X = 88
    K_Y = 89
    K_Z = 90

    K_LSHIFT = 160
    K_RSHIFT = 161
    K_LCTRL = 162
    K_RCTRL = 163


class MouseButtons(_enum):
    M_LEFT = 0
    M_RIGHT = 1


class Input:
    __keys_held: list = []
    __new_keys_this_frame: list = []

    __mouse_buttons_held: list = []
    __new_mouse_buttons_this_frame = []

    __keys_down_queue: list = []
    __keys_up_queue: list = []

    __mouse_state = None
    __last_mouse_state = None

    @staticmethod
    def key_pressed(key: Keys) -> bool:
        return key in Input.__new_keys_this_frame

    @staticmethod
    def key_down(key: Keys) -> bool:
        return key in Input.__keys_held

    @staticmethod
    def mouse_button_pressed(button: MouseButtons) -> bool:
        return button in Input.__new_mouse_buttons_this_frame

    @staticmethod
    def mouse_button_down(button: MouseButtons) -> bool:
        return button in Input.__mouse_buttons_held

    @staticmethod
    def mouse_button_up(button: MouseButtons) -> bool:
        return not Input.mouse_button_down(button)

    @staticmethod
    def mouse_position() -> Vector2:
        return Vector2(Input.__mouse_state.X, Input.__mouse_state.Y)

    @staticmethod
    def delta_mouse_position() -> Vector2:
        """Returns a Vector2 which contains the difference between the current mouse position, and last frame's mouse position."""
        return Input.mouse_position() - Vector2(Input.__last_mouse_state.X, Input.__last_mouse_state.Y)

    @staticmethod
    def _update():
        Input.__last_mouse_state = Input.__mouse_state
        Input.__new_keys_this_frame.clear()
        Input.__new_mouse_buttons_this_frame.clear()

        for key in Input.__keys_down_queue:
            Input.__key_down(key)
        Input.__keys_down_queue.clear()

        for key in Input.__keys_up_queue:
            Input.__key_up(key)
        Input.__keys_up_queue.clear()

        Input.__mouse_state = _mgInput.Mouse.GetState()
        if Input.__mouse_state.LeftButton == _mgInput.ButtonState.Pressed:
            Input.__mouse_down(MouseButtons.M_LEFT)
        else:
            Input.__mouse_up(MouseButtons.M_LEFT)

        if Input.__mouse_state.RightButton == _mgInput.ButtonState.Pressed:
            Input.__mouse_down(MouseButtons.M_RIGHT)
        else:
            Input.__mouse_up(MouseButtons.M_RIGHT)


    @staticmethod
    def __key_down(key: Keys):
        if not key in Input.__keys_held:
            Input.__keys_held.append(key)
            Input.__new_keys_this_frame.append(key)

    @staticmethod
    def __key_up(key: Keys):
        try:
            Input.__keys_held.remove(key)
            if key in Input.__new_keys_this_frame:
                Input.__new_keys_this_frame.remove(key)
        except Exception as e:
            print(e)

    @staticmethod
    def __mouse_down(button: MouseButtons):
        if not button in Input.__mouse_buttons_held:
            Input.__mouse_buttons_held.append(button)
            Input.__new_mouse_buttons_this_frame.append(button)

    @staticmethod
    def __mouse_up(button: MouseButtons):
        if button in Input.__mouse_buttons_held:
            Input.__mouse_buttons_held.remove(button)
        if button in Input.__new_mouse_buttons_this_frame:
            Input.__new_mouse_buttons_this_frame.remove(button)

    @staticmethod
    def _set_key_down(sender, key):
        try:
            Input.__keys_down_queue.append(Keys(key.Key.GetHashCode()))
        except:
            pass

    @staticmethod
    def _set_key_up(sender, key):
        try:
            Input.__keys_up_queue.append(Keys(key.Key.GetHashCode()))
        except:
            pass


class Time:
    __frames = 0
    __game_time = None
    __counter = 0
    __fps = 0
    __frames_since_last_second = 0

    @staticmethod
    def delta_time() -> float:
        return float(Time.__game_time.ElapsedGameTime.TotalSeconds)

    @staticmethod
    def elapsed_milliseconds() -> int:
        return int(Time.__game_time.TotalGameTime.TotalMilliseconds)

    @staticmethod
    def total_frames() -> int:
        return Time.__frames

    @staticmethod
    def fps_precise() -> float:
        return Time.__fps

    @staticmethod
    def fps() -> int:
        return int(Time.__fps)

    @staticmethod
    def _update(game_time):
        Time.__frames += 1
        Time.__game_time = game_time
        Time.__frames_since_last_second += 1

        if Time.elapsed_milliseconds() - Time.__counter >= 1000:
            Time.__counter = Time.elapsed_milliseconds()
            Time.__fps = Time.__frames_since_last_second
            Time.__frames_since_last_second = 0