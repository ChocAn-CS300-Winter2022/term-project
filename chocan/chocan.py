import json
import re
from datetime import datetime
from pathlib import Path

from chocan import utils
from chocan.utils import Alignment
from chocan.menu import Menu
from chocan.person import Person
from chocan.reports.report import Report
from chocan.service import Service


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
        self.users = [file.stem for file in path.glob("*.json")]

        while not quit:
            command = self.menu.display()

            # Login page
            if self.menu.page == Menu.MenuPage.LogIn:
                # Ask for ID
                if command == "1":
                    id = input("Enter an ID: ")
                    is_provider = id.startswith("8")

                    if id not in self.users or not (is_provider or
                        id.startswith("9")):
                        print("Invalid ID. Please try again.")
                    else:
                        self.current_person = Person(id)

                        self.menu.page = (Menu.MenuPage.ProviderTerminal
                            if is_provider else Menu.MenuPage.ManagerTerminal)
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
                    self.add_service_record()
                # Back to terminal
                elif command == "0":
                    if self.current_person.id.startswith("8"):
                        self.menu.page = Menu.MenuPage.ProviderTerminal
                    else:
                        self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")
            # Manage users
            elif self.menu.page == Menu.MenuPage.UserInformation:
                # Add user
                if command == "1":
                    self.add_user()
                # Remove user
                elif command == "2":
                    self.remove_user()
                # Modify user
                elif command == "3":
                    self.modify_user()
                # Back to terminal
                elif command == "0":
                    if self.current_person.id.startswith("8"):
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
                    if self.current_person.id.startswith("8"):
                        self.menu.page = Menu.MenuPage.ProviderTerminal
                    else:
                        self.menu.page = Menu.MenuPage.ManagerTerminal
                else:
                    print("Invalid command. Please try again.")

    def display_provider_directory(self):
        """Display the provider directory to the user."""
        # Tabulate the provider directory for printing and writing to file
        providers = utils.tabulate(["ID", "Name", "Fee"],
            [(key, value["name"], value["fee"]) for key, value in
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

    def add_service_record(self):
        """Add a service record."""
        id = input("Enter member ID: ")

        if id not in self.users:
            print("Invalid member ID.")
            return

        # TODO: Should we allow provider and manager numbers to be
        # used as IDs for services?
        member = Person(id)
        member.load()

        if member.status == Person.Status.Invalid:
            print("Invalid member ID.")
            return

        if member.status == Person.Status.Suspended:
            print("Member suspended until dues are paid.")
            return

        service_date = ""
        success = False

        while not success:
            service_date = input("Enter date service was provided "
                "(MM-DD-YYYY): ")
            success = re.search(r"\d{2}-\d{2}-\d{4}", service_date)

            if not success:
                print("Invalid date format. Please try again.")

        success = False
        self.display_provider_directory()

        service_code = ""
        confirm = False

        while service_code not in self.provider_directory or not confirm:
            service_code = input("Enter service service_code: ")

            if service_code not in self.provider_directory:
                print("Invalid service_code. Please try again.")
            else:
                confirm = utils.confirmation(
                    f"Is \"{self.provider_directory[service_code]['name']}\" "
                    "the correct service?")

        comments = input("Enter comments: ")

        Service(
            datetime.strptime(service_date, "%m-%d-%Y"),
            self.current_person,
            member,
            service_code,
            comments).generate_record(self.provider_directory)

        print(f"Fee: ${self.provider_directory[service_code]['fee']}")

    def add_user(self):
        pass

    def remove_user(self):
        pass

    def modify_user(self):
        pass

