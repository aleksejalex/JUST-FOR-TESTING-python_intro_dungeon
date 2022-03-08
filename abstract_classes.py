import abc


class DungeonInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, size: tuple):
        self.size = size
        self.dungeon_map = []

    @abc.abstractmethod
    def create_dungeon(self):
        """
        Generates dungeon. The size of dungeon is given by tuple self.size.
        Entrance is always located at position (1,1)
        . - empty space
        ▓ - wall
        """
        raise NotImplementedError

    @abc.abstractmethod
    def place_entities(self, entities: list):
        """
        Place entities in list to random places in created dungeon.
        Player is placed into entrance at position (1,1).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def hero_action(self, direction):
        """
        Method to update the position of hero in the map.
        :param direction:
        :return: self.actual_dungeon_map
        """
        raise NotImplementedError

    @abc.abstractmethod
    def update_map(self, entities):
        """
        Update map with new position of entities.
        :param entities:
        :return: self.actual_dungeon_map
        """
        raise NotImplementedError


class Creature(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, identifier: str):
        self.map_identifier = identifier


    def attack(self):
        """

        :return:
        """
        raise NotImplementedError
