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
        self.modified_user = None

        path = utils.get_top_directory() / "restricted" / "provider_directory.json"

        if not path.is_file():
            print("Failed to load provider directory.")
            return

        with open(path, 'r') as file:
            self.provider_directory = json.load(file)

    def run(self):
        """Run the ChocAn program."""
        quit = False
        path = utils.get_top_directory() / "restricted" / "users"
        self.users = [file.stem for file in path.glob("*.json")]

        while not quit:
            command = self.menu.display(
                self.current_person is not None and
                self.current_person.id.startswith("9"))

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
                        self.menu.page = Menu.MenuPage.Main
                # Exit program
                elif command == "0":
                    quit = True
                else:
                    print("Invalid command. Please try again.")
            # Main terminal
            elif self.menu.page == Menu.MenuPage.Main:
                # Manage services
                if command == "1":
                    self.menu.page = Menu.MenuPage.Services
                # Back to login
                elif command == "0":
                    self.menu.page = Menu.MenuPage.LogIn
                elif self.current_person.id.startswith("9"):
                    # Manage users
                    if command == "2":
                        self.menu.page = Menu.MenuPage.UserInformation
                    # Manage reports
                    elif command == "3":
                        self.menu.page = Menu.MenuPage.Reports
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
                    self.menu.page = Menu.MenuPage.Main
                else:
                    print("Invalid command. Please try again.")
            # Manage users
            elif self.menu.page == Menu.MenuPage.UserInformation:              
                # Add user
                if command == "1":
                    self.add_user()
                # Remove user
                elif command == "2":
                    id = input("Enter the ID of the Member you would "
                          "like to remove: ")
                    self.modified_user = Person(id)
                    # Back to terminal selection if load fails
                    if not self.modified_user.load():
                        print("Member ID not found in ChocAn system")
                    else:
                        self.remove_user()
                # Modify user menu
                elif command == "3":
                    id = input("Enter the ID of the Member you would "
                          "like to modify: ")
                    self.modified_user = Person(id)
                    # Back to terminal selection if load fails
                    if not self.modified_user.load():
                        print("Member ID not found in ChocAn system")
                    else:
                        self.menu.page = Menu.MenuPage.ModifyUser
                # Back to terminal selection
                elif command == "0":
                    self.menu.page = Menu.MenuPage.Main
                else:
                    print("Invalid command. Please try again.")
            #Modify User function
            elif self.menu.page == Menu.MenuPage.ModifyUser:
                self.modify_user(command)
            # Manage reports
            elif self.menu.page == Menu.MenuPage.Reports:
                # Generate summary report
                if command == "1":
                    self.generate_summary_report()
                # Generate member report
                elif command == "2":
                    self.generate_member_report()
                # Generate provider report
                elif command == "3":
                    self.generate_provider_report()
                # Back to terminal
                elif command == "0":
                    self.menu.page = Menu.MenuPage.Main
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

        path = utils.get_top_directory() / "provider_directory.txt"

        if not utils.check_file(path):
            print("Could not write provider directory to file.")
            return

        with open(path, 'w') as file:
            file.write(providers)

    def add_service_record(self):
        """Add a service record."""
        id = input("Enter member ID: ")

        if id not in self.users or id.startswith("8") or id.startswith("9"):
            print("Invalid member ID.")
            return

        member = Person(id)
        member.load()

        if member.status == Person.Status.Invalid:
            print("Invalid member ID.")
            return

        if member.status == Person.Status.Suspended:
            print("Member suspended until dues are paid.")
            return

        if self.current_person.id.startswith("9"):
            provider_id = ""

            while provider_id not in self.users or \
                not provider_id.startswith("8"):
                provider_id = input("Enter provider ID: ")

                if provider_id not in self.users or \
                    not provider_id.startswith("8"):
                    print("Invalid provider ID. Please try again.")

            provider = Person(provider_id)
            provider.load()
        else:
            provider = self.current_person

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
            service_code = input("Enter service code: ")

            if service_code not in self.provider_directory:
                print("Invalid service code. Please try again.")
            else:
                confirm = utils.confirmation(
                    f"Is \"{self.provider_directory[service_code]['name']}\" "
                    "the correct service?")

        comments = input("Enter comments: ")

        Service(
            datetime.strptime(service_date, "%m-%d-%Y"),
            provider,
            member,
            service_code,
            comments).generate_record(self.provider_directory)

        print(f"Fee: ${self.provider_directory[service_code]['fee']}")

    def add_user(self):
        create_provider = False

        if self.current_person.id.startswith("9"):
            command = ""

            while command == "":
                print("1) Create a new Member")
                print("2) Create a new Provider")
                print("0) Back")

                command = input("> ")
                create_provider = True if command == "3" else False

                if command == "2":
                    pass
                elif command == "3":
                    pass
                else:
                    print("Invalid command. Please try again.")

    def remove_user(self):
        """Sets user ID to invalid which flags the ID to never be used again.
        Users shall not be removed from system"""
        print("This is the user to be removed from the ChocAn system...\n")
        self.modified_user.display()
        if utils.confirmation("Are you sure you want to remove this user? "
                            "This action is PERMANENT: "):
            self.modified_user.status = Person.Status.Invalid
            print("The user has been deleted from the ChocAn system.")
            return
        else:
            print("The user has not been removed from the ChocAn system.")

    def modify_user(self, command):
        """Modifies the chosen user

        Args:
            command (str): command from main function
        """
        # Name
        if command == "1":
            new_name = input("Enter user's new name: ")
            if len(new_name) > 25:
                print("User's new name is too long. Must be 25 "
                    "characters or less.")
            else:
                self.modified_user.name = new_name
                self.modified_user.save()
        # Address
        elif command == "2":
            new_address = input("Enter user's new address: ")
            if len(new_address) > 25:
                print("User's new address is too long. Must be 25 "
                    "characters or less.")
            else:
                self.modified_user.address = new_address
                self.modified_user.save()
        # City
        elif command == "3":
            new_city = input("Enter user's new city: ")
            if len(new_city) > 14:
                print("User's new city is too long. Must be 14 "
                    "characters or less.")
            else:
                self.modified_user.city = new_city
                self.modified_user.save()
        # State
        elif command == "4":
            new_state = input("Enter user's new state: ")
            if len(new_state) > 2:
                print("User's new state is too long. Must be 2 "
                    "characters or less.")
            else:
                self.modified_user.state = new_state
                self.modified_user.save()
        # Zip code
        elif command == "5":
            new_zip = input("Enter user's new zip code: ")
            if len(new_zip) > 5:
                print("User's new zip code is too long. Must be 2 "
                    "characters or less.")
            else:
                self.modified_user.zip_code = new_zip
                self.modified_user.save()
        # Back to user information
        elif command == "0":
            self.menu.page = Menu.MenuPage.UserInformation
        else:
            print("Invalid command. Please try again.")

    def generate_summary_report(self):
        pass

    def generate_member_report(self):
        pass

    def generate_provider_report(self):
        pass
