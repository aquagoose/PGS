from src import *
from src.UI import *


class RacingGame(Game):
    def initialize(self):
        # Initialize our sprite drawer & UI manager here. These will be shared throughout the scenes.
        self.sprite_drawer = SpriteDrawer()
        self.ui_manager = UIManager(self.sprite_drawer)

        # We load all the assets into this dictionary before the game starts so we don't need to load them later.
        # There are very few of them so it's fine to do this.
        self.assets: dict = {}

        # Set the current scene to the Load Assets scene.
        self.current_scene: Scene = LoadAssetsScene(self)
        self.current_scene.initialize()

    def update(self):
        self.current_scene.update()

    def draw(self):
        self.current_scene.draw()

    def change_scene(self, scene: 'Scene'):
        self.current_scene.unload()
        self.current_scene = scene
        self.current_scene.initialize()


class Scene:
    def __init__(self, game: RacingGame):
        self.game: RacingGame = game
        self.sprite_drawer = game.sprite_drawer
        self.ui_manager = game.ui_manager

    def initialize(self):
        pass

    def unload(self):
        self.ui_manager.clear_elements()

    def update(self):
        self.ui_manager.update()

    def draw(self):
        self.ui_manager.draw()


class LoadAssetsScene(Scene):
    def initialize(self):
        self.has_one_frame_been_processed = False
        loading_label = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()),Colors.WHITE, "Loading...", 100)
        loading_label.position.offset = -Vector2(loading_label.screen_size.width, loading_label.screen_size.height) / 2
        self.ui_manager.add_element("loadingText", loading_label)

    def draw(self):
        if self.has_one_frame_been_processed:
            self.load_assets()
            self.game.change_scene(MenuScene(self.game))
        else:
            self.has_one_frame_been_processed = True

        super().draw()

    def load_assets(self):
        self.game.assets["racecar"] = Texture("Assets/racecar.png")
        self.game.assets["highway"] = Texture("Assets/highway.png")


class MenuScene(Scene):
    def initialize(self):
        self.game.clear_color = Colors.INDIAN_RED

        play_button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(-205, 0)), Size(200, 100), "Play")
        quit_button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(5, 0)), Size(200, 100), "Quit")
        quit_button.on_click = lambda: self.game.exit()

        self.ui_manager.add_element("playButton", play_button)
        self.ui_manager.add_element("quitButton", quit_button)

        self.ui_manager.add_element("peenButton", Button(self.ui_manager, Position(DockType.CENTER, Vector2(5, 0)), Size(1000, 1000), "Quit"))


if __name__ == "__main__":
    game = RacingGame(1280, 720, "Racing Game Example", resizable=True)

    game.run(60)
