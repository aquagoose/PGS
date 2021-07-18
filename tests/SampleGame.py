from src import *
from src.UI import *
import math
from random import randint as r


class SampleGame(Game):
    def initialize(self):
        self.active_scene: Scene = MenuScene(self)
        self.active_scene.initialize()

    def update(self):
        if self.active_scene is not None:
            self.active_scene.update()

    def draw(self):
        if self.active_scene is not None:
            self.active_scene.draw()

    def change_scene(self, scene: 'Scene'):
        self.active_scene.unload()
        self.active_scene = scene
        self.active_scene.initialize()


class Scene:
    def __init__(self, game: SampleGame):
        self.game: SampleGame = game

    def initialize(self):
        pass

    def unload(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MenuScene(Scene):
    def initialize(self):
        self.game.clear_color = Colors.YELLOW_GREEN
        self.sprite_drawer = SpriteDrawer()
        self.ui_manager = UIManager(self.sprite_drawer)
        self.should_load = False

        self.ui_manager.ui_defaults = UIDefaults(Color.from_hex(0x853A76), Color.from_hex(0x4B0C3B), Color.from_hex(0x4B0C3B), Colors.PURPLE, Colors.WHITE, 36)

        title = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Racing Game", 100)
        title.position.offset = (-title.screen_size.to_vector2() / 2) + Vector2(0, -200)
        self.ui_manager.add_element("title", title)

        self.loading = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Loading...", 50)
        self.loading.position.offset = (-self.loading.screen_size.to_vector2() / 2) + Vector2(0, 300)
        self.loading.visible = False
        self.ui_manager.add_element("loading", self.loading)

        endless = Button(self.ui_manager, Position(DockType.CENTER, Vector2(-300, -50)), Size(200, 100), "Play Endless")
        endless.on_click = self.endless_click
        self.ui_manager.add_element("endless", endless)

    def update(self):
        if self.should_load:
            self.game.change_scene(MainScene(self.game))
        self.ui_manager.update()

    def draw(self):
        self.ui_manager.draw()

    def endless_click(self):
        self.should_load = True
        self.loading.visible = True


class MainScene(Scene):
    def initialize(self):
        self.game.clear_color = Colors.BLACK
        self.sprite_drawer = SpriteDrawer()
        self.ui_manager = UIManager(self.sprite_drawer)
        self.ui_manager.ui_defaults = UIDefaults(Color.from_hex(0x853A76), Color.from_hex(0x4B0C3B),
                                                 Color.from_hex(0x4B0C3B), Colors.PURPLE, Colors.WHITE, 36)

        self.car_texture = Texture("./Assets/racecar.png")
        self.car = PlayerCar(Sprite(self.car_texture, Vector2(100, 720 / 2)))
        self.camera = Camera()
        self.camera.origin = Vector2(0, self.game.window_size.height / 2)

        self.road_system = RoadSystem(Texture("./Assets/highway.png"), Vector2(0, 720 / 2))
        self.cars = []
        self.spawned = False

        self.speed_label = Label(self.ui_manager, Position(DockType.BOTTOM_LEFT, Vector2.zero()), Colors.WHITE, "300 km/h")
        self.speed_label.position.offset = Vector2(0, -self.speed_label.screen_size.height)
        self.ui_manager.add_element("speed", self.speed_label)

        self.points = 200
        self.points_label = Label(self.ui_manager, Position.from_xy(0, 0), Colors.WHITE, str(self.points))
        self.ui_manager.add_element("points", self.points_label)

        self.game_over_label = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Game Over!", 100)
        self.game_over_label.position.offset = (-self.game_over_label.screen_size.to_vector2() / 2) + Vector2(0, -200)
        self.game_over_label.visible = False
        self.ui_manager.add_element("game_over", self.game_over_label)

        self.length_label = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Placeholder", 50)
        self.length_label.position.offset = (-self.length_label.screen_size.to_vector2() / 2) + Vector2(0, -100)
        self.length_label.visible = False
        self.ui_manager.add_element("length", self.length_label)

        self.retry_button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(-250, -50)), Size(200, 100), "Retry")
        self.retry_button.on_click = self.reload
        self.retry_button.visible = False
        self.menu_button = Button(self.ui_manager, Position(DockType.CENTER, Vector2(50, -50)), Size(200, 100), "Main Menu")
        self.menu_button.on_click = lambda: self.game.change_scene(MenuScene(self.game))
        self.menu_button.visible = False

        self.ui_manager.add_element("retry_button", self.retry_button)
        self.ui_manager.add_element("menu_button", self.menu_button)

        self.loading = Label(self.ui_manager, Position(DockType.CENTER, Vector2.zero()), Colors.WHITE, "Loading...", 50)
        self.loading.position.offset = (-self.loading.screen_size.to_vector2() / 2) + Vector2(0, 300)
        self.loading.visible = False
        self.ui_manager.add_element("loading", self.loading)
        self.should_reload = False

        self.starting_time = Time.elapsed_milliseconds()
        self.lerp_time = None

    def update(self):
        if self.should_reload:
            self.game.change_scene(MainScene(self.game))
        if Input.key_pressed(Keys.K_ESCAPE):
            self.game.exit()

        self.car.update(self.camera.position)
        self.road_system.update(self.camera.position)
        self.camera.position.x = self.car.sprite.position.x - 100
        self.speed_label.text = f"{int(self.car.speed_in_kmh)} km/h"
        self.points_label.text = str(self.points)

        if self.camera.position.x % 1000 <= 500 and not self.car.game_over:
            if not self.spawned:
                self.cars.append(Car(Sprite(self.car_texture, Vector2(self.game.window_size.width + 100 + self.camera.position.x, r(115, 610)))))
                self.spawned = True
        else:
            self.spawned = False

        # lol... spawns a new car every frame. uncomment for a laugh
        #for i in range(1):
        #    self.cars.append(Car(Sprite(self.car_texture, Vector2(self.window_size.width + 100 + self.camera.position.x, r(115, 610)))))

        for car in self.cars:
            car.update(self.camera.position)
            if self.car.sprite.position.x <= car.sprite.position.x + car.sprite.texture.size.width * car.sprite.scale.x and self.car.sprite.position.x + self.car.sprite.texture.size.width * self.car.sprite.scale.x > car.sprite.position.x and self.car.sprite.position.y <= car.sprite.position.y + car.sprite.texture.size.height * car.sprite.scale.y and self.car.sprite.position.y + self.car.sprite.texture.size.height * self.car.sprite.scale.y > car.sprite.position.y and not car.has_added:
                self.points -= 50
                self.car.velocity -= 500
                car.has_added = True
            elif self.car.sprite.position.x >= car.sprite.position.x and not car.has_added:
                self.points += 10
                car.has_added = True
            if car.destroy:
                self.cars.remove(car)
        if self.points < 0:
            if self.lerp_time is None:
                self.lerp_time = Time.elapsed_milliseconds()
                self.cars.clear()
                self.points_label.visible = False
                self.game_over_label.visible = True
                lasted_seconds = int(((self.lerp_time - self.starting_time) / 1000) % 60)
                lasted_minutes = int((self.lerp_time - self.starting_time) / (1000 * 60) % 60)
                self.length_label.text = f"You lasted {'%02d:%02d' % (lasted_minutes, lasted_seconds)}"
                self.length_label.position.offset = (-self.length_label.screen_size.to_vector2() / 2) + Vector2(0, -100)
                self.length_label.visible = True
                self.retry_button.visible = True
                self.menu_button.visible = True
            self.car.game_over = True
            self.car.velocity -= PlayerCar.BRAKING * Time.delta_time()
            delta = PGSMath.clamp((Time.elapsed_milliseconds() - self.lerp_time) / 1000 / 3, 0, 1)
            current_camera_pos = self.camera.position
            self.camera.position = Vector2.lerp(current_camera_pos, self.car.sprite.position - Vector2(1280, 720) / 2, delta)
            current_camera_origin = self.camera.origin
            self.camera.origin = Vector2.lerp(current_camera_origin, Vector2(1280, 720) / 2, delta)
            ##self.camera.origin = Vector2(1280, 720) / 2
            self.camera.zoom = PGSMath.lerp(1, 1.5, delta)
            if delta >= 1:
                self.camera.rotation += 0.1 * Time.delta_time()

        self.ui_manager.update()

    def draw(self):
        self.sprite_drawer.start(self.camera.transform_matrix(self.game.window_size))
        self.road_system.draw(self.sprite_drawer)
        for car in self.cars:
            car.draw(self.sprite_drawer)
        self.car.draw(self.sprite_drawer)
        self.sprite_drawer.end()

        self.ui_manager.draw()

    def reload(self):
        self.should_reload = True
        self.loading.visible = True


