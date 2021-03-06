import json
import tkinter


class EntrySection(object):
    def __init__(self, root, data):
        self.Text = tkinter.StringVar()
        self.Label = tkinter.Label(root, textvariable=self.Text)
        self.Text.set(data["text"]["text"])
        self.Label.pack(side=tkinter.LEFT, expand=True)
        self.Label.place(
            x=data["text"]["x"], y=data["y"], height=data["text"]["height"]
        )
        self.Label.visible = True
        self.Box = tkinter.Entry(root, bd=4)
        self.Box.place(
            x=data["box"]["x"],
            y=data["y"],
            width=data["box"]["width"],
            height=data["box"]["height"],
        )
        self.Box.visible = True
        self.Error = tkinter.Entry(root, bd=4)
        self.Error.place(
            x=data["box"]["x"] + data["box"]["width"],
            y=data["y"],
            width=100,
            height=data["box"]["height"],
        )
        self.Error.visible = True

    def Toggle(self):
        if self.Label.visible:
            self.Label.pi = self.Label.place_info()
            self.Label.place_forget()
        else:
            self.Label.place(self.Label.pi)
        self.Label.visible = not self.Label.visible

        if self.Box.visible:
            self.Box.pi = self.Box.place_info()
            self.Box.place_forget()
        else:
            self.Box.place(self.Box.pi)
        self.Box.visible = not self.Box.visible

        if self.Error.visible:
            self.Error.pi = self.Error.place_info()
            self.Error.place_forget()
        else:
            self.Error.place(self.Error.pi)
        self.Error.visible = not self.Error.visible


def DoubleEntrySection(EntrySection):
    def __init__(self, root, data):
        super(DoubleEntrySection, self).__init__(root, data)
        self.RandomBox = tkinter.Entry(root, bd=4)
        self.RandomBox.place(
            x=data["box"]["x"],
            y=data["y"],
            width=data["box"]["width"],
            height=data["box"]["height"],
        )
        self.RandomBox.visible = True
        self.Error2 = tkinter.Entry(root, bd=4)
        self.Error2.place(
            x=data["box"]["x"] + data["box"]["width"],
            y=data["y"],
            width=100,
            height=data["box"]["height"],
        )
        self.Error2.visible = True

    def Toggle(self):
        super(DoubleEntrySection, self).Toggle()


class Button(object):
    def __init__(self, root, data):
        self.Button = tkinter.Button(root, text=data["text"], command=data["func"])
        self.Button.place(x=data["x"], y=data["y"], width=100, height=25)
        self.Button.visible = True

    def Toggle(self):
        if self.Button.visible:
            self.Button.pi = self.Button.place_info()
            self.Button.place_forget()
        else:
            self.Button.place(self.Button.pi)
        self.Button.visible = not self.Button.visible


def IsInt(string):
    try:
        int(string)
        return True
    except:
        return False


def IsFloat(string):
    try:
        float(string)
        return True
    except:
        return False


def IsBool(string):
    try:
        if len(string) == 0:
            return False
        bool(string)
        return True
    except:
        return False


lst = [
    "axe",
    "mace",
    "sword",
    "spear",
    "dagger",
    "claw",
    "bow",
    "crossbow",
    "gun",
    "thrown",
    "wand",
    "staff",
]


def IsWeapon(string):
    s = string.lower()
    s = int(string) if IsInt(string) else string
    for i in range(len(lst)):
        if s == i or s == lst[i]:
            return i, True
    return -1, False


class DisplayMain(object):
    def __init__(self, root, main):
        self.root = root
        self.root.minsize(300, 225)
        self.root.geometry("300x225")
        self.main = main

        self.Name = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Name", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 0,
            },
        )
        self.Str = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Strength", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 25,
            },
        )
        self.Agi = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Agility", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 50,
            },
        )
        self.Int = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Intellect", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 75,
            },
        )
        self.Range = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Damage Range", "height": 25},
                "box": {"x": 100, "width": 50, "height": 25},
                "y": 100,
            },
        )
        self.Range.Error.place(x=200, y=100, width=100, height=25)
        self.Range.Box2 = tkinter.Entry(self.root, bd=4)
        self.Range.Box2.place(x=150, y=100, width=50, height=25)
        self.Range.Box2.visible = True

        self.Make = Button(
            self.root, {"x": 0, "y": 0, "text": "Make", "func": self.MakeHandle}
        )
        self.Back = Button(
            self.root, {"x": 0, "y": 0, "text": "Back", "func": self.Toggle}
        )

    def EditLabel(self, check, data, link, returnData):
        if check(data):
            link.Error.delete(0, "end")
            return True
        else:
            link.Error.delete(0, "end")
            link.Error.insert("end", returnData)
            return False

    def MakeHandle(self):
        data = self.MakeItem()
        if data != False:
            print(data)
            try:
                print(self.path + data["Name"])
                with open(self.path + data["Name"] + "." + self.type, "w") as f:
                    f.write(json.dumps(data, sort_keys=True, separators=(",", ":")))
                    self.Clean()
            except:
                print("Error!!! Nub!")

    def MakeItem(self):
        boolean = True
        name = self.Name.Box.get()
        strength = self.Str.Box.get()
        agility = self.Agi.Box.get()
        intellect = self.Int.Box.get()
        range1 = self.Range.Box.get()
        range2 = self.Range.Box2.get()

        if not self.EditLabel(IsInt, strength, self.Str, "Not a number!"):
            boolean = False
        if not self.EditLabel(IsInt, agility, self.Agi, "Not a number!"):
            boolean = False
        if not self.EditLabel(IsInt, intellect, self.Int, "Not a number!"):
            boolean = False
        if not self.EditLabel(IsFloat, range1, self.Range, "Not a number!"):
            boolean = False
        if not self.EditLabel(IsFloat, range2, self.Range, "Not a number!"):
            boolean = False

        if boolean:
            return {
                "str": int(strength),
                "agi": int(agility),
                "int": int(intellect),
                "Name": name,
                "Range": [float(range1), float(range2)],
            }
        return False

    def Clean(self):
        self.Name.Box.delete(0, "end")
        self.Str.Box.delete(0, "end")
        self.Agi.Box.delete(0, "end")
        self.Int.Box.delete(0, "end")
        self.Range.Box.delete(0, "end")
        self.Range.Box2.delete(0, "end")

    def Toggle(self):
        self.Name.Toggle()
        self.Str.Toggle()
        self.Agi.Toggle()
        self.Int.Toggle()
        self.Range.Toggle()
        self.Make.Toggle()
        self.Back.Toggle()
        self.main.Toggle()

        if self.Range.Box2.visible:
            self.Range.Box2.pi = self.Range.Box2.place_info()
            self.Range.Box2.place_forget()
        else:
            self.Range.Box2.place(self.Range.Box2.pi)
        self.Range.Box2.visible = not self.Range.Box2.visible


