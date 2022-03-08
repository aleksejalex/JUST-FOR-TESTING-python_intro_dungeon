from abstract_classes import DungeonInterface
import random
from copy import deepcopy
from map_entities import Hero


class Dungeon(DungeonInterface):

    def __init__(self, size: tuple, tunnels_number: int, hero_name: str):
        self.hero = Hero("@", hero_name)
        self.size = size
        self.tunnels_number = tunnels_number
        self.dungeon_map = []
        self.entities = []
        self.actual_dungeon_map = []

    def __str__(self):
        printable_map = ""
        for column in self.actual_dungeon_map:
            for row in column:
                printable_map += row
            printable_map += "\n"
        return printable_map

    def create_dungeon(self):
        for x in range(self.size[0]):
            self.dungeon_map.append([])
            for y in range(self.size[1]):
                self.dungeon_map[x].append("▓")

        actual_position = [1, 1]
        for tunnel in range(self.tunnels_number):
            directions = ["U", "D", "L", "R"]
            # pick random direction
            max_tunnel_length = 0
            while max_tunnel_length == 0:
                direction = random.choice(directions)
                print(direction)
                if direction == "U":
                    if actual_position[0] > 1:
                        max_tunnel_length = actual_position[0] - 1
                elif direction == "D":
                    if actual_position[0] < self.size[0] - 1:
                        max_tunnel_length = self.size[0] - actual_position[0] - 2
                elif direction == "L":
                    if actual_position[1] > 1:
                        max_tunnel_length = actual_position[1] - 1
                elif direction == "R":
                    if actual_position[1] < self.size[1] - 1:
                        max_tunnel_length = self.size[1] - actual_position[1] - 2
            tunnel_length = random.randint(1, max_tunnel_length)
            for x in range(tunnel_length):
                if direction == "U":
                    self.dungeon_map[actual_position[0] - 1][actual_position[1]] = "."
                    actual_position[0] = actual_position[0] - 1
                if direction == "D":
                    self.dungeon_map[actual_position[0] + 1][actual_position[1]] = "."
                    actual_position[0] = actual_position[0] + 1
                if direction == "R":
                    self.dungeon_map[actual_position[0]][actual_position[1] + 1] = "."
                    actual_position[1] = actual_position[1] + 1
                if direction == "L":
                    self.dungeon_map[actual_position[0]][actual_position[1] - 1] = "."
                    actual_position[1] = actual_position[1] - 1
        self.dungeon_map[1][1] = "."
        self.actual_dungeon_map = deepcopy(self.dungeon_map[:])
        self.actual_dungeon_map[1][1] = "@"

    def place_entities(self, entities: list):
        pass

    def hero_action(self, action):
        if action == "R":
            if self.hero.position[1] + 1 < self.size[1] - 1:
                if self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
                    self.hero.position[1] += 1
        elif action == "L":
            if self.hero.position[1] - 1 > 0:
                if self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
                    self.hero.position[1] -= 1
        elif action == "U":
            if self.hero.position[0] - 1 > 0:
                if self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
                    self.hero.position[0] -= 1
        elif action == "D":
            if self.hero.position[0] + 1 < self.size[0] - 1:
                if self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
                    self.hero.position[0] += 1
        self.update_map([])

    def update_map(self, entities):
        self.actual_dungeon_map = deepcopy(self.dungeon_map)

        self.actual_dungeon_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier





