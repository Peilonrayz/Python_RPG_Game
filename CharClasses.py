import random
import math as m
import json
import ItemClasses as Item

def SPrint(string, n):
    return " "*(n-len(string))+string
def RPrint(string, n):
    return string+" "*(n-len(string))

class EntityBase(object):#Character
    def __init__(self, data):
        #data
        self.baseStrength = data["str"]
        self.baseAgility = data["agi"]
        self.baseIntellect = data["int"]
        self.strength = data["str"]
        self.agility = data["agi"]
        self.intellect = data["int"]

        self.gender = data["Gender"]
        self.name = data["Name"]
        self.slots = {}
        for i in data["Slots"]:
            self.slots[int(i)] = Item.Make(data["Slots"][i], self)
        
        self.maxHealth = 0
        self.UpdateHP()
        """
        strength:
            More health. (Done)
            More health regeneration. (Done)
            More attack with melee weppons.
        agility:
            More speed. (Done)
            More attack with ranged weppons. (fast/small wepons aka ranged + Dagger + Claw)
            More critical hit chance.
        intellect:
            More mana.
            More mana regeneration.
            More attack with spells.
            More spell critical hit chance.
        """

    def __str__(self):
        slots = {}
        for i in self.slots:
            slots[i] = self.slots[i].get()
        return json.dumps({"str": self.baseStrength, "agi": self.baseAgility, "int": self.baseIntellect, "Gender":self.gender, "Name": self.name, "Slots": slots, "Health": self.health})
    def get(self):
        slots = {}
        for i in self.slots:
            slots[i] = self.slots[i].get()
        return {"str": self.baseStrength, "agi": self.baseAgility, "int": self.baseIntellect, "Gender":self.gender, "Name": self.name, "Slots": slots, "Health": self.health}

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
        except:pass#print "Error on slot 0"
        try:dmg += self.AdditionalDamage(self.slots[1], self.slots[1].Damage(1))
        except:pass#print "Error on slot 1"
        dmg = int(dmg*(self.health/float(self.maxHealth)))
        other.TakeDamage(dmg)
    def Speed(self):
        return (float(self.health) / self.maxHealth) * self.agility
    def PHealth(self):
        return str(self.health) + "/" + str(self.maxHealth)

    def UpdateHP(self):
        r = int(self.strength**(m.e-1.5)/2)-self.maxHealth
        self.maxHealth += r
        self.healthRegen = int(self.strength**(m.e-2)/2)
        return r
    def EndOfTurnHeal(self):
        self.health += self.healthRegen
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def EquipWeppon(self, item, slot=True):#Slot: True == 0, False == 1 aka True = RHand, False = LHand
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
                
    def Equip(self, item):
        if self.equiped[item.placement] == None:
            self.equiped[item.placement] = item
        else:
            self.inventory.append(self.equiped[item.placement])
            self.equiped[item.placement] = item

