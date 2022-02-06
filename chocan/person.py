import json
from pathlib import Path

from chocan import utils
from chocan.service import Service


class Person:
    def __init__(self, id="", name="", address="", city="", state="",
        zip_code=""):
        """Create a new instance of Person."""
        self.id = id[:9]
        self.name = name[:25]
        self.address = address[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = zip_code[:5]
        self.services = []

    def addService(date_provided: datetime.date, provider, member,
        service_name, comments="")
        self.services.append(Service(date_provided, provider, member,
        service_name, comments))
        

    def display(self):
        """Display the person on the command line."""
        print(f"---- ID: {self.id} ----")
        print(f"Name:    {self.name}")
        print(f"Address: {self.address}, {self.city}, {self.state} "
              f"{self.zip_code}")

    def save(self):
        """Save the person to disk."""
        path = self.get_file(self.id)

        if not utils.check_file(path):
            print(f"Could not write person with ID {self.id} to disk.")
            return

        with open(path, "w") as file:
            json.dump(self.__dict__, file, indent=4, sort_keys=False)

    def load(self, id=""):
        """Load the person from disk with a given ID."""
        if id == "":
            id = self.id

        path = self.get_file(id)

        if not path.is_file():
            print(f"Could not load person with ID {id} from disk.")
            return

        with open(path, 'r') as file:
            self.__dict__.update(json.load(file))

    @staticmethod
    def get_file(id):
        """Get the file that the person is stored in."""
        if id.startswith("8"):
            folder = "providers"
        elif id.startswith("9"):
            folder = "managers"
        else:
            folder = "members"

        return Path(".") / "restricted" / "users" / folder / f"{id}.json"
