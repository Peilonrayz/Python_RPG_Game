import json, os

for fileName in os.listdir(os.curdir):
    fSplit = os.path.splitext(fileName)
    if fSplit[1] == '.json':
        print fileName
        with open(fSplit[0]+'.base', 'w') as f1:
            with open(fSplit[0]+'.json', 'r') as f2:
                s = json.load(f2)
                json.dump(s, f1, sort_keys=True)
        with open(fSplit[0]+'.json', 'w') as f:
            json.dump(s, f, sort_keys=True, indent=4, separators=(',', ': '))