class Player(EntityBase):
    def __init__(self, data):
        super(Player, self).__init__(data)
        
        self.gold = data["Gold"]
        self.inventory = {}
        for i in data["Inventory"]:
            self.inventory[int(i)] = Item.Make(data["Inventory"][i], self)
        
        self.exp = data["EXP"]
        self.level = 1
        self.level += self.Level()
        self.health = data["Health"]
        """
        Max uint16 lvl =  47
        Max uint32 lvl =  2828
        Max uint64 lvl =  9894624
        """
    def __str__(self):
        data = super(Player, self).get()
        inv = {}
        if len(self.inventory):
            for i in self.inventory:
                inv[i] = self.inventory[i].get()
        data.update({"Gold": self.gold, "Inventory": inv, "EXP": self.exp})
        return json.dumps(data)
        
        
    def CanFlee(self, other):
        return other.Speed() < self.Speed()

    def Level(self):
        l = self.level
        #((2^(x+2))-((x-2)^2))/(((2^x)/(x^2)))
        """
        First:
        (2^x)-(x^2)
        (2^(x+2))-((x-2)^2)
        ((2^(x+2))-((x-2)^2))/(((2^x)/(x^2)))
        Second:
        (2^x)-(x^2)
        (2^(x+4))-((x+4)^2)
        ((2^(x+4))-((x+4)^2))/(((2^x)/(x^2)))
        Third:
        (e^x)-(x^e)
        ((e^(x+e))-((x+e)^e))
        (((e^(x+e))-((x+e)^e)))/(((e^x)/(x^e)))
        (((e^(x+e))-((x+e)^e)))/((e^(pi-1))*(((e^x)/(x^e))))
        Normal:
        (e^(x+e)-(x+e)^e)/(e^(pi-1)*e^x/x^e)
        Python:
        (e**(x+e)-(x+e)**e)/(e**(pi-1)*e**x/x**e)
        More Levels:
        -x**e*(e**(1-x-pi)*(x+e)**e-e**(1+e-pi))
        MAX: 1800000
        """
        while self.exp > -l**m.e*(m.e**(1-l-m.pi)*(l+m.e)**m.e-m.e**(1+m.e-m.pi)):l += 1
        return l - 1
    
    def GainExp(self, other):
        exp = other.GetExp(self)
        self.exp += exp
        print "Gained %i EXP!"%exp
        level = self.Level()
        if self.level != level:
            self.LevelUp(level - self.level)

    def LevelUp(self, levelDif):
        self.level += levelDif
        print "Leveled up to %i!"%self.level
        self.strength += (2*levelDif)
        self.agility += (2*levelDif)
        self.intellect += (2*levelDif)
        self.baseStrength += (2*levelDif)
        self.baseAgility += (2*levelDif)
        self.baseIntellect += (2*levelDif)
        hpGain = self.UpdateHP()
        self.health = self.maxHealth
        print "Max. HP  "+SPrint("+"+str(hpGain), 4)+SPrint(str(self.maxHealth), 6)
        print "Agility  "+SPrint("+"+str(2*levelDif), 4)+SPrint(str(self.agility), 6)
        print "Strength "+SPrint("+"+str(2*levelDif), 4)+SPrint(str(self.strength), 6)
        print "intellect"+SPrint("+"+str(2*levelDif), 4)+SPrint(str(self.intellect), 6)

class Barbarian(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 31, 'Inventory': {}, 'Name': 'Mr. Barbra', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'Bloody Sword', 'Range': [70, 110], 'Weppon': 2, 'agi': 0, 'int': 0, 'str': 5}, 1: {'2H': False, 'Damage': 5, 'Name': 'HAxer', 'Range': [70, 110], 'Weppon': 0, 'agi': 0, 'int': 0, 'str': 5}}, 'agi': 10, 'int': 10, 'str': 20}
        super(Barbarian, self).__init__(data)

class Hunter(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 8, 'Inventory': {}, 'Name': 'Pet Keeper', 'Slots': {0: {'2H': True, 'Damage': 10, 'Name': 'Where\'s pet', 'Range': [70, 110], 'Weppon': 6, 'agi': 10, 'int': 0, 'str': 0}}, 'agi': 20, 'int': 10, 'str': 10}
        super(Hunter, self).__init__(data)

class Wizard(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 8, 'Inventory': {}, 'Name': 'Gandalf', 'Slots': {0: {'2H': True, 'Damage': 10, 'Name': 'U Shall Not Pass', 'Range': [70, 110], 'Weppon': 11, 'agi': 0, 'int': 10, 'str': 0}}, 'agi': 10, 'int': 20, 'str': 10}
        super(Wizard, self).__init__(data)

class Rouge(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 19, 'Inventory': {}, 'Name': 'Shadow Dealer', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'Sneaky', 'Range': [70, 110], 'Weppon': 4, 'agi': 5, 'int': 0, 'str': 0}, 1: {'2H': False, 'Damage': 5, 'Name': 'Skillz', 'Range': [70, 110], 'Weppon': 4, 'agi': 0, 'int': 0, 'str': 5}}, 'agi': 15, 'int': 10, 'str': 15}
        super(Rouge, self).__init__(data)

