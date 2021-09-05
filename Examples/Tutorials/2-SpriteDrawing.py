# Import the PGS.
# Please note you will need to change this if you are using the PGS in a different folder.
# To use this import method, the PGS source folder (which you can get from the latest release) must be placed
# in the same folder as your python file!
from src import *

# This tutorial aims to show you how to draw sprites to the screen.
# This tutorial assumes you understand the previous tutorials.
class SpriteDrawingAndInput(Game):
    def initialize(self):
        self.clear_color = Colors.MAROON

        # Create our sprite drawer. To draw sprites at all, you must have an instance of the SpriteDrawer.
        self.sprite_drawer = SpriteDrawer()

        # A sprite is an object that can be drawn to the screen. A sprite contains texture, position, scale, rotation,
        # origin, and colour information.
        # A sprite is the recommended way to draw things to the screen, as it results in neater code generally.
        self.sprite = Sprite(Texture("./Assets/awesomeface.png"), Vector2(100, 100))
        self.sprite.scale = Vector2(0.5, 0.5)

        # The SpriteDrawer can also directly draw textures to the screen. This does give you (somewhat) finer control
        # over drawing the texture, however you need to provide all the information that is contained in a Sprite() yourself.
        self.texture = Texture("./Assets/bagel.jpg")

    def update(self):
        pass

    def draw(self):
        # Any time you want to draw sprites to the screen, you need to call the start() method. If you don't, an exception
        # will be raised. Sprites cannot be drawn outside of these calls.
        self.sprite_drawer.start()

        # Draw the sprite we defined earlier to the screen.
        self.sprite_drawer.draw_sprite(self.sprite)

        # This is how we draw textures to the screen. We need to provide all the same information that a Sprite() also contains,
        # such as position, colour, texture, scale, origin, and rotational information.
        # Doing this is fine, but it's recommended that you use a Sprite() instead, as it makes your code neater!
        self.sprite_drawer.draw_texture(self.texture, Vector2(700, 400), Colors.WHITE, self.texture.size.to_vector2() / 2,
                                        Vector2(0.1, 0.2), PGSMath.degrees_to_radians(90), False)

        # Just as start() must be called, end() must be called as well!
        self.sprite_drawer.end()


if __name__ == "__main__":
    window = SpriteDrawingAndInput(1280, 720, "Sprite Drawing")
    window.run(60)
