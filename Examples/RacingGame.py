from src import *
from src.UI import *
import math

REFERENCE_RESOLUTION = Size(1280, 720)

class RacingGame(Game):
    screen_size: Size = Size(0, 0)

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

        RacingGame.screen_size = self.screen_size

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
            #self.game.change_scene(MenuScene(self.game))
            self.game.change_scene(MainScene(self.game))
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
        play_button.on_click = lambda: self.game.change_scene(MainScene(self.game))
        quit_button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(5, 0)), Size(200, 100), "Quit")
        quit_button.on_click = lambda: self.game.exit()

        self.ui_manager.add_element("playButton", play_button)
        self.ui_manager.add_element("quitButton", quit_button)


class MainScene(Scene):
    def initialize(self):
        self.game.clear_color = Colors.BLACK
        self.camera: Camera = Camera(Vector2.zero(), -self.game.window_size.to_vector2() / 2)

        self.player = Player(Sprite(self.game.assets["racecar"], Vector2(100, 0)))

        self.highway: Highway = Highway(Sprite(self.game.assets["highway"], Vector2(0, 0)))

    def update(self):
        self.highway.update()
        self.player.update()
        self.camera.position = Vector2(self.player.sprite.position.x + REFERENCE_RESOLUTION.width / 2 - 100, 0)

    def draw(self):
        self.sprite_drawer.start(self.camera.transform_matrix)

        self.highway.draw(self.sprite_drawer)
        self.player.draw(self.sprite_drawer)

        self.sprite_drawer.end()


class Entity:
    def __init__(self, sprite: Sprite):
        self.sprite: Sprite = sprite

    def update(self):
        pass

    def draw(self, sprite_drawer: SpriteDrawer):
        sprite_drawer.draw_sprite(self.sprite)


class Camera:
    def __init__(self, position: Vector2, origin: Vector2):
        self.position: Vector2 = position
        self.origin: Vector2 = origin
        self.zoom: float = 1
        self.rotation: float = 0.0

    @property
    def transform_matrix(self) -> Matrix:
        transform: Matrix = Matrix.transform(-self.position - self.origin)
        transform *= Matrix.transform(self.origin)
        transform *= Matrix.scale(Vector2(self.zoom, self.zoom))
        transform *= Matrix.rotate(self.rotation)
        transform *= Matrix.transform(-self.origin)
        return transform


class Player(Entity):
    MAX_SPEED = 20000
    ACCELERATION = 200
    DECELERATION = 100
    BRAKING = 500

    TURNING_SPEED = 1.2

    @property
    def forward(self) -> Vector2:
        return Vector2(math.cos(self.sprite.rotation), math.sin(self.sprite.rotation))

    def __init__(self, sprite: Sprite):
        super().__init__(sprite)
        self.sprite.scale = Vector2(0.15, 0.15)
        self.sprite.origin = self.sprite.texture.size.to_vector2() / 2

        self.velocity: float = 0

    def update(self):
        if Input.key_down(Keys.K_RIGHT):
            self.velocity += Player.ACCELERATION * Time.delta_time()
        elif Input.key_down(Keys.K_LEFT):
            self.velocity -= Player.BRAKING * Time.delta_time()
        else:
            self.velocity -= Player.DECELERATION * Time.delta_time()

        if Input.key_down(Keys.K_UP):
            self.sprite.rotation -= Player.TURNING_SPEED * Time.delta_time()
        if Input.key_down(Keys.K_DOWN):
            self.sprite.rotation += Player.TURNING_SPEED * Time.delta_time()

        self.velocity = PGSMath.clamp(self.velocity, 0, Player.MAX_SPEED)
        self.sprite.position += self.velocity * self.forward * Time.delta_time()

    def draw(self, sprite_drawer: SpriteDrawer):
        sprite_drawer.draw_sprite(self.sprite)


class Highway(Entity):
    def __init__(self, sprite: Sprite):
        super().__init__(sprite)
        self.sprite.rotation = PGSMath.degrees_to_radians(90)
        self.sprite.origin = Vector2(self.sprite.texture.size.width / 2, self.sprite.texture.size.height)


if __name__ == "__main__":
    game = RacingGame(1280, 720, "Racing Game Example", resizable=True)

    game.run(60)
