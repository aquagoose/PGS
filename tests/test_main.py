from src import *
from src.UI import *


class Test(Game):
    def initialize(self):
        self.sprite_drawer = SpriteDrawer()
        self.ui_manager = UIManager(self.sprite_drawer)
        button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(-100, -50)), Size(200, 100), "Hello!")
        self.ui_manager.add_element("test", button)


    def update(self):
        self.ui_manager.update()

    def draw(self):
        self.ui_manager.draw()


if __name__ == "__main__":
    test = Test(1280, 720)
    test.run()