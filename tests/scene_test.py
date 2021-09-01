from src import *
from src.Scenes import *

class Main(Game):
    def initialize(self):
        self.scene_manager = SceneManager(self)


if __name__ == "__main__":
    game = Main(1280, 720)
    game.run()