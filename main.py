# import the Menu class from the file chocan/menu.py
from chocan.menu import Menu

def main():
    menu = Menu()
    quit = False

    while not quit:
        command = menu.display()

        if command == "1":
            menu.page = Menu.MenuPage.FirstLoad
        elif command == "2":
            menu.page = Menu.MenuPage.Login
        elif command == "3":
            menu.page = Menu.MenuPage.ProviderMain
        elif command == "4":
            menu.page = Menu.MenuPage.ManagerMain
        else:
            print("Invalid command.")
            quit = True

    print("Exiting...")

if __name__ == "__main__":
    main()
