import CharClasses as Class
import NewGame


class Menu:
    def __init__(self, player):
        self.player = player

    @staticmethod
    def new_game():
        return Menu(NewGame.select_hero())

    @staticmethod
    def load_player(name):
        with open(f"Saves\\{name}.rpgsave", "w") as f:
            return Menu(Class.Player(f.read()))

    def save(self):
        with open(f"Saves\\{self.player.name}.rpgsave", "w") as f:
            f.write(str(self.player))


if __name__ == "__main__":
    menu = Menu.new_game()
    menu.save()
