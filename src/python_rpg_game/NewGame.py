import json
import os

import CharClasses as Class


def int_(string):
    try:
        int(string)
        return True
    except:
        return False


def loop(question, functions):
    if functions is None:
        del functions
        functions = []
    b = False
    while not b:
        choice = input(question)
        b = True
        for i in functions:
            if not i(choice):
                b = False
                break
    return choice


def get_hero_choice():
    for fileName in os.listdir("classes\\"):
        fSplit = os.path.splitext(fileName)
        if fSplit[1] == ".base":
            yield fSplit[0]


def get_saves():
    for fileName in os.listdir("Saves\\"):
        fSplit = os.path.splitext(fileName)
        if fSplit[1] == ".rpgsave":
            yield fSplit[0]


def select_hero():
    c = list(get_hero_choice())
    for i in range(len(c)):
        print(i, c[i])

    def a(List):
        def b(string):
            return string in List

        return b

    choice = loop(
        "What do you want to be?\n", [int_, a([str(i) for i in range(len(c))])]
    )
    saves = list(get_saves())
    while True:
        name = loop("What is your name?\n", [])
        if name in saves:
            over = loop(
                "This player allready exists, do you wish to overide it?\n",
                [a(["y", "yes", "n", "no"])],
            )
            if over in ["yes", "y"]:
                break
            else:
                pass
        else:
            break
    gender = loop("Are you male or female?\n", [a(["m", "male", "f", "female"])])
    if gender in ["m", "male"]:
        gender = "Male"
    else:
        gender = "Female"
    with open("classes\\" + c[int(choice)] + ".base", "r") as f:
        s = json.load(f)
        s["Name"] = name
        s["Gender"] = gender
        return Class.Player(s)
