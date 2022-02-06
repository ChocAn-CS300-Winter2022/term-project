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
        RequestInformation = 2
        Services = 3
        Reports = 4

    #Menu constructor - using page inspiried by Alana's teachings
    def __init__(self):
        """Create a new Menu instance."""
        self.page = Menu.MenuPage.FirstLoad
        self.people = []
        self.reports = []

    def display(self):
        """Display the menu system."""
        print()

        #TODO Adjust the firstload and login to be elsewhere so a flag can be
        #used to properly identify HOW to display the menu and make this a
        #little cleaner.
        #TODO "Draft bill" does not do anything yet...
        #TODO "Add Subsystem for Interactive Menu Items"
        if self.page == Menu.MenuPage.FirstLoad:
            print(" Menu ".center(67, "="))
            print("1) Draft a bill")
            print("2) Request information")
            print("3) Manage services")
            print("4) Reports")
            print("0) Log off")
        elif self.page == Menu.MenuPage.RequestInformation:
            print(" Request Information ".center(67, "="))
            print("1) Request member information")
            print("2) Request provider information")
            print("3) Request available services")
            print("0) Back")
        elif self.page == Menu.MenuPage.Services:
            print(" Services ".center(67, "="))
            print("1) Member services")
            print("2) Provider services")
            print("3) Service modifications")
            print("0) Back")
        elif self.page == Menu.MenuPage.Reports:
            print(" Reports ".center(67, "="))
            print("1) Summary report")
            print("2) Member report")
            print("3) Weekly provider report")
            print("4) EFT report")
            print("0) Back")

        print(67 * "=")

        return input("> ")
