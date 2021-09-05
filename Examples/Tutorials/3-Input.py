# Import the PGS.
# Please note you will need to change this if you are using the PGS in a different folder.
# To use this import method, the PGS source folder (which you can get from the latest release) must be placed
# in the same folder as your python file!
from src import *
from random import randint as rand

# This tutorial aims to show you how to receive input from the user.
# This tutorial assumes you understand the previous tutorials.
class SpriteDrawingAndInput(Game):
    def initialize(self):
        self.clear_color = Colors.MAROON

        self.sprite_drawer = SpriteDrawer()
        self.sprite = Sprite(Texture("./Assets/awesomeface.png"), Vector2(100, 100))
        self.sprite.scale = Vector2(0.5, 0.5)

    def update(self):
        # The key_pressed() method will return true if the key is down, however only for one frame.
        # This is useful to detect single keypresses.
        if Input.key_pressed(Keys.K_ESCAPE):
            self.exit()

        # The key_down() method will return true for as long as the key is down. This is useful for movement, etc.
        if Input.key_down(Keys.K_W):
            self.sprite.position.y -= 100 * Time.delta_time()  # You should really multiply everything by the delta time!
        if Input.key_down(Keys.K_S):
            self.sprite.position.y += 100 * Time.delta_time()
        if Input.key_down(Keys.K_A):
            self.sprite.position.x -= 100 * Time.delta_time()
        if Input.key_down(Keys.K_D):
            self.sprite.position.x += 100 * Time.delta_time()

        # What is delta time??
        # Delta time is the amount of time the previous frame took to process. It's usually a reeeaaaly small number,
        # as it's measured in seconds, and your graphics card can update the frame multiple times per second!
        # In order to get framerate independent movement, you must multiply by the delta time. If you don't, your movement
        # will speed up or slow down based on the framerate. At 3000 fps, the movement will be really fast!
        # At 1fps, the movement will be super slow. Multiply by delta time? 3000fps? Normal speed. 1fps? Normal speed.
        # You will need to make your movement values much larger, but the tradeoff is worth it.

        if Input.mouse_button_down(MouseButtons.M_LEFT):
            self.sprite.position = Input.mouse_position()

        if Input.mouse_button_pressed(MouseButtons.M_RIGHT):
            self.sprite.color = Color(rand(0, 255), rand(0, 255), rand(0, 255))

    def draw(self):
        self.sprite_drawer.start()
        self.sprite_drawer.draw_sprite(self.sprite)
        self.sprite_drawer.end()


if __name__ == "__main__":
    window = SpriteDrawingAndInput(1280, 720, "Sprite Drawing & Input")
    window.run(60)
