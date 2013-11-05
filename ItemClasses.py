import inspect
import json
import random

class Item(object):
    def __init__(self, data, enitity):
        self.given = False
        self.strength = data["str"]
        self.agility = data["agi"]
        self.intellect = data["int"]
        self.name = data["Name"]
        self.range = data["Range"]
        if enitity != None:
            self.AddStats(enitity)
            self.given = True

        """
        Wepons:
        
        00 RHand
        01 LHand

        Armour:

        02 Head
        03 Neck
        04 Sholder
        05 Cloak
        06 Chest
        07 Wrist
        08 Hands
        09 Waist
        10 Legs
        11 Feet
        12 Ring1
        13 Ring1
        """
    def __str__(self):
        return json.dumps({"str": self.strength, "agi": self.agility, "int": self.intellect, "Name": self.name, "Range": self.range})
    def get(self):
        return {"str": self.strength, "agi": self.agility, "int": self.intellect, "Name": self.name, "Range": self.range}

    def AddStats(self, enitity):
        enitity.strength += self.strength
        enitity.agility += self.agility
        enitity.intellect += self.intellect

    def RemoveStats(self, enitity):
        enitity.strength -= self.strength
        enitity.agility -= self.agility
        enitity.intellect -= self.intellect

class Armour(Item):
    def __init__(self, data, enitity):
        super(Armour, self).__init__(data, enitity)
        self.defence = data["Defence"]
        
    def __str__(self):
        data = super(Armour, self).get()
        data.update({"Defence": self.defence, "Armour": self.placement})
        return json.dumps(data)
    def get(self):
        data = super(Armour, self).get()
        data.update({"Defence": self.defence, "Armour": self.placement})
        return data

    def Protection(self):
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.defence)/100.

class Head(Armour):
    def __init__(self, data, enitity):
        super(Head, self).__init__(data, enitity)
        self.placement = 2

class Neck(Armour):
    def __init__(self, data, enitity):
        super(Neck, self).__init__(data, enitity)
        self.placement = 3

class Sholder(Armour):
    def __init__(self, data, enitity):
        super(Sholder, self).__init__(data, enitity)
        self.placement = 4

class Cloak(Armour):
    def __init__(self, data, enitity):
        super(Cloak, self).__init__(data, enitity)
        self.placement = 5

class Chest(Armour):
    def __init__(self, data, enitity):
        super(Chest, self).__init__(data, enitity)
        self.placement = 6

class Wrist(Armour):
    def __init__(self, data, enitity):
        super(Wrist, self).__init__(data, enitity)
        self.placement = 7

class Hands(Armour):
    def __init__(self, data, enitity):
        super(Hands, self).__init__(data, enitity)
        self.placement = 8

class Waist(Armour):
    def __init__(self, data, enitity):
        super(Waist, self).__init__(data, enitity)
        self.placement = 9

class Legs(Armour):
    def __init__(self, data, enitity):
        super(Legs, self).__init__(data, enitity)
        self.placement = 10

class Feet(Armour):
    def __init__(self, data, enitity):
        super(Feet, self).__init__(data, enitity)
        self.placement = 11

class Ring(Armour):
    def __init__(self, data, enitity):
        super(Ring, self).__init__(data, enitity)
        self.placement = 12

class Sheild(Armour):
    def __init__(self, data, enitity):
        super(Ring, self).__init__(data, enitity)
        self.placement = 0
        self.twoH = False
    
class Weapon(Item):
    def __init__(self, data, enitity):
        super(Weapon, self).__init__(data, enitity)
        self.placement = 0
        self.twoH = data["2H"]
        self.damage = data["Damage"]
        """
        Str:
            00 Axe
            01 Mace
            02 Sword
            03 Spear
        Agi:
            04 Dagger
            05 Fist Weapon(Claw)
            06 Bow
            07 Crossbow
            08 Gun
            09 Thrown
        Int:
            10 Wand
            11 Staff
        """
    def __str__(self):
        data = super(Weapon, self).get()
        data.update({"2H": self.twoH, "Damage": self.damage, "Weppon": self.type})
        return json.dumps(data)
    def get(self):
        data = super(Weapon, self).get()
        data.update({"2H": self.twoH, "Damage": self.damage, "Weppon": self.type})
        return data

    def Damage(self, s):
        if s == 1 and self.twoH:
            return 0
        return (random.randrange(self.range[0], self.range[1]+1, 1)*self.damage)/100.

