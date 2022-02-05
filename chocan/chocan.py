from chocan.menu import Menu

class ChocAn:
    def __init__(self):
        self.menu = Menu()

    def begin(self):
        quit = False

        while not quit:
            command = self.menu.display()

            if command == "1":
                self.menu.page = Menu.MenuPage.FirstLoad
            elif command == "2":
                self.menu.page = Menu.MenuPage.Login
            elif command == "3":
                self.menu.page = Menu.MenuPage.ProviderMain
            elif command == "4":
                self.menu.page = Menu.MenuPage.ManagerMain
            else:
                print("Invalid command.")
                quit = True

        print("Exiting...")
