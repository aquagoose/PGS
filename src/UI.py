import _PGS as _p
from _PGS import Colors as _c
from _PGS import Color as _co
import abc as _abc
from enum import Enum as _enum
from typing import Callable as _callable


class UIDefaults:
    def __init__(self, back_color: _co = _c.GHOST_WHITE, border_color: _co = _c.WHITE, hover_color: _co = _c.GAINSBORO,
                 click_color: _co = _c.LIGHT_GRAY, label_color: _co = _c.BLACK, label_size: int = 48,
                 label_font: str = "Arial", button_execute_on_release: bool = True, border_width: int = 2):
        self.back_color: _co = back_color
        self.border_color: _co = border_color
        self.hover_color: _co = hover_color
        self.click_color: _co = click_color
        self.label_color: _co = label_color
        self.label_size: int = label_size
        self.label_font: str = label_font
        self.button_execute_on_release: bool = button_execute_on_release
        self.border_width: int = border_width


class UIManager:
    def __init__(self, sprite_drawer: _p.SpriteDrawer):
        self.sprite_drawer: _p.SpriteDrawer = sprite_drawer
        self.__ui_elements: dict = {}
        self.__reversed_ui_elements: list = []
        self.ui_defaults = UIDefaults()

    def update(self):
        mouse_taken: bool = False
        for element in self.__reversed_ui_elements:
            mouse_taken = element.update(mouse_taken)
        #print(mouse_taken)

    def draw(self, transform_matrix: _p.Matrix = _p.Matrix.identity(), begun: bool = False):
        self.sprite_drawer.start(transform_matrix)
        for element in self.__ui_elements:
            self.__ui_elements[element].draw()
        self.sprite_drawer.end()

    def add_element(self, element_name: str, element: 'UIElement'):
        self.__ui_elements[element_name] = element
        self.__reverse_elements()

    def __reverse_elements(self):
        self.__reversed_ui_elements.clear()
        for i in range(len(self.__ui_elements) - 1, -1, -1):
            self.__reversed_ui_elements.append(self.__ui_elements[list(self.__ui_elements)[i]])


class Position:
    @property
    def screen_position(self):
        return self.__screen_position

    @property
    def x(self):
        return self.screen_position.x

    @property
    def y(self):
        return self.screen_position.y

    def __init__(self, dock_type: 'DockType', offset: _p.Vector2):
        self.dock_type: 'DockType' = dock_type
        self.offset: _p.Vector2 = offset
        self.__screen_position: _p.Vector2 = _p.Vector2.zero()
        self._update()

    @staticmethod
    def from_vector2(position: _p.Vector2):
        return Position(DockType.TOP_LEFT, position)

    @staticmethod
    def from_xy(x: float, y: float):
        return Position(DockType.TOP_LEFT, _p.Vector2(x, y))

    def _update(self):
        if self.dock_type == DockType.TOP_LEFT:
            self.__screen_position = self.offset
        elif self.dock_type == DockType.TOP_RIGHT:
            self.__screen_position = _p.Vector2(_p._GameBackend.graphics_device.ScissorRectangle.Width, 0) + self.offset
        elif self.dock_type == DockType.BOTTOM_LEFT:
            self.__screen_position = _p.Vector2(0, _p._GameBackend.graphics_device.ScissorRectangle.Height) + self.offset
        elif self.dock_type == DockType.BOTTOM_RIGHT:
            self.__screen_position = _p.Vector2(_p._GameBackend.graphics_device.ScissorRectangle.Width, _p._GameBackend.graphics_device.ScissorRectangle.Height) + self.offset
        elif self.dock_type == DockType.CENTER:
            self.__screen_position = _p.Vector2(_p._GameBackend.graphics_device.ScissorRectangle.Width, _p._GameBackend.graphics_device.ScissorRectangle.Height) / 2 + self.offset
        else:
            raise TypeError()


class DockType(_enum):
    TOP_LEFT = 0
    TOP_RIGHT = 1
    BOTTOM_LEFT = 2
    BOTTOM_RIGHT = 3
    CENTER = 4


class UIElement(_abc.ABC):
    def __init__(self, ui_manager: UIManager, position: Position, size: _p.Size, color: _p.Color):
        self._ui_manager: UIManager = ui_manager
        self._sprite_drawer: _p.SpriteDrawer = ui_manager.sprite_drawer
        self.position: Position = position
        self.size: _p.Size = size
        self.color: _p.Color = color

        self.rotation: float = 0
        self.origin: _p.Vector2 = _p.Vector2.zero()

        self.mouse_transparent: bool = False
        self.visible: bool = True
        self.disabled: bool = False
        self.focused: bool = False
        self._hovering: bool = False

    def update(self, mouse_taken: bool) -> bool:
        if self.position is not None and self.size is not None and not self.disabled and not self.mouse_transparent:
            if _p.Input.mouse_position().x >= self.position.x and _p.Input.mouse_position().x <= self.position.x + self.size.width and _p.Input.mouse_position().y >= self.position.y and _p.Input.mouse_position().y <= self.position.y + self.size.height and not mouse_taken:
                mouse_taken = True
                self._hovering = True
                if _p.Input.mouse_button_pressed(_p.MouseButtons.M_LEFT):
                    self.focused = True
            else:
                self._hovering = False
                if _p.Input.mouse_button_pressed(_p.MouseButtons.M_LEFT):
                    self.focused = False

            self.position._update()
        return mouse_taken

    @_abc.abstractmethod
    def draw(self):
        pass


