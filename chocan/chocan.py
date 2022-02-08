import json
from pathlib import Path

from chocan.menu import Menu


class ChocAn:
    def __init__(self):
        self.menu = Menu()

        path = Path(".") / "restricted" / "provider_directory.json"

        if not path.is_file():
            print("Failed to load provider directory.")
            return

        with open(path, 'r') as file:
            self.provider_directory = json.load(file)

    def run(self):
        quit = False

        while not quit:
            command = self.menu.display()

            if self.menu.page == Menu.MenuPage.LogIn:
                if command == "1":
                    # TODO: Determine whether manager of provider
                    self.menu.page = Menu.MenuPage.ManagerTerminal
                elif command == "0":
                    quit = True
                else:
                    print("Invalid command. Please try again.")
            elif self.menu.page == Menu.MenuPage.ProviderTerminal:
                if command == "1":
                    self.menu.page = Menu.MenuPage.Services
                elif command == "0":
                    self.menu.page = Menu.MenuPage.LogIn
                else:
                    print("Invalid command. Please try again.")
            elif self.menu.page == Menu.MenuPage.ManagerTerminal:
                if command == "1":
                    self.menu.page = Menu.MenuPage.Services
                elif command == "0":
                    self.menu.page = Menu.MenuPage.LogIn
                elif command == "2":
                    self.menu.page = Menu.MenuPage.UserInformation
                elif command == "3":
                    self.menu.page = Menu.MenuPage.Reports
                else:
                    print("Invalid command. Please try again.")
            elif self.menu.page == Menu.MenuPage.Services:
                if command == "1":
                    self.display_provider_directory()
                elif command == "2":
                    print("Add service record")
                elif command == "0":
                    # TODO: Determine whether provider or manager
                    self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")
            elif self.menu.page == Menu.MenuPage.UserInformation:
                if command == "1":
                    print("Add member")
                elif command == "2":
                    print("Remove member")
                elif command == "3":
                    print("Modify member")
                elif command == "4":
                    print("Add provider")
                elif command == "5":
                    print("Remove provider")
                elif command == "6":
                    print("Modify provider")
                elif command == "0":
                    # TODO: Determine whether provider or manager
                    self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")
            elif self.menu.page == Menu.MenuPage.Reports:
                if command == "1":
                    print("Generate summary report")
                elif command == "2":
                    print("Generate member report")
                elif command == "3":
                    print("Generate provider report")
                elif command == "0":
                    # TODO: Determine whether provider or manager
                    self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")

    def display_provider_directory(self):
        """Display the provider directory to the user."""
        pass
