import CharClasses as Class
import ItemClasses as Item
import FightClasses as Fight

import json, os

class Menu(object):
    def __init__(self):
        pass
    def Load(self, name):
        with open('Saves\\'+name+'.rpgsave', "w") as f:
            self.player = Class.Player(f.read())
    def Save(self):
        with open('Saves\\'+self.player.name+'.rpgsave', "w") as f:
            f.write(str(self.player))
    def NewGame(self):
        import NewGame
        self.player = NewGame.SelectHero()
        del NewGame


menu = Menu()
if True:
    menu.NewGame()
    menu.Save()