class FillRectangle(UIElement):
    def __init__(self, ui_manager: UIManager, position: Position, size: _p.Size, color: _p.Color, ignore_mouse: bool = True):
        super().__init__(ui_manager, position, size, color)
        self.__texture = _p.Texture.custom(1, 1)
        self.__texture.set_pixels([_p.Colors.WHITE])
        self.mouse_transparent = ignore_mouse

    def draw(self):
        self._sprite_drawer.draw_texture(self.__texture, self.position.screen_position, self.color, self.origin, self.size.to_vector2(), self.rotation)


class BorderRectangle(UIElement):
    def __init__(self, ui_manager: UIManager, position: Position, size: _p.Size, border_width: int, color: _p.Color, ignore_mouse: bool = True):
        super().__init__(ui_manager, position, size, color)
        self.__texture = _p.Texture.custom(size.width, size.height)
        pixels = [None] * size.width * size.height
        for x in range(size.width):
            for y in range(size.height):
                if x < border_width or x > size.width - border_width - 1 or y < border_width or y > size.height - border_width - 1:
                    pixels[y * size.width + x] = _p.Colors.WHITE
                else:
                    pixels[y * size.width + x] = _p.Colors.TRANSPARENT
        self.__texture.set_pixels(pixels)
        self.mouse_transparent = ignore_mouse

    def draw(self):
        self._sprite_drawer.draw_texture(self.__texture, self.position.screen_position, self.color, self.origin, _p.Vector2.one(), self.rotation)


class Label(UIElement):
    @property
    def screen_size(self):
        font_size = _p._FontManager.get_font(self.font, self.font_size).MeasureString(self.text)
        return _p.Size(int(font_size.X), int(font_size.Y))

    def __init__(self, ui_manager: UIManager, position: Position, color: _p.Color, text: str, font_size: int = 48, font: str = "Arial"):
        super().__init__(ui_manager, position, _p.Size(0, 0), color)
        self.text: str = text
        self.font_size: int = font_size
        self.font: str = font

    def draw(self):
        self._sprite_drawer.draw_text(self.font, self.font_size, self.text, self.position.screen_position, self.color, self.origin)


class Button(UIElement):
    def __init__(self, ui_manager: UIManager, position: Position, size: _p.Size, text: str = ""):
        super().__init__(ui_manager, position, size, ui_manager.ui_defaults.back_color)
        defaults: UIDefaults = ui_manager.ui_defaults
        self.__back_color = defaults.back_color
        self.__border_width = defaults.border_width
        self.__border_color = defaults.border_color
        self.__hover_color = defaults.hover_color
        self.__click_color = defaults.click_color
        self.__label_color = defaults.label_color
        self.__label_size = defaults.label_size
        self.__label_font = defaults.label_font
        self.execute_on_release = defaults.button_execute_on_release

        self.__background = FillRectangle(ui_manager, position, size, self.__back_color)
        self.__border = BorderRectangle(ui_manager, position, size, self.__border_width, self.__border_color)
        self.__text = Label(ui_manager, Position.from_xy(position.x + size.width / 2, position.y + size.height / 2),
                            self.__label_color, text,  self.__label_size, self.__label_font)
        self.__text.origin = self.__text.screen_size.to_vector2() / 2

        self.__pressed = False
        self.on_click: _callable = lambda: None

    def update(self, mouse_taken: bool) -> bool:
        mouse_taken = super().update(mouse_taken)

        if self._hovering:
            self.__background.color = self.__hover_color
            if _p.Input.mouse_button_down(_p.MouseButtons.M_LEFT):
                self.__background.color = self.__click_color
                if not self.__pressed:
                    self.__pressed = True
                    if not self.execute_on_release:
                        self.on_click()
            elif self.execute_on_release and _p.Input.mouse_button_up(_p.MouseButtons.M_LEFT) and self.__pressed:
                self.on_click()
                self.__pressed = False
            else:
                self.__pressed = False
        else:
            self.__background.color = self.__back_color
            self.__pressed = False

        self.__background.position = self.position
        self.__background.update(mouse_taken)
        self.__border.position = self.position
        self.__border.update(mouse_taken)
        self.__text.position = Position.from_xy(self.position.x + self.size.width / 2, self.position.y + self.size.height / 2)
        self.__text.update(mouse_taken)

        return mouse_taken

    def draw(self):
        self.__background.draw()
        self.__border.draw()
        self.__text.draw()
