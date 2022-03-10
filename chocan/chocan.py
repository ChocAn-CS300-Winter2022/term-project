import json
import re
from datetime import datetime

from chocan import utils
from chocan.menu import Menu
from chocan.person import Person
from chocan.random_generator import RandomGenerator
from chocan.reports.report import Report
from chocan.reports.summary_report import SummaryReport
from chocan.service import Service
from chocan.utils import Alignment

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
                self.current_person.is_manager())

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
                # Manage members
                elif self.current_person.is_manager():
                    if command == "2":
                        self.menu.page = Menu.MenuPage.UserInformation
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
                    id_valid = False

                    while not id_valid:
                        id = input("Enter the ID of the user to remove: ")

                        if self.current_person.is_provider():
                            if not id.startswith("8") and not id.startswith("9"):
                                id_valid = True
                        else:
                            if not id.startswith("9"):
                                id_valid = True

                        if id not in self.users:
                            id_valid = False

                        if not id_valid:
                            print("Invalid ID. Please try again.")

                    user = Person(id)
                    # Back to terminal selection if load fails
                    if user.load():
                        self.remove_user(user)
                # Modify user menu
                elif command == "3":
                    id_valid = False

                    while not id_valid:
                        id = input("Enter the ID of the user to modify: ")

                        if self.current_person.is_provider():
                            if not id.startswith("8") and not id.startswith("9"):
                                id_valid = True
                        else:
                            if not id.startswith("9"):
                                id_valid = True

                        if id not in self.users:
                            id_valid = False

                        if not id_valid:
                            print("Invalid ID. Please try again.")

                    self.modified_user = Person(id)
                    # Back to terminal selection if load fails
                    if self.modified_user.load():
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

        if self.current_person.is_manager():
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
        """Add a user."""
        create_provider = False

        if self.current_person.is_manager():
            command = ""

            while command == "":
                print()
                print(" Services ".center(67, "="))
                print("1) Create a new Member")
                print("2) Create a new Provider")
                print("0) Back")
                print(67 * "=")

                command = input("> ")
                #use this to check if making a provider to save input
                #commands
                create_provider = True if command == "2" else False

                if command == "1":
                    create_provider = False
                elif command == "2":
                    create_provider = True
                elif command == "0":
                    self.menu.page = Menu.MenuPage.UserInformation
                    return
                else:
                    print("Invalid command. Please try again.")

        name = input("Enter first and last name: ")
        address = input("Enter address: ")
        city = input("Enter city: ")
        state = input("Enter state: ")
        zip_code = input("Enter zip code: ")

        id = ""
        id_valid = False

        while not id_valid:
            id = RandomGenerator.generate_id("providers" if
                create_provider else "members")
            if id["id"] not in self.users:
                id_valid = True

        new_user = Person(id["id"], name, address, city, state,
            zip_code)
        new_user.display()
        new_user.save()

        if utils.confirmation(f"Do you want to modify {name}?"):
            self.menu.page = Menu.MenuPage.ModifyUser

    def remove_user(self, user):
        """Sets user ID to invalid. Users are not removed from the system. The
        ID may not be used again.

        Args:
            user (Person): user to remove
        """
        user.display()

        print()

        if utils.confirmation(f"Are you sure you want to remove {user.name}? "
                               "This action is permanent."):
            user.status = Person.Status.Invalid
            user.save()
            print("The user has been removed.")
        else:
            print("Cancelled removing user.")

    def modify_user(self, command):
        """Modifies the chosen user.

        Args:
            command (str): command from main function
        """
        # Name
        if command == "1":
            new_name = input("Enter user's new name: ")
            if len(new_name) > 25:
                print("User's new name must be 25 characters or less.")
            else:
                self.modified_user.name = new_name
                self.modified_user.save()
        # Address
        elif command == "2":
            new_address = input("Enter user's new address: ")
            if len(new_address) > 25:
                print("User's new address must be 25 characters or less.")
            else:
                self.modified_user.address = new_address
                self.modified_user.save()
        # City
        elif command == "3":
            new_city = input("Enter user's new city: ")
            if len(new_city) > 14:
                print("User's new city must be 14 characters or less.")
            else:
                self.modified_user.city = new_city
                self.modified_user.save()
        # State
        elif command == "4":
            new_state = input("Enter user's new state: ")
            if len(new_state) != 2:
                print("User's new state must be 2 characters exactly.")
            else:
                self.modified_user.state = new_state
                self.modified_user.save()
        # Zip code
        elif command == "5":
            new_zip = input("Enter user's new zip code: ")
            if len(new_zip) != 5:
                print("User's new zip code must be 5 characters exactly.")
            else:
                self.modified_user.zip_code = new_zip
                self.modified_user.save()
        # Back to user information
        elif command == "0":
            self.menu.page = Menu.MenuPage.UserInformation
        else:
            print("Invalid command. Please try again.")

    def generate_summary_report(self):
        report = SummaryReport()
        report.write(self.provider_directory)
        report.display(self.provider_directory)

    def generate_member_report(self):
        # TODO: member report
        #   Ask for member ID or all members
        #   Gather records for ID or all from last week (regex)
        #   Create new MemberReport() (or multiple if all)
        #   Write to disk
        pass

    def generate_provider_report(self):
        # TODO: provider report
        #   Ask for provider/manager ID or all
        #   Gather records for ID or all from last week (regex)
        #   Create new ProviderReport() (or multiple if all)
        #   Write to disk
        pass
