from src.OpenGL import *


class Test(Game):
    def initialize(self):
        self.clear_color = Colors.CORNFLOWER_BLUE

    def update(self):
        print(Input.mouse_position())

    def draw(self):
        pass


if __name__ == "__main__":
    test = Test(1280, 720, "Window")
    test.run()