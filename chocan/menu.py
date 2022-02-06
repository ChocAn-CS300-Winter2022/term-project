'''
This file contains the menu system and various components to
enable fluid navigation through the ChocAn system.
'''

from enum import Enum


#Class for the menu. Contains the functions for each menu that will be utilized
#for the ChocAn system.
class Menu:
    #enum the options to give visible description when being checked against
    #other parts of the system.
    class MenuPage(Enum):
        LogIn = 1
        ProviderTerminal = 2
        ManagerTerminal = 3
        UserInformation = 4
        Services = 5
        Reports = 6

    #Menu constructor - using page inspiried by Alana's teachings
    def __init__(self):
        """Create a new Menu instance."""
        self.page = Menu.MenuPage.LogIn
        self.people = []
        self.reports = []

    def display(self):
        """Display the menu system."""
        print()

        if self.page == Menu.MenuPage.LogIn:
            print(" Chocoholics Anonymous ".center(67, "="))
            print("1) Log in")
            print("0) Exit")
        elif (self.page == Menu.MenuPage.ProviderTerminal or
              self.page == Menu.MenuPage.ManagerTerminal):
            # provider or manager
            print(" Main Menu ".center(67, "="))
            print("1) Manage services")

            if self.page == Menu.MenuPage.ManagerTerminal:
                # only manager
                print("2) Member or provider information")
                print("3) Reports")

            print("0) Log off")
        elif self.page == Menu.MenuPage.Services:
            print(" Services ".center(67, "="))
            print("1) View provider directory")
            print("2) Add service record")
            print("0) Back")
        elif self.page == Menu.MenuPage.UserInformation:
            print(" User Information ".center(67, "="))
            print(" Member ".center(67, "-"))
            print("1) Add member")
            print("2) Remove member")
            print("3) Modify member")
            print(" Provider ".center(67, "-"))
            print("4) Add provider")
            print("5) Remove provider")
            print("6) Modify provider")
            print("0) Back")
        elif self.page == Menu.MenuPage.Reports:
            print(" Reports ".center(67, "="))
            print("1) Generate summary report")
            print("2) Generate member report")
            print("3) Generate provider report")
            print("0) Back")

        print(67 * "=")

        return input("> ")
