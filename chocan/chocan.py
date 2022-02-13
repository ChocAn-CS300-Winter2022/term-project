import json
from pathlib import Path

from chocan import utils
from chocan.utils import Alignment
from chocan.menu import Menu
from chocan.person import Person


class ChocAn:
    def __init__(self):
        self.menu = Menu()
        self.current_person = None

        path = Path(".") / "restricted" / "provider_directory.json"

        if not path.is_file():
            print("Failed to load provider directory.")
            return

        with open(path, 'r') as file:
            self.provider_directory = json.load(file)

    def run(self):
        """Run the ChocAn program."""
        quit = False
        path = Path(".") / "restricted" / "users"
        users = [file.stem for file in path.glob("*.json")]

        while not quit:
            command = self.menu.display()

            # Login page
            if self.menu.page == Menu.MenuPage.LogIn:
                # Ask for ID
                if command == "1":
                    self.login()
                # Exit program
                elif command == "0":
                    quit = True
                else:
                    print("Invalid command. Please try again.")
            # Provider terminal
            elif self.menu.page == Menu.MenuPage.ProviderTerminal:
                # Manage services
                if command == "1":
                    self.menu.page = Menu.MenuPage.Services
                # Back to login
                elif command == "0":
                    self.menu.page = Menu.MenuPage.LogIn
                else:
                    print("Invalid command. Please try again.")
            # Manager terminal
            elif self.menu.page == Menu.MenuPage.ManagerTerminal:
                # Manage services
                if command == "1":
                    self.menu.page = Menu.MenuPage.Services
                # Manager users
                elif command == "2":
                    self.menu.page = Menu.MenuPage.UserInformation
                # Manage reports
                elif command == "3":
                    self.menu.page = Menu.MenuPage.Reports
                # Back to login page
                elif command == "0":
                    self.menu.page = Menu.MenuPage.LogIn
                else:
                    print("Invalid command. Please try again.")
            # Manage services
            elif self.menu.page == Menu.MenuPage.Services:
                # Show provider directory
                if command == "1":
                    self.display_provider_directory()
                # Add a service record
                elif command == "2":
                    print("Add service record")
                # Back to terminal
                elif command == "0":
                    if self.current_person["id"].startswith("8"):
                        self.menu.page = Menu.MenuPage.ProviderTerminal
                    else:
                        self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")
            # Manage users
            elif self.menu.page == Menu.MenuPage.UserInformation:
                # Add member
                if command == "1":
                    print("Add member")
                # Remove member
                elif command == "2":
                    print("Remove member")
                # Modify member
                elif command == "3":
                    print("Modify member")
                # Add provider
                elif command == "4":
                    print("Add provider")
                # Remove provider
                elif command == "5":
                    print("Remove provider")
                # Modify provider
                elif command == "6":
                    print("Modify provider")
                # Back to terminal
                elif command == "0":
                    if self.current_person["id"].startswith("8"):
                        self.menu.page = Menu.MenuPage.ProviderTerminal
                    else:
                        self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")
            # Manage reports
            elif self.menu.page == Menu.MenuPage.Reports:
                # Generate summary report
                if command == "1":
                    print("Generate summary report")
                # Generate member report
                elif command == "2":
                    print("Generate member report")
                # Generate provider report
                elif command == "3":
                    print("Generate provider report")
                # Back to terminal
                elif command == "0":
                    if self.current_person["id"].startswith("8"):
                        self.menu.page = Menu.MenuPage.ProviderTerminal
                    else:
                        self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")

    def display_provider_directory(self):
        """Display the provider directory to the user."""
        # Tabulate the provider directory for printing and writing to file
        providers = utils.tabulate(["ID", "Name", "Fee"],
            [(value['id'], key, value['fee']) for key, value in
                self.provider_directory.items()],
            [Alignment.Left, Alignment.Left, Alignment.Right])

        if not providers:
            print("Could not write provider directory to file.")
            return

        print(" Provider Directory ".center(providers.index("\n"), "-"))
        print(providers)

        path = Path(".") / "provider_directory.txt"

        if not utils.check_file(path):
            print("Could not write provider directory to file.")
            return

        with open(path, 'w') as file:
            file.write(providers)

    def login(self):
        """Log in to the terminal."""
        id = input("Enter an ID: ")
        is_provider = id.startswith("8")

        if id not in self.users or not (is_provider or id.startswith("9")):
            print("Invalid ID. Please try again.")
        else:
            self.current_person = Person(id)

            self.menu.page = (Menu.MenuPage.ProviderTerminal
                if is_provider else Menu.MenuPage.ManagerTerminal)
