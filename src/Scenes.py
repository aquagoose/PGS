import _PGS as _p


class SceneManager:
    __game_class = None

    def __init__(self, game_class):
        SceneManager.__game_class = game_class
        if not issubclass(game_class, _p.Game):
            raise TypeError("The game class must derive off of class type 'Game'.")
        self.__active_scene: Scene


class Scene:
    def __init__(self):
        pass