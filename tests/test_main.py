from src import *
from src.UI import *


class Test(Game):
    def initialize(self):
        self.sprite_drawer = SpriteDrawer()
        self.low_res_sprite = Sprite(Texture(r"D:\Users\ollie\Pictures\unknown.png"), self.window_size.to_vector2() / 2)
        self.low_res_sprite.scale = Vector2(5, 5)
        self.low_res_sprite.origin = self.low_res_sprite.texture.size.to_vector2() / 2

        self.clear_color = Colors.CORNFLOWER_BLUE

    def update(self):
        pass

    def draw(self):
        self.sprite_drawer.start(pixel_mode=PixelMode.Clamp)
        self.sprite_drawer.draw_sprite(self.low_res_sprite)
        self.sprite_drawer.end()
        pass


if __name__ == "__main__":
    test = Test(1280, 720)
    test.run()