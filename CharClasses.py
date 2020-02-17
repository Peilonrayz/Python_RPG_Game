import random
import math as m
import json
import ItemClasses as Item
from .mixin import Mixin


def s_print(string, n):
    return ' '*(n-len(string))+string


def r_print(string, n):
    return string+' '*(n-len(string))


class Inventory(list):
    pass


class LevelMixin(Mixin):
    exp: int = 'exp'

    def __init__(self):
        self._exp = 0
        self._level = 0

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, exp):
        self._exp = exp
        self._level = 1

    @property
    def level(self):
        return self._level



class EntityBase:
    baseStrength: int = 'str'
    baseAgility: int = 'agi'
    baseIntellect: int = 'int'
    strength: int = 'str'
    agility: int = 'agi'
    intellect: int = 'int'
    gender: str = 'Gender'
    name: str = 'Name'

    def __init__(self, data):
        self.inventory = Inventory()
        self.equipped = []

        self.slots = {}
        for i in data['Slots']:
            j = Item.make(data['Slots'][i])
            self.slots[int(i)] = j

        self.max_health = 0
        self.health_regen = 0
        self.update_hp()

    def __str__(self):
        slots = {}
        for i in self.slots:
            slots[i] = self.slots[i].get()
        return json.dumps({'str': self.baseStrength, 'agi': self.baseAgility, 'int': self.baseIntellect, 'Gender':self.gender, 'Name': self.name, 'Slots': slots, 'Health': self.health})

    def get(self):
        slots = {}
        for i in self.slots:
            slots[i] = self.slots[i].get()
        return {'str': self.baseStrength, 'agi': self.baseAgility, 'int': self.baseIntellect, 'Gender':self.gender, 'Name': self.name, 'Slots': slots, 'Health': self.health}

    def take_damage(self, damage):
        try:
            if self.slots[1].type == Item.Sheild:
                damage -= self.slots[1].protection()
        except:
            pass
        for i in range(2, 14, 1):  #Armour slots
            try:
                damage -= self.slots[i].protection()
            except:
                pass
        damage = int(damage)
        if damage < 0:
            damage = 0
        self.health -= damage

    def additional_damage(self, item, damage):
        attr = item.primary_attribute
        if attr == 'strength':
            stat = self.strength
        elif attr == 'agility':
            stat = self.agility
        elif attr == 'intellect':
            stat = self.intellect
        else:
            return 0
        return int((1+(random.randrange(90, 111, 1)*stat)/10000.)*damage)
    
    def fight(self, other):
        dmg = 0
        try:
            dmg += self.additional_damage(self.slots[0], self.slots[0].damage(0))
        except:
            pass  #print 'Error on slot 0'
        try:
            dmg += self.additional_damage(self.slots[1], self.slots[1].damage(1))
        except:
            pass  #print 'Error on slot 1'
        dmg = int(dmg * (self.health / float(self.max_health)))
        other.take_damage(dmg)

    def speed(self):
        return (float(self.health) / self.max_health) * self.agility

    def p_health(self):
        return str(self.health) + '/' + str(self.max_health)

    def update_hp(self):
        r = int(self.strength**(m.e-1.5)/2)-self.max_health
        self.max_health += r
        self.health_regen = int(self.strength ** (m.e - 2) / 2)
        return r

    def end_of_turn_heal(self):
        self.health += self.health_regen
        if self.health > self.max_health:
            self.health = self.max_health

    def equip_weapon(self, item, slot=True):  #Slot: True == 0, False == 1 aka True = RHand, False = LHand
        if item.twoH:
            changed = 0
            if self.equipped[0] is not None:
                self.inventory.append(self.equipped[0])
                changed += 1
            if self.equipped[1] is not None:
                self.inventory.append(self.equipped[1])
                changed += 1
            if changed == 2 and self.inventory[-2] == self.inventory[-1]:
                self.inventory.pop()
            self.equipped[0] = item
            self.equipped[1] = item
        else:
            if self.equipped[0] is not None:
                self.equipped[1] = item
            elif self.equipped[1] is not None:
                self.equipped[1] = item
            else:
                if slot:
                    self.inventory.append(self.equipped[0])
                    if self.equipped[0] == self.equipped[1]:
                        self.equipped[1] = None
                    self.equipped[0] = item
                else:
                    self.inventory.append(self.equipped[1])
                    if self.equipped[0] == self.equipped[1]:
                        self.equipped[0] = None
                    self.equipped[1] = item

    def check_slot(self, item, slot):
        if item.placement != slot:
            return item.placement in [0, 12] and item.placement + 1 == slot
        return True
    
    def equip(self, item, slot):
        if not self.check_slot(item, slot):
            return 1
        if self.equipped[slot] is None:
            self.equipped[slot] = item
            return 0
        else:
            return 2

    def un_equip(self, slot):
        if self.equipped[slot] is None:
            return 2
        else:
            self.inventory.append(self.equipped[slot])
            self.equipped[slot] = item
            return 0


