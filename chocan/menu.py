'''
This file contains the menu system and various components to
enable fluid navigation through the ChocAn system
'''

from enum import Enum
import enum



#Class for the menu. Contains the functions for each menu that will be utilized
#for the ChocAn system.
class Menu:
    
    #enum the options to give visible description when being checked against other parts of the system.
    class Menu_Enum(Enum):
        FirstLoad = 1
        Login = 2
        ProviderMain = 3
        ManagerMain = 4

    #Menu constructor - using page inspiried by Alana's teachings
    def __init__(self):
        self.page = Menu.Menu_Enum.FirstLoad

    #display the menu system
    def menu_display(self):

        #TODO Testing input
        print("Pick a number 1-4 - though we don't actually do anything with it yet")

        #TODO refer to the crash-course and design doc on what to put here... This could
        #be cut smaller by combining the last elif into the provider main some how?
        #it also doesn't hurt to just have double menu in manager I suppose?
        '''if self.page == Menu.Menu_Enum.FirstLoad:
            #TBD
        elif self.page == Menu.Menu_Enum.Login:
            #TBD
        elif self.page == Menu.Menu_Enum.ProviderMain:
            #TBD
        elif self.page == Menu.Menu_Enum.ManagerMain:
            #TBD'''
        
        return input("> ")

if __name__ == "__main__":
    menu = Menu()
    menu.menu_display()