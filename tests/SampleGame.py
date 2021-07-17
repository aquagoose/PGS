from src import *
from src.UI import *
import math
from random import randint as r


class SampleGame(Game):
    def initialize(self):
        self.clear_color = Colors.CORNFLOWER_BLUE
        self.sprite_drawer = SpriteDrawer()
        self.ui_manager = UIManager(self.sprite_drawer)

        self.car_texture = Texture("./Assets/racecar.png")
        self.car = PlayerCar(Sprite(self.car_texture, Vector2(100, 720 / 2)))
        self.camera = Camera()
        self.camera.origin = Vector2(0, self.window_size.height / 2)

        self.road_system = RoadSystem(Texture("./Assets/highway.png"), Vector2(0, 720 / 2))
        self.cars = []
        self.spawned = False

        self.speed_label = Label(self.ui_manager, Position(DockType.BOTTOM_LEFT, Vector2.zero()), Colors.WHITE, "300 km/h")
        self.speed_label.position.offset = Vector2(0, -self.speed_label.screen_size.height)
        self.ui_manager.add_element("speed", self.speed_label)

    def update(self):
        if Input.key_pressed(Keys.K_ESCAPE):
            self.exit()

        self.car.update(self.camera.position)
        self.road_system.update(self.camera.position)
        self.camera.position.x = self.car.sprite.position.x - 100
        self.speed_label.text = f"{int(self.car.speed_in_kmh)} km/h"

        if Time.elapsed_milliseconds() % PGSMath.clamp(1000 / (PGSMath.max(self.car.velocity, 1)) * 1000, 0, 1000) <= 50:
            if not self.spawned:
                self.cars.append(Car(Sprite(self.car_texture, Vector2(self.window_size.width + 100 + self.camera.position.x, r(115, 610)))))
                self.spawned = True
        else:
            self.spawned = False

        # lol... spawns a new car every frame. uncomment for a laugh
        #for i in range(1):
        #    self.cars.append(Car(Sprite(self.car_texture, Vector2(self.window_size.width + 100 + self.camera.position.x, r(115, 610)))))

        for car in self.cars:
            car.update(self.camera.position)
            if car.destroy:
                self.cars.remove(car)

        self.ui_manager.update()

    def draw(self):
        self.sprite_drawer.start(self.camera.transform_matrix(self.window_size))
        self.road_system.draw(self.sprite_drawer)
        for car in self.cars:
            car.draw(self.sprite_drawer)
        self.car.draw(self.sprite_drawer)
        self.sprite_drawer.end()

        self.ui_manager.draw()


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

    def update(self, camera_position: Vector2):
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
        self.reference_resolution: Size = Size(1280, 720)

    def transform_matrix(self, screen_size: Size):
        return Matrix.transform(-self.position) * Matrix.transform(-self.origin) * Matrix.scale(Vector2(self.zoom, self.zoom)) * Matrix.transform(self.origin) * Matrix.scale(Vector2(screen_size.width / self.reference_resolution.width, screen_size.height / self.reference_resolution.height))


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
        print(self.roads[0].position)
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

    def update(self, camera_position: Vector2):
        self.sprite.position.x -= Car.CAR_SPEED * Time.delta_time()
        if self.sprite.position.x + 100 <= camera_position.x:
            self.destroy = True


if __name__ == "__main__":
    game = SampleGame(1920, 1080, "Sample Game")
    game.fullscreen = True
    game.run()