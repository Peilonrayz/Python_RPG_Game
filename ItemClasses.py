import json
import random


class Item:
    def __init__(self, data):
        self.given = False
        self.strength = data['str']
        self.agility = data['agi']
        self.intellect = data['int']
        self.name = data['Name']
        self.range = data['Range']
        self.two_h = data['2H']
        self.primary_attribute = 'strength'

    def __type__(self):
        return self.type

    def __str__(self):
        return json.dumps({'str': self.strength, 'agi': self.agility, 'int': self.intellect, 'Name': self.name, 'Range': self.range, '2H': self.two_h, self.type[0]: self.type[1]})

    def get(self):
        return {'str': self.strength, 'agi': self.agility, 'int': self.intellect, 'Name': self.name, 'Range': self.range, '2H': self.two_h}

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
    def __init__(self, data):
        super(Armour, self).__init__(data)
        self.defence = data['Defence']
        self.type = ('Armour', data['Armour'])

    def __str__(self):
        data = super(Armour, self).get()
        data.update({'Defence': self.defence})
        return json.dumps(data)

    def get(self):
        data = super(Armour, self).get()
        data.update({'Defence': self.defence})
        return data

    def protection(self):
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.defence)/100.


class Weapon(Item):
    def __init__(self, data):
        super(Weapon, self).__init__(data)
        self.placement = 0
        self.damage = data['Damage']
        self.type = ('Weapon', data['Weapon'])
        
    def __str__(self):
        data = super(Weapon, self).get()
        data.update({'Damage': self.damage})
        return json.dumps(data)

    def get(self):
        data = super(Weapon, self).get()
        data.update({'Damage': self.damage})
        return data

    def damage(self, s):
        if s == 1 and self.two_h:
            return 0
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.damage)/100.


def make(data):
    if 'Armour' in data:
        return Armour(data)
    elif 'Weapon' in data:
        return Weapon(data)
    return None


if __name__ == '__main__':
    h = make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    print(h)
    print(type(h))
    print(h.protection())
    j = make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    k = make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    print(h == j)
    print(j == k)
    print(k == h)
