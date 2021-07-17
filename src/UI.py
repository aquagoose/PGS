import _PGS as _p
import abc as _abc


class UIManager:
    def __init__(self, sprite_drawer: _p.SpriteDrawer):
        self.sprite_drawer: _p.SpriteDrawer = sprite_drawer
        self.__ui_elements: dict = {}
        self.__reversed_ui_elements: list = []

    def update(self):
        mouse_taken: bool = False
        for element in self.__reversed_ui_elements:
            mouse_taken = element.update()

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
        for i in range(len(self.__ui_elements) - 1, 0, -1):
            self.__reversed_ui_elements.append(self.__ui_elements[list(self.__ui_elements)[i]])


class UIElement(_abc.ABC):
    def __init__(self, ui_manager: UIManager, position: _p.Vector2, size: _p.Size, color: _p.Color):
        self._ui_manager: UIManager = ui_manager
        self._sprite_drawer: _p.SpriteDrawer = ui_manager.sprite_drawer
        self.position: _p.Vector2 = position
        self.size: _p.Size = size
        self.color: _p.Color = color

        self.rotation: float = 0
        self.origin: _p.Vector2 = _p.Vector2.zero()

        self.mouse_transparent: bool = False
        self.visible: bool = True
        self.disabled: bool = False
        self.focused: bool = False
        self._hovering: bool = False

    def update(self, mouse_taken: bool):
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

        # TODO: position
        #self.position.update()

    @_abc.abstractmethod
    def draw(self):
        pass


class FillRectangle(UIElement):
    def __init__(self, ui_manager: UIManager, position: _p.Vector2, size: _p.Size, color: _p.Color, ignore_mouse: bool = True):
        super().__init__(ui_manager, position, size, color)
        self.__texture = _p.Texture.custom(1, 1)
        self.__texture.set_pixels([_p.Colors.WHITE])
        self.mouse_transparent = ignore_mouse

    def draw(self):
        self._sprite_drawer.draw_texture(self.__texture, self.position, self.color, self.origin, self.size.to_vector2(), self.rotation)


class BorderRectangle(UIElement):
    def __init__(self, ui_manager: UIManager, position: _p.Vector2, size: _p.Size, border_width: int, color: _p.Color, ignore_mouse: bool = True):
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
        self._sprite_drawer.draw_texture(self.__texture, self.position, self.color, self.origin, _p.Vector2.one(), self.rotation)
