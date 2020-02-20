import json
import random
from mixin import Mixin
from typing import Tuple


class Item(Mixin):
    strength: int = 'str'
    agility: int = 'agi'
    intellect: int = 'int'
    name: str = 'Name'
    range: Tuple[int, int] = 'Range'
    two_h: bool = '2H'
    primary_attribute: str = 'primary_attribute'
    type: Tuple[str, str] = 'type'

    def __init__(self):
        self.given = False

    def __str__(self):
        return json.dumps(self.to_external())

    def get(self):
        return self.to_external()

    def add_stats(self, entity):
        entity.strength += self.strength
        entity.agility += self.agility
        entity.intellect += self.intellect

    def remove_stats(self, entity):
        entity.strength -= self.strength
        entity.agility -= self.agility
        entity.intellect -= self.intellect

    def equip(self, other):
        if other is not None:
            self.add_stats(other)
            self.given = True


class Armour(Item):
    defence: int = 'Defence'

    def protection(self):
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.defence)/100.


class Weapon(Item):
    dmg: int = 'Damage'

    def damage(self, s):
        if s == 1 and self.two_h:
            return 0
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.dmg)/100.


if __name__ == '__main__':
    v = {
        'str': 5,
        'agi': 5,
        'int': 0,
        'Name': 'OrkHelm',
        'Range': [70, 110],
        '2H': False,
        'primary_attribute': 'str',
        'type': ('Armour', 2),
        'Defence': 10
    }
    h = Armour.from_external(v)
    print('h', h)
    print('h.type', h.type)
    print('h.protection()', h.protection())
    j = Armour.from_external(v)
    k = Armour.from_external(v)
    # TODO: fix equality check
    print(h == j)
    print(j == k)
    print(k == h)
