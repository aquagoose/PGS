import sys
import os
sys.path.append(os.path.dirname("../"))
from src.OpenGL import *
#print (os.path.dirname(__file__))

class Test(Game):
    def initialize(self):
        self.clear_color = Colors.CORNFLOWER_BLUE

        self.sprite_drawer = SpriteDrawer()

        self.tex = Texture("Assets/racecar.png")

    def update(self):
        if Input.mouse_button_pressed(MouseButtons.M_LEFT):
            print("pres")

    def draw(self):
        self.sprite_drawer.draw(self.tex)


if __name__ == "__main__":
    test = Test(1280, 720, "Window")
    test.run()