class Entity:
    def __init__(self, sprite: Sprite):
        self.sprite = sprite

    def update(self, camera_position: Vector2):
        pass

    def draw(self, sprite_drawer: SpriteDrawer):
        sprite_drawer.draw_sprite(self.sprite)


class PlayerCar(Entity):
    SPEED = 2000
    ACCELERATION = 200
    DECELERATION = 100
    BRAKING = 500
    TURN_SPEED = 1.2

    SPEED_IN_KMH = 300

    @property
    def speed_in_kmh(self) -> float:
        return self.velocity * (PlayerCar.SPEED_IN_KMH / PlayerCar.SPEED)

    @property
    def forward(self) -> Vector2:
        return Vector2(math.cos(self.sprite.rotation), math.sin(self.sprite.rotation))

    def __init__(self, sprite: Sprite):
        super().__init__(sprite)
        self.sprite.scale = Vector2(0.15, 0.15)
        self.sprite.origin = self.sprite.texture.size.to_vector2() / 2
        self.velocity = 0
        self.game_over = False

    def update(self, camera_position: Vector2):
        if not self.game_over:
            if Input.key_down(Keys.K_RIGHT):
                self.velocity += PlayerCar.ACCELERATION * Time.delta_time()
            else:
                self.velocity -= PlayerCar.DECELERATION * Time.delta_time()
            if Input.key_down(Keys.K_LEFT):
                self.velocity -= PlayerCar.BRAKING * Time.delta_time()

            if Input.key_down(Keys.K_UP):
                self.sprite.rotation -= PlayerCar.TURN_SPEED * Time.delta_time()
            if Input.key_down(Keys.K_DOWN):
                self.sprite.rotation += PlayerCar.TURN_SPEED * Time.delta_time()

        self.velocity = PGSMath.clamp(self.velocity, 0, PlayerCar.SPEED)
        self.sprite.position += self.velocity * self.forward * Time.delta_time()
        self.sprite.position.y = PGSMath.clamp(self.sprite.position.y, 115, 610)