class Player(EntityBase):
    gold: int = 'Gold'
    exp: int = 'EXP'
    health: int = 'Health'

    def __init__(self, data):
        super(Player, self).__init__(data)

        for i in data['Inventory']:
            self.inventory[int(i)] = Item.make(data['Inventory'][i])

        self.level = 1
        self.level += self.get_level()

    def __str__(self):
        data = super(Player, self).get()
        inv = {}
        if len(self.inventory):
            for i in self.inventory:
                inv[i] = self.inventory[i].get()
        data.update({'Gold': self.gold, 'Inventory': inv, 'EXP': self.exp})
        return json.dumps(data)

    def can_flee(self, other):
        return other.speed() < self.speed()

    def get_level(self):
        l = self.level
        while self.exp > -l**m.e*(m.e**(1-l-m.pi)*(l+m.e)**m.e-m.e**(1+m.e-m.pi)):
            l += 1
        return l - 1
    
    def gain_exp(self, other):
        exp = other.get_exp(self)
        self.exp += exp
        print('Gained %i EXP!' % exp)
        level = self.get_level()
        if self.level != level:
            self.level_up(level - self.level)

    def level_up(self, level_dif):
        self.level += level_dif
        print('Leveled up to %i!'%self.level)
        self.strength += (2 * level_dif)
        self.agility += (2 * level_dif)
        self.intellect += (2 * level_dif)
        self.baseStrength += (2 * level_dif)
        self.baseAgility += (2 * level_dif)
        self.baseIntellect += (2 * level_dif)
        hp_gain = self.update_hp()
        self.health = self.max_health
        print('Max. HP  ' + s_print('+' + str(hp_gain), 4) + s_print(str(self.max_health), 6))
        print('Agility  ' + s_print('+' + str(2 * level_dif), 4) + s_print(str(self.agility), 6))
        print('Strength ' + s_print('+' + str(2 * level_dif), 4) + s_print(str(self.strength), 6))
        print('intellect' + s_print('+' + str(2 * level_dif), 4) + s_print(str(self.intellect), 6))


class Mobile(EntityBase):
    experience: int = 'Experience'

    def __init__(self, data):
        super(Mobile, self).__init__(data)
        self.experience = data['Experience']
        self.health = self.max_health

    def get_exp(self, other):
        e = ((self.strength+self.agility+self.intellect)-40)/6
        'x^(e-2.3)*y^(e-2.3)*12'
        e = int(other.level**(m.e-2.3)*[e if e > 1 else 1][0]**(m.e-2.3)*12)
        e = (random.randrange(90, 110) * (e+self.experience))/100+1
        return e


class Ork(Mobile):
    def __init__(self, name='Orkie', data=None):
        if data == None:
            data = {'str': 15, 'agi': 15, 'int': 15, 'Gender': 'Male', 'Inventory': {}, 'Slots': {0: {'Weapon': 2, 'agi': 0, 'int': 0, 'Damage': 5, 'Range': [70, 110], 'str': 0, '2H': False, 'Name': 'OrkSword'}}, 'Experience': 0}
        data['Name'] = name
        super(Ork, self).__init__(data)


class Troll(Mobile):
    def __init__(self, name='Trollbate', data=None):
        if data == None:
            data = {'str': 30, 'agi': 15, 'int': 15, 'Gender': 'Male', 'Inventory': {}, 'Slots': {0: {'Weapon': 1, 'agi': 0, 'int': 0, 'Damage': 10, 'Range': [70, 110], 'str': 0, '2H': True, 'Name': 'TrollSword'}}, 'Experience': 150}
        data['Name'] = name
        super(Troll, self).__init__(data)


if __name__ == '__main__':
    player = Player({'EXP': 5000, 'Gender': 'Female', 'Gold': 0, 'Health': 19, 'Inventory': {}, 'Name': 'Peilonrayz', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'Sneaky', 'Range': [70, 110], 'Weapon': 4, 'agi': 5, 'int': 0, 'str': 0}, 1: {'2H': False, 'Damage': 5, 'Name': 'Skillz', 'Range': [70, 110], 'Weapon': 4, 'agi': 0, 'int': 0, 'str': 5}}, 'agi': 15, 'int': 10, 'str': 15})
    item = Item.make({'Range': [70, 110], 'Armour': 2, 'agi': 0, 'int': 0, 'str': 0, 'Defence': 10, 'Name': 'Helm', '2H': False})
    player.slots[item.type[1]] = item
