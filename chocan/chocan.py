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


    def begin(self):
        quit = False

        while not quit:
            command = self.menu.display()

            if self.menu.page == Menu.MenuPage.FirstLoad:
                if command == "1":
                    self.menu.page = Menu.MenuPage.FirstLoad
                elif command == "2":
                    self.menu.page = Menu.MenuPage.RequestInformation
                elif command == "3":
                    self.menu.page = Menu.MenuPage.InteractiveMenu
                elif command == "4":
                    self.menu.page = Menu.MenuPage.Reports
                elif command == "0":
                    quit = True
                else:
                    print("Invalid command, Please Try Again.")
            elif self.menu.page == Menu.MenuPage.RequestInformation:
                if command == "1":
                    print("Member Information test")
                elif command == "2":
                    print("Provider Information test")
                elif command == "3":
                    print("Available Services test")
                elif command == "0":
                    self.menu.page = Menu.MenuPage.FirstLoad
                else:
                    print("Invalid command, Please Try Again.")
            elif self.menu.page == Menu.MenuPage.InteractiveMenu:
                if command == "1":
                    print("Add member sub menu")
                elif command == "2":
                    print("Add provider sub menu")
                elif command == "3":
                    print("Add services sub menu")
                elif command == "0":
                    self.menu.page = Menu.MenuPage.FirstLoad
                else:
                    print("Invalid command, Please Try Again.")
            elif self.menu.page == Menu.MenuPage.Reports:
                if command == "1":
                    print("Generating Summary Report...")
                elif command == "2":
                    print("Generating Member Report")
                elif command == "3":
                    print("Generating Wkly Provider Report")
                elif command == "4":
                    print("Generating EFT Report")
                elif command == "0":
                    self.menu.page = Menu.MenuPage.FirstLoad
                else:
                    print("Invalid command, Please Try Again.")