class DisplayWeapon(DisplayMain):
    def __init__(self, root, main):
        super(DisplayWeapon, self).__init__(root, main)
        self.Damage = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Damage", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 125,
            },
        )
        self.TwoHand = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Two handed", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 150,
            },
        )
        self.Weapon = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Weapon", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 175,
            },
        )

        self.Make.Button.place(x=100, y=200, width=100, height=25)
        self.Back.Button.place(x=0, y=200, width=100, height=25)

        self.path = "Weapons\\"
        self.type = "weapon"

    def MakeItem(self):
        data = super(DisplayWeapon, self).MakeItem()

        boolean = True
        damage = self.Damage.Box.get()
        twoHand = self.TwoHand.Box.get()
        weapon = self.Weapon.Box.get()

        if not self.EditLabel(IsInt, damage, self.Damage, "Not a number!"):
            boolean = False
        if not self.EditLabel(IsBool, twoHand, self.TwoHand, "Not a bool!"):
            boolean = False
        weapon, boo = IsWeapon(weapon)
        if boo:
            self.Weapon.Error.delete(0, "end")
        else:
            boolean = False
            self.Weapon.Error.delete(0, "end")
            self.Weapon.Error.insert("end", "Not a weapon!")

        if boolean:
            if data == False:
                return False
            data.update({"2H": bool(twoHand), "Damage": int(damage), "Weapon": weapon})
            return data
        return False

    def Clean(self):
        super(DisplayWeapon, self).Clean()
        self.Damage.Box.delete(0, "end")
        self.TwoHand.Box.delete(0, "end")
        self.Weapon.Box.delete(0, "end")

    def Toggle(self):
        super(DisplayWeapon, self).Toggle()
        self.Damage.Toggle()
        self.TwoHand.Toggle()
        self.Weapon.Toggle()


class DisplayItem(DisplayMain):
    def __init__(self, root, main):
        super(DisplayItem, self).__init__(root, main)
        self.Defence = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Defence", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 125,
            },
        )
        self.Armour = EntrySection(
            self.root,
            {
                "text": {"x": 0, "text": "Armour Type", "height": 25},
                "box": {"x": 100, "width": 100, "height": 25},
                "y": 150,
            },
        )

        self.Make.Button.place(x=100, y=175, width=100, height=25)
        self.Back.Button.place(x=0, y=175, width=100, height=25)

        self.path = "Items\\"
        self.type = "item"

    def MakeItem(self):
        data = super(DisplayItem, self).MakeItem()

        boolean = True
        defence = self.Defence.Box.get()
        armour = self.Armour.Box.get()

        if not self.EditLabel(IsInt, defence, self.Defence, "Not a number!"):
            boolean = False
        armour, boo = IsWeapon(armour)
        if boo:
            self.Armour.Error.delete(0, "end")
        else:
            boolean = False
            self.Armour.Error.delete(0, "end")
            self.Armour.Error.insert("end", "Not a weapon!")

        if boolean:
            if data == False:
                return False
            data.update({"Defence": defence, "Armour": armour})
            return data
        return False

    def Clean(self):
        super(DisplayItem, self).Clean()
        self.Defence.Box.delete(0, "end")
        self.Armour.Box.delete(0, "end")

    def Toggle(self):
        super(DisplayItem, self).Toggle()
        self.Defence.Toggle()
        self.Armour.Toggle()


class Display(object):
    def __init__(self):
        self.root = tkinter.Tk()

        self.Item = DisplayItem(self.root, self)
        self.Weapon = DisplayWeapon(self.root, self)

        self.Items = Button(
            self.root, {"x": 0, "y": 0, "text": "Make Item", "func": self.MakeItem}
        )
        self.Weapons = Button(
            self.root, {"x": 0, "y": 25, "text": "Make Weapon", "func": self.MakeWeapon}
        )

        self.Item.Toggle()
        self.Weapon.Toggle()

        self.root.mainloop()

    def MakeItem(self):
        self.Item.Toggle()

    def MakeWeapon(self):
        self.Weapon.Toggle()

    def Toggle(self):
        self.Items.Toggle()
        self.Weapons.Toggle()


# root = Tkinter.Tk()
# DisplayItem(root)
# root.mainloop()
Display()
