from src import *


class Test(Game):
    def initialize(self):
        self.sprite_drawer = SpriteDrawer()
        self.texture = Texture.custom(200, 100)
        colors = []
        for i in range(200 * 100):
            colors.append(Colors.WHITE)
        self.texture.set_data(colors)
        pass

    def update(self):
        pass

    def draw(self):
        self.sprite_drawer.start()
        self.sprite_drawer.draw_texture(self.texture, Vector2(100, 100))
        self.sprite_drawer.end()
        pass


if __name__ == "__main__":
    test = Test(1280, 720)
    test.run()