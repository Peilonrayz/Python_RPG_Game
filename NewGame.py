import CharClasses as Class
import json, os

def Int(string):
    try:
        int(string)
        return True
    except:
        return False

def Loop(question, functions):
    if functions == None:
        del functions
        functions = []
    b = False
    while b == False:
        choice = raw_input(question)
        b = True
        for i in functions:
            if not i(choice):
                b = False
                break
    return choice

def getHeroChoice():
    for fileName in os.listdir('classes\\'):
        fSplit = os.path.splitext(fileName)
        if fSplit[1] == '.base':
            yield fSplit[0]

def getSaves():
    for fileName in os.listdir('Saves\\'):
        fSplit = os.path.splitext(fileName)
        if fSplit[1] == '.rpgsave':
            yield fSplit[0]
            
def SelectHero():
    c = list(getHeroChoice())
    for i in xrange(len(c)):
        print i, c[i]
    def a(List):
        def b(string):
            return string in List
        return b
    choice = Loop('What do you want to be?\n', [Int, a([str(i) for i in range(len(c))])])
    saves = list(getSaves())
    while True:
        name = Loop('What is your name?\n', [])
        if name in saves:
            over = Loop('This player allready exists, do you wish to overide it?\n', [a(['y', 'yes', 'n', 'no'])])
            if over in ['yes', 'y']:
                break
            else:
                pass
        else:
            break
    gender = Loop('Are you male or female?\n', [a(['m', 'male', 'f', 'female'])])
    if gender in ['m', 'male']:
        gender = 'Male'
    else:
        gender = 'Female'
    with open('classes\\'+c[int(choice)]+'.base', 'r') as f:
        s = json.load(f)
        s['Name'] = name
        s['Gender'] = gender
        return Class.Player(s)
