import json
import random

class Item(object):
    def __init__(self, data):
        self.given = False
        self.strength = data['str']
        self.agility = data['agi']
        self.intellect = data['int']
        self.name = data['Name']
        self.range = data['Range']
        self.twoH = data['2H']
    def __type__(self):
        return self.type
    def __str__(self):
        return json.dumps({'str': self.strength, 'agi': self.agility, 'int': self.intellect, 'Name': self.name, 'Range': self.range, '2H': self.twoH, self.type[0]: self.type[1]})
    def get(self):
        return {'str': self.strength, 'agi': self.agility, 'int': self.intellect, 'Name': self.name, 'Range': self.range, '2H': self.twoH}

    def AddStats(self, enitity):
        enitity.strength += self.strength
        enitity.agility += self.agility
        enitity.intellect += self.intellect

    def RemoveStats(self, enitity):
        enitity.strength -= self.strength
        enitity.agility -= self.agility
        enitity.intellect -= self.intellect

    def Equip(self, other):
        if other != None:
            self.AddStats(other)
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
    def Protection(self):
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

    def Damage(self, s):
        if s == 1 and self.twoH:
            return 0
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.damage)/100.

def Make(data):
    t = type(data)
    if t == dict:
        if 'Armour' in list(data):
            return Armour(data)
        elif 'Weapon' in list(data):
            return Weapon(data)
    return None

if __name__ == '__main__':
    h = Make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    print h
    print type(h)
    print h.Protection()
    j = Make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    k = Make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'})
    print h == j
    print j == k
    print k == h
