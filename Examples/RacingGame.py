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

        self.__last_resolution = Size(0, 0)

        RacingGame.screen_size = self.window_size

        self.rendert = RenderTarget(Size(200, 200))

    def update(self):
        if Input.key_pressed(Keys.K_G):
            if self.fullscreen:
                self.fullscreen = False
                # FIXME: This does not set the resolution
                self.window_size = self.__last_resolution
            else:
                self.__last_resolution = self.window_size
                self.window_size = Size(1920, 1080)
                self.fullscreen = True

        self.current_scene.update()

    def draw(self):
        self.current_scene.draw()

    def change_scene(self, scene: 'Scene'):
        self.current_scene.unload()
        self.current_scene = scene
        self.current_scene.initialize()

    def resize(self):
        RacingGame.screen_size = self.window_size
        self.current_scene.resize()


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

    def resize(self):
        pass


class LoadAssetsScene(Scene):
    def initialize(self):
        self.has_one_frame_been_processed = False
        loading_label = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Loading...", 100)
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
        self.camera: Camera = Camera(Vector2.zero(), Vector2.zero())

        self.player = Player(Sprite(self.game.assets["racecar"], Vector2(100, 0)))

        self.highway: Highway = Highway(Sprite(self.game.assets["highway"], Vector2(0, 0)))
        self.ai: CarAI = CarAI(self.game.assets["racecar"])

        self.speed_label = Label(self.ui_manager, Position(DockType.BOTTOM_LEFT, Vector2(0, -50)), Colors.WHITE, "0")
        self.speed_label.position.offset = Vector2(0, -self.speed_label.screen_size.height)

        self.ui_manager.add_element("speedLabel", self.speed_label)

    def update(self):
        self.ui_manager.update()
        self.player.update()
        self.speed_label.text = f"{int(self.player.speed)} km/h"
        self.camera.position = Vector2(self.player.sprite.position.x - 100, -self.game.window_size.height / 2)
        self.highway.update(self.camera.position)
        self.ai.update()

    def draw(self):
        self.sprite_drawer.start(self.camera.transform_matrix)

        self.highway.draw(self.sprite_drawer)
        self.ai.draw(self.sprite_drawer)
        self.player.draw(self.sprite_drawer)

        self.sprite_drawer.end()

        self.ui_manager.draw()

    def resize(self):
        self.highway.generate_roads()


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
    MAX_SPEED = 200000000
    ACCELERATION = 200000000
    DECELERATION = 100
    BRAKING = 500
    MAX_SPEED_KMH = 30000000

    TURNING_SPEED = 1.2

    @property
    def forward(self) -> Vector2:
        return Vector2(math.cos(self.sprite.rotation), math.sin(self.sprite.rotation))

    @property
    def speed(self) -> float:
        return self.velocity * (Player.MAX_SPEED_KMH / Player.MAX_SPEED)

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
        self.sprite.rotation = PGSMath.clamp(self.sprite.rotation, PGSMath.degrees_to_radians(-90),
                                             PGSMath.degrees_to_radians(90))
        self.sprite.position += self.velocity * self.forward * Time.delta_time()
        self.sprite.position.y = PGSMath.clamp(self.sprite.position.y, -245, 250)

        if Input.mouse_button_down(MouseButtons.M_LEFT):
            print("Presse")

    def draw(self, sprite_drawer: SpriteDrawer):
        sprite_drawer.draw_sprite(self.sprite)


class Highway:
    def __init__(self, sprite: Sprite):
        self.road_sprite = sprite
        self.road_sprite.rotation = PGSMath.degrees_to_radians(90)
        self.road_sprite.origin = Vector2(self.road_sprite.texture.size.width / 2, self.road_sprite.texture.size.height)
        self.roads = []
        self.generate_roads()

    def generate_roads(self):
        self.roads.clear()
        roads_needed = math.ceil(RacingGame.screen_size.width / self.road_sprite.texture.size.height) + 1
        for i in range(roads_needed):
            road: Sprite = Sprite.from_sprite(self.road_sprite)
            self.roads.append(road)
            self.roads[i].position += Vector2(i * self.road_sprite.texture.size.height, 0)

    def update(self, camera_position: Vector2):
        if camera_position.x >= self.roads[len(self.roads) - 1].position.x + self.roads[len(self.roads) - 1].texture.size.height:
            for i in range(len(self.roads)):
                self.roads[i].position = Vector2(camera_position.x + (i * self.roads[i].texture.size.height), 0)
        if camera_position.x >= self.roads[0].position.x + self.roads[0].texture.size.height:
            self.roads[0].position = Vector2(self.roads[len(self.roads) - 1].position.x + self.roads[len(self.roads) - 1].texture.size.height, 0)
            road0 = self.roads[0]
            for i in range(len(self.roads) - 1):
                self.roads[i] = self.roads[i + 1]
            self.roads[len(self.roads) - 1] = road0

    def draw(self, sprite_drawer: SpriteDrawer):
        for road in self.roads:
            sprite_drawer.draw_sprite(road)


class CarAI:
    SPEED = 200

    def __init__(self, texture: Texture):
        self.car_sprite = Sprite(texture, RacingGame.screen_size.to_vector2())
        self.car_sprite.scale = Vector2(0.15, 0.15)
        self.car_sprite.rotation = PGSMath.degrees_to_radians(180)

    def update(self):
        pass

    def draw(self, sprite_drawer: SpriteDrawer):
        sprite_drawer.draw_sprite(self.car_sprite)


if __name__ == "__main__":
    game = RacingGame(1280, 720, "Racing Game Example", resizable=True)

    game.run(60)
