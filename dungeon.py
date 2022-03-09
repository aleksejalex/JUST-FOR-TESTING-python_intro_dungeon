from abstract_classes import DungeonInterface
import random
from datetime import datetime
from copy import deepcopy
from map_entities import Hero, Goblin


class Dungeon(DungeonInterface):

    def __init__(self, size: tuple, tunnels_number: int, hero_name: str):
        super().__init__(size)
        self.hero = Hero(identifier="@", position=[1, 1], name=hero_name, base_attack=5, base_ac=3, damage=1)
        self.size = size
        self.tunnels_number = tunnels_number
        self.entities = []
        self.actual_dungeon_map = []
        self.empty_space = []
        self.starting_entities = ["goblin", "goblin"]
        self.fighting = False
        self.message = ""

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
                if actual_position != [1, 1]:
                    self.empty_space.append(tuple(actual_position[:]))
        self.empty_space = list(map(list, set(self.empty_space)))
        self.dungeon_map[1][1] = "."
        self.place_entities()
        self.actual_dungeon_map = deepcopy(self.dungeon_map[:])
        self.actual_dungeon_map[1][1] = "@"

    def place_entities(self):
        positions = random.sample(self.empty_space, len(self.starting_entities))
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(Goblin(identifier="\033[38;5;1mg\033[0;0m", position=positions[idx], base_attack=-1, base_ac=0, damage=1))
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

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
        elif action == "A":
            self.fighting = False
            for entity in self.entities:
                if self.hero.position == entity.position:
                    if hasattr(entity, "attack"):
                        self.message = "Fight!"
                        self.fighting = True
                        self.fight(entity)
            if not self.fighting:
                self.message = "Your big sword is hitting air really hard!"
        self.update_map([])
        if self.hero.hp < 1:
            exit(0)

    def update_map(self, entities):
        self.actual_dungeon_map = deepcopy(self.dungeon_map)
        self.actual_dungeon_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier

    def fight(self, monster):
        hero_roll = self.hero.attack()
        monster_roll = monster.attack()
        if hero_roll["attack_roll"] > monster.base_ac:
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                self.message = "Hero inflicted {} damage".format(hero_roll["inflicted_damage"])
            else:
                self.message = "Hero inflicted {} damage and slain {}".format(hero_roll["inflicted_damage"], monster)
                self.hero.gold += monster.gold
                self.hero.xp += 1
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."
                self.entities.remove(monster)

        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.message += "\nMonster inflicted {} damage".format(monster_roll["inflicted_damage"])
            self.hero.hp -= monster_roll["inflicted_damage"]
            if self.hero.hp < 1:
                self.message += "\n{} have been slained by {}".format(self.hero.name, monster)

        self.message += "\nHero HP: {}  Monster HP: {}".format(self.hero.hp, monster.hp)