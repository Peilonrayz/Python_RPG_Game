import CharClasses as Class
import ItemClasses as Item
import FightClasses as Fight

import json

class Menu(object):
    def __init__(self):
        pass
    def Load(self, name):
        with open(name, "r") as f:
            data = json.loads(f.read())
        if data["Class"] == "Barb":self.Player = Class.Barbarian(data)
        if data["Class"] == "Hunt":self.Player = Class.Hunter(data)
        if data["Class"] == "Wiza":self.Player = Class.Wizard(data)
        if data["Class"] == "Roug":self.Player = Class.Rouge(data)
        if data["Class"] == "Monk":self.Player = Class.Monk(data)
        if data["Class"] == "Pala":self.Player = Class.Paladin(data)
    def Save(self, name):
        with open(name, "w") as f:
            f.write(str(self.player))

hero = Class.Rouge()
print hero
o = {'str': 15, 'agi': 15, 'int': 15, 'Gender': 'Male', 'Inventory': {}, 'Slots': {0: {'Weppon': 2, 'agi': 5, 'int': 0, 'Damage': 5, 'Range': [70, 110], 'str': 0, '2H': False, 'Name': 'OrkSword'}, 2: {'Armour': 2, 'agi': 0, 'int': 0, 'Defence': 2, 'Range': [70, 110], 'str': 0, '2H': False, 'Name': 'OrkHealm'}}, "Experience": 0}
ork = Class.Ork("OrkyOrk", o)
if Fight.Fight([hero], [ork]).Won():
    print "Beat the Measly Ork!"