class Camera:
    def __init__(self, start_pos: Vector2 = Vector2.zero()):
        self.position: Vector2 = start_pos
        self.origin: Vector2 = Vector2.zero()
        self.zoom: float = 1
        self.rotation = 0
        self.reference_resolution: Size = Size(1280, 720)

    def transform_matrix(self, screen_size: Size):
        return Matrix.transform(-self.position) * Matrix.transform(-self.origin) * Matrix.rotate(float(self.rotation)) * Matrix.scale(Vector2(self.zoom, self.zoom)) * Matrix.transform(self.origin) * Matrix.scale(Vector2(screen_size.width / self.reference_resolution.width, screen_size.height / self.reference_resolution.height))


class RoadSystem:
    def __init__(self, road_texture: Texture, starting_pos: Vector2):
        self.roads = []

        self.road1 = Sprite(road_texture, starting_pos)
        self.road1.origin = Vector2(self.road1.texture.size.width / 2, self.road1.texture.size.height)
        self.road1.rotation = PGSMath.degrees_to_radians(90)
        self.roads.append(self.road1)

        self.road2 = Sprite.from_sprite(self.road1)
        self.road2.position += Vector2(self.road1.texture.size.height, 0)
        self.roads.append(self.road2)

        self.road3 = Sprite.from_sprite(self.road2)
        self.road3.position += Vector2(self.road2.texture.size.height, 0)
        self.roads.append(self.road3)

        # We really only need 3 roads, but at fast speeds you can sometimes see the background colour.
        self.road4 = Sprite.from_sprite(self.road3)
        self.road4.position += Vector2(self.road3.texture.size.height, 0)
        self.roads.append(self.road4)

    def update(self, camera_position: Vector2):
        if camera_position.x >= self.roads[0].position.x + self.roads[0].texture.size.height:
            road = self.roads.pop(0)
            last_road = self.roads[len(self.roads) - 1]
            road.position = last_road.position + Vector2(last_road.texture.size.height, 0)
            self.roads.append(road)

    def draw(self, sprite_drawer: SpriteDrawer):
        for road in self.roads:
            sprite_drawer.draw_sprite(road)


class Car(Entity):
    CAR_SPEED = 500

    def __init__(self, sprite: Sprite):
        super().__init__(sprite)
        self.sprite.scale = Vector2(0.15, 0.15)
        self.sprite.origin = self.sprite.texture.size.to_vector2() / 2
        self.sprite.rotation = PGSMath.degrees_to_radians(180)
        self.sprite.color = Color(r(0, 255), r(0, 255), r(0, 255))
        self.destroy = False
        self.has_added = False

    def update(self, camera_position: Vector2):
        self.sprite.position.x -= Car.CAR_SPEED * Time.delta_time()
        if self.sprite.position.x + 100 <= camera_position.x:
            self.destroy = True


if __name__ == "__main__":
    game = SampleGame(1280, 720, "Sample Game")
    #game.fullscreen = True
    game.run()