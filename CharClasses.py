import random
import math as m
import json
import ItemClasses as Item

def SPrint(string, n):
    return ' '*(n-len(string))+string
def RPrint(string, n):
    return string+' '*(n-len(string))

class EntityBase(object):
    def __init__(self, data):
        self.baseStrength = data['str']
        self.baseAgility = data['agi']
        self.baseIntellect = data['int']
        self.strength = data['str']
        self.agility = data['agi']
        self.intellect = data['int']

        self.gender = data['Gender']
        self.name = data['Name']
        self.slots = {}
        for i in data['Slots']:
            j = Item.Make(data['Slots'][i])
            self.slots[int(i)] = j
        
        self.maxHealth = 0
        self.UpdateHP()

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

    def TakeDamage(self, damage):
        try:
            if type(self.slots[1]) == Item.Sheild:damage -= self.slots[1].Protection()
        except:pass
        for i in xrange(2, 14, 1):#Armour slots
            try:damage -= self.slots[i].Protection()
            except:pass
        damage = int(damage)
        if damage < 0: damage = 0
        self.health -= damage

    def AdditionalDamage(self, item, damage):
        if type(item) in [Item.Axe, Item.Mace, Item.Sword, Item.Spear]:
            return int((1+(random.randrange(90, 111, 1)*self.strength)/10000.)*damage)
        if type(item) in [Item.Dagger, Item.Claw, Item.Bow, Item.Crossbow, Item.Gun, Item.Thrown]:
            return int((1+(random.randrange(90, 111, 1)*self.agility)/10000.)*damage)
        if type(item) in [Item.Wand, Item.Staff]:
            return int((1+(random.randrange(90, 111, 1)*self.intellect)/10000.)*damage)
    
    def Fight(self, other):
        dmg = 0
        try:dmg += self.AdditionalDamage(self.slots[0], self.slots[0].Damage(0))
        except:pass#print 'Error on slot 0'
        try:dmg += self.AdditionalDamage(self.slots[1], self.slots[1].Damage(1))
        except:pass#print 'Error on slot 1'
        dmg = int(dmg*(self.health/float(self.maxHealth)))
        other.TakeDamage(dmg)
    def Speed(self):
        return (float(self.health) / self.maxHealth) * self.agility
    def PHealth(self):
        return str(self.health) + '/' + str(self.maxHealth)

    def UpdateHP(self):
        r = int(self.strength**(m.e-1.5)/2)-self.maxHealth
        self.maxHealth += r
        self.healthRegen = int(self.strength**(m.e-2)/2)
        return r
    def EndOfTurnHeal(self):
        self.health += self.healthRegen
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def EquipWeapon(self, item, slot=True):#Slot: True == 0, False == 1 aka True = RHand, False = LHand
        if item.twoH:
            changed = 0
            if self.equiped[0] != None:
                self.inventory.append(self.equiped[0])
                changed += 1
            if self.equiped[1] != None:
                self.inventory.append(self.equiped[1])
                changed += 1
            if changed == 2 and self.inventory[-2] == self.inventory[-1]:
                self.inventory.pop()
            self.equiped[0] = item
            self.equiped[1] = item
        else:
            if self.equiped[0] == None:
                self.equiped[1] = item
            elif self.equiped[1] == None:
                self.equiped[1] = item
            else:
                if slot:
                    self.inventory.append(self.equiped[0])
                    if self.equiped[0] == self.equiped[1]:
                        self.equiped[1] = None
                    self.equiped[0] = item
                else:
                    self.inventory.append(self.equiped[1])
                    if self.equiped[0] == self.equiped[1]:
                        self.equiped[0] = None
                    self.equiped[1] = item

    def CkeckSlot(self, item, slot):
        if item.placement != slot:
            if item.placement in [0, 12]:
                if item.placement + 1 != slot:
                    return False
            else:return False
        return True
    
    def Equip(self, item, slot):
        if not CkeckSlot(self, item, slot):
            return 1
        if self.equiped[slot] == None:
            self.equiped[slot] = item
            return 0
        else:
            return 2

    def UnEquip(self, slot):
        if self.equiped[slot] == None:
            return 2
        else:
            self.inventory.append(self.equiped[slot])
            self.equiped[slot] = item
            return 0

class Player(EntityBase):
    def __init__(self, data):
        super(Player, self).__init__(data)
        
        self.gold = data['Gold']
        self.inventory = {}
        for i in data['Inventory']:
            self.inventory[int(i)] = Item.Make(data['Inventory'][i])
        
        self.exp = data['EXP']
        self.level = 1
        self.level += self.Level()
        self.health = data['Health']
    def __str__(self):
        data = super(Player, self).get()
        inv = {}
        if len(self.inventory):
            for i in self.inventory:
                inv[i] = self.inventory[i].get()
        data.update({'Gold': self.gold, 'Inventory': inv, 'EXP': self.exp})
        return json.dumps(data)
        
        
    def CanFlee(self, other):
        return other.Speed() < self.Speed()

    def Level(self):
        l = self.level
        while self.exp > -l**m.e*(m.e**(1-l-m.pi)*(l+m.e)**m.e-m.e**(1+m.e-m.pi)):l += 1
        return l - 1
    
    def GainExp(self, other):
        exp = other.GetExp(self)
        self.exp += exp
        print 'Gained %i EXP!'%exp
        level = self.Level()
        if self.level != level:
            self.LevelUp(level - self.level)

    def LevelUp(self, levelDif):
        self.level += levelDif
        print 'Leveled up to %i!'%self.level
        self.strength += (2*levelDif)
        self.agility += (2*levelDif)
        self.intellect += (2*levelDif)
        self.baseStrength += (2*levelDif)
        self.baseAgility += (2*levelDif)
        self.baseIntellect += (2*levelDif)
        hpGain = self.UpdateHP()
        self.health = self.maxHealth
        print 'Max. HP  '+SPrint('+'+str(hpGain), 4)+SPrint(str(self.maxHealth), 6)
        print 'Agility  '+SPrint('+'+str(2*levelDif), 4)+SPrint(str(self.agility), 6)
        print 'Strength '+SPrint('+'+str(2*levelDif), 4)+SPrint(str(self.strength), 6)
        print 'intellect'+SPrint('+'+str(2*levelDif), 4)+SPrint(str(self.intellect), 6)

class Mobile(EntityBase):
    def __init__(self, data):
        super(Mobile, self).__init__(data)
        self.experience = data['Experience']
        self.health = self.maxHealth
    def GetExp(self, other):
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
    p = Player({'EXP': 5000, 'Gender': 'Female', 'Gold': 0, 'Health': 19, 'Inventory': {}, 'Name': 'Peilonrayz', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'Sneaky', 'Range': [70, 110], 'Weapon': 4, 'agi': 5, 'int': 0, 'str': 0}, 1: {'2H': False, 'Damage': 5, 'Name': 'Skillz', 'Range': [70, 110], 'Weapon': 4, 'agi': 0, 'int': 0, 'str': 5}}, 'agi': 15, 'int': 10, 'str': 15})
    i = Item.Make({'Range': [70, 110], 'Armour': 2, 'agi': 0, 'int': 0, 'str': 0, 'Defence': 10, 'Name': 'Helm', '2H': False})
    p.slots[i.type[1]] = i
