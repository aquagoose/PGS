from src import *
from src.UI import *


class Test(Game):
    def initialize(self):
        self.ui_manager = UIManager(SpriteDrawer())
        self.ui_manager.add_element("test", FillRectangle(self.ui_manager, Vector2(100, 150), Size(200, 100), Colors.GRAY))
        self.ui_manager.add_element("test", BorderRectangle(self.ui_manager, Vector2(100, 150), Size(200, 100), 5, Colors.WHITE))

    def update(self):
        self.ui_manager.update()

    def draw(self):
        self.ui_manager.draw()



if __name__ == "__main__":
    test = Test(1280, 720)
    test.run()