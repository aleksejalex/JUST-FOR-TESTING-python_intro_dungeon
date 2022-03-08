from abstract_classes import Creature


class Hero(Creature):
    object_type = "hero"

    def __init__(self, identifier, name):
        super().__init__(identifier)
        self.name = name
        self.max_hp = 20
        self.hp = 20
        self.base_ac = 5
        self.base_attack = 3
        self.max_stamina = 20
        self.stamina = 20
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.position = [1, 1]

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.max_hp += 5

    def rest(self):
        self.hp = self.max_hp
        self.stamina = self.max_stamina

    def attack(self):
        pass