class Monk(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 8, 'Inventory': {}, 'Name': 'Faith', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'One Palm', 'Range': [70, 110], 'Weppon': 5, 'agi': 5, 'int': 0, 'str': 0}, 1: {'2H': False, 'Damage': 5, 'Name': 'Two Palm', 'Range': [70, 110], 'Weppon': 5, 'agi': 0, 'int': 5, 'str': 0}}, 'agi': 15, 'int': 15, 'str': 10}
        super(Monk, self).__init__(data)

class Paladin(Player):
    def __init__(self, data=None):
        if data == None:
            data = {'EXP': 0, 'Gender': 'Male', 'Gold': 0, 'Health': 19, 'Inventory': {}, 'Name': '...', 'Slots': {0: {'2H': False, 'Damage': 10, 'Name': '...', 'Range': [70, 110], 'Weppon': 2, 'agi': 0, 'int': 5, 'str': 5}}, 'agi': 10, 'int': 15, 'str': 15}
        super(Paladin, self).__init__(data)



class Mobile(EntityBase):
    def __init__(self, data):
        super(Mobile, self).__init__(data)
        self.experience = data["Experience"]
        self.health = self.maxHealth
    def GetExp(self, other):
        e = ((self.strength+self.agility+self.intellect)-40)/6
        "x^(e-2.3)*y^(e-2.3)*12"
        e = int(other.level**(m.e-2.3)*[e if e>0 else 1][0]**(m.e-2.3)*12)
        e = (random.randrange(90, 110) * (e+self.experience))/100
        return e if e > 0 else 1

class Ork(Mobile):
    def __init__(self, name="Orkie", data=None):
        if data == None:
            data = {'str': 15, 'agi': 15, 'int': 15, 'Gender': 'Male', 'Inventory': {}, 'Slots': {0: {'Weppon': 2, 'agi': 0, 'int': 0, 'Damage': 5, 'Range': [70, 110], 'str': 0, '2H': False, 'Name': 'OrkSword'}}, "Experience": 0}
        data["Name"] = name
        super(Ork, self).__init__(data)

class Troll(Mobile):
    def __init__(self, name="Trollbate", data=None):
        if data == None:
            data = {'str': 30, 'agi': 15, 'int': 15, 'Gender': 'Male', 'Inventory': {}, 'Slots': {0: {'Weppon': 1, 'agi': 0, 'int': 0, 'Damage': 10, 'Range': [70, 110], 'str': 0, '2H': True, 'Name': 'TrollSword'}}, "Experience": 150}
        data["Name"] = name
        super(Troll, self).__init__(data)

#p = Rouge({u'Gold': 0, u'str': 15, u'agi': 15, u'int': 10, u'Gender': u'Female', u'Inventory': {}, u'Slots': {u'0': {u'Weppon': 0, u'agi': 0, u'int': 0, u'Damage': 90, u'Range': [0.7, 1.1], u'str': 0, u'2H': True, "Name":"Axxy"}}, u'Class': u'Roug', u'Name': u'Peilonrayz'})
#print p
if __name__ == "__main__":
    if False:
        print Barbarian()
        print Hunter()
        print Wizard()
        print Rouge()
        print Monk()
        print Paladin()

    p = Rouge({'EXP': 5000, 'Gender': 'Female', 'Gold': 0, 'Health': 19, 'Inventory': {}, 'Name': 'Peilonrayz', 'Slots': {0: {'2H': False, 'Damage': 5, 'Name': 'Sneaky', 'Range': [70, 110], 'Weppon': 4, 'agi': 5, 'int': 0, 'str': 0}, 1: {'2H': False, 'Damage': 5, 'Name': 'Skillz', 'Range': [70, 110], 'Weppon': 4, 'agi': 0, 'int': 0, 'str': 5}}, 'agi': 15, 'int': 10, 'str': 15})
    i = Item.Make({'Range': [70, 110], 'Armour': 2, 'agi': 0, 'int': 0, 'str': 0, 'Defence': 10, 'Name': 'Helm'}, p)
    p.slots[i.placement] = i
    print type(i)
    print i
    print type(p)
    print p
    print p.level