class Axe(Weapon):
    def __init__(self, data, enitity):
        super(Axe, self).__init__(data, enitity)
        self.type = 0

class Mace(Weapon):
    def __init__(self, data, enitity):
        super(Mace, self).__init__(data, enitity)
        self.type = 1

class Sword(Weapon):
    def __init__(self, data, enitity):
        super(Sword, self).__init__(data, enitity)
        self.type = 2

class Spear(Weapon):
    def __init__(self, data, enitity):
        super(Spear, self).__init__(data, enitity)
        self.type = 3

class Dagger(Weapon):
    def __init__(self, data, enitity):
        super(Dagger, self).__init__(data, enitity)
        self.type = 4

class Claw(Weapon):
    def __init__(self, data, enitity):
        super(Claw, self).__init__(data, enitity)
        self.type = 5

class Bow(Weapon):
    def __init__(self, data, enitity):
        super(Bow, self).__init__(data, enitity)
        self.type = 6

class Crossbow(Weapon):
    def __init__(self, data, enitity):
        super(Crossbow, self).__init__(data, enitity)
        self.type = 7

class Gun(Weapon):
    def __init__(self, data, enitity):
        super(Gun, self).__init__(data, enitity)
        self.type = 8

class Thrown(Weapon):
    def __init__(self, data, enitity):
        super(Thrown, self).__init__(data, enitity)
        self.type = 9

class Wand(Weapon):
    def __init__(self, data, enitity):
        super(Wand, self).__init__(data, enitity)
        self.type = 10

class Staff(Weapon):
    def __init__(self, data, enitity):
        super(Staff, self).__init__(data, enitity)
        self.type = 11

def Make(data, enitity):
    if type(data) in [Axe, Mace, Sword, Spear, Dagger, Claw, Bow, Crossbow, Gun, Thrown, Wand, Staff, Sheild, Head, Neck, Sholder, Cloak, Chest, Wrist, Hands, Waist, Legs, Feet, Ring]:
        print type(data)
        if not data.given:
            data.AddStats(enitity)
            data.given = True
        return data
    elif "Armour" in list(data):
        if data["Armour"] == 0:return Sheild(data, enitity)
        elif data["Armour"] == 2:return Head(data, enitity)
        elif data["Armour"] == 3:return Neck(data, enitity)
        elif data["Armour"] == 4:return Sholder(data, enitity)
        elif data["Armour"] == 5:return Cloak(data, enitity)
        elif data["Armour"] == 6:return Chest(data, enitity)
        elif data["Armour"] == 7:return Wrist(data, enitity)
        elif data["Armour"] == 8:return Hands(data, enitity)
        elif data["Armour"] == 9:return Waist(data, enitity)
        elif data["Armour"] == 10:return Legs(data, enitity)
        elif data["Armour"] == 11:return Feet(data, enitity)
        elif data["Armour"] == 12:return Ring(data, enitity)
    elif "Weppon" in list(data):
        if data["Weppon"] == 0:return Axe(data, enitity)
        elif data["Weppon"] == 1:return Mace(data, enitity)
        elif data["Weppon"] == 2:return Sword(data, enitity)
        elif data["Weppon"] == 3:return Spear(data, enitity)
        elif data["Weppon"] == 4:return Dagger(data, enitity)
        elif data["Weppon"] == 5:return Claw(data, enitity)
        elif data["Weppon"] == 6:return Bow(data, enitity)
        elif data["Weppon"] == 7:return Crossbow(data, enitity)
        elif data["Weppon"] == 8:return Gun(data, enitity)
        elif data["Weppon"] == 9:return Thrown(data, enitity)
        elif data["Weppon"] == 10:return Wand(data, enitity)
        elif data["Weppon"] == 11:return Staff(data, enitity)
    print "Error!!!"
    print type(data)
    print data
    return None

if __name__ == "__main__":
    h = Make({'Armour': 2, 'agi': 5, 'int': 0, 'Defence': 10, 'Range': [70, 110], 'str': 5, '2H': False, 'Name': 'OrkHealm'}, None)
    print h
    print type(h)
    print h.Protection()
