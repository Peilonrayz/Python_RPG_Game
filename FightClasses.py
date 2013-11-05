class Fight(object):
    def __init__(self, good, bad):
        print "FIGHT!!!"
        print ", ".join((i.name for i in good))+" v "+", ".join((i.name for i in bad))
        print
        self.gChars = good
        self.bChars = bad
        i = 0
        while len(self.gChars)!=0 and len(self.bChars)!=0:
            print "TURN %i!!!"%i
            self.Turn()
            i += 1
    def Turn(self):
        attackQueue = []
        for i in self.gChars:
            attackQueue.append([i.Speed(), i, True])
        for i in self.bChars:
            attackQueue.append([i.Speed(), i, False])
        attackQueue.sort()
        attackQueue.reverse()
        for i in attackQueue:
            if i[1].health > 0:
                arr = self.bChars if i[2] else self.gChars
                print i[1].name, "v", arr[0].name
                print i[1].PHealth(), ":", arr[0].PHealth()
                i[1].Fight(arr[0])
                print i[1].PHealth(), ":", arr[0].PHealth()
                if arr[0].health <= 0:
                    if i[2]:
                        i[1].GainExp(arr[0])
                        self.bChars.pop(0)
                    else:
                        self.gChars.pop(0)
                    if len(arr) == 0:
                        break
        for i in self.gChars:
            i.EndOfTurnHeal()
        for i in self.bChars:
            i.EndOfTurnHeal()
    def Won(self):
        return len(self.gChars) != 0 and len(self.bChars) == 0
