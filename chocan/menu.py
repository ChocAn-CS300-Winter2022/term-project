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
        InteractiveMenu = 3
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
            print(30 * "=", "Menu", 30 * "=")
            print("1) Draft a bill")
            print("2) Request Information")
            print("3) Interactive Menu")
            print("4) Reports")
            print("0) Log Off")
            print(67 * "=")
        elif self.page == Menu.MenuPage.RequestInformation:  
            print("1) Request Member Information")
            print("2) Request Provider Information")
            print("3) Request Available Services")
            print("0) Main Menu")
        elif self.page == Menu.MenuPage.InteractiveMenu:
            print("1) Member Services")
            print("2) Provider Services")
            print("3) Service Modifications")
            print("0) Main Menu")
        elif self.page == Menu.MenuPage.Reports:
            print("1) Summary Report")
            print("2) Member Report")
            print("3) Weekly Provder Report")
            print("4) EFT Report")
            print("0) Main Menu")


        return input("> ")
