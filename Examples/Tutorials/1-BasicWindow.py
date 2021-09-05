# Import the PGS.
# Please note you will need to change this if you are using the PGS in a different folder.
# To use this import method, the PGS source folder (which you can get from the latest release) must be placed
# in the same folder as your python file!
from src import *

# The PGS is very heavily object oriented. You MUST have a central class that derives off the 'Game' class.
# The 'Game' class provides the initialize, update, and draw methods, as well as some settings like the window clear
# colour.
class BasicWindow(Game):
    # Initialize is called once, when the game starts.
    # Use this method to set the window clear colour, create assets, etc.
    def initialize(self):
        # Here we set the window clear colour. I won't go into detail here much,
        # but every frame the window must be cleared, to allow new objects to be
        # drawn to the screen. If we don't clear the window, the objects will just
        # be drawn on top of each other, leaving a horrible trail of objects!
        # Note: You don't need to set this, it defaults to black. The PGS automatically
        # deals with window clearing for you!
        self.clear_color = Colors.YELLOW_GREEN

    # Update is called once per frame. Put your game logic in here.
    def update(self):
        pass

    # Draw is called once per frame, after Update is called.
    # Put drawing commands in here.
    def draw(self):
        pass


if __name__ == "__main__":
    # Create a new instance of our game, with the given resolution and title.
    window = BasicWindow(1280, 720, "Basic Window")
    # Run our game!
    window.run()
