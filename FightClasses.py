class Fight(object):
    def __init__(self, good, bad):
        print("FIGHT!!!")
        print(", ".join((i.name for i in good))+" v "+", ".join((i.name for i in bad)))
        print()
        self.gChars = good
        self.bChars = bad
        i = 0
        while len(self.gChars)!=0 and len(self.bChars)!=0:
            print("TURN %i!!!"%i)
            self.turn()
            i += 1

    def turn(self):
        attack_queue = []
        for i in self.gChars:
            attack_queue.append([i.speed(), i, True])
        for i in self.bChars:
            attack_queue.append([i.speed(), i, False])
        attack_queue.sort()
        attack_queue.reverse()
        for i in attack_queue:
            if i[1].health > 0:
                arr = self.bChars if i[2] else self.gChars
                print(i[1].name, "v", arr[0].name)
                print(i[1].p_health(), ":", arr[0].p_health())
                i[1].fight(arr[0])
                print(i[1].p_health(), ":", arr[0].p_health())
                if arr[0].health <= 0:
                    if i[2]:
                        i[1].gain_exp(arr[0])
                        self.bChars.pop(0)
                    else:
                        self.gChars.pop(0)
                    if len(arr) == 0:
                        break
        for i in self.gChars:
            i.end_of_turn_heal()
        for i in self.bChars:
            i.end_of_turn_heal()

    def won(self):
        return len(self.gChars) != 0 and len(self.bChars) == 0
