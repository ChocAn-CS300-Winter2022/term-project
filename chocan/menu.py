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
        FirstLoad = 1
        Login = 2
        ProviderMain = 3
        ManagerMain = 4

    #Menu constructor - using page inspiried by Alana's teachings
    def __init__(self):
        """Create a new Menu instance."""
        self.page = Menu.MenuPage.FirstLoad

    def display(self):
        """Display the menu system."""
        print("Pick a number 1-4 - though we don't actually do anything with it"
              " yet")

        #TODO Adjust the firstload and login to be elsewhere so a flag can be
        #used to properly identify HOW to display the menu and make this a
        #little cleaner.
        if self.page == Menu.MenuPage.FirstLoad:
            print("first load")
        elif self.page == Menu.MenuPage.Login:
            print("login")
        elif self.page == Menu.MenuPage.ProviderMain:
            print("provider main")
        elif self.page == Menu.MenuPage.ManagerMain:
            print("manager main")

        return input("> ")
