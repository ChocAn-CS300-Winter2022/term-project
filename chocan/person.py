import json
from pathlib import Path
from enum import Enum

from chocan import utils


class Person:
    class Status(Enum):
        Invalid = -1
        Suspended = 0
        Valid = 1

    def __init__(self, id="", name="", address="", city="", state="",
        zip_code=""):
        """Create a new instance of Person."""
        self.id = id[:9]
        self.name = name[:25]
        self.address = address[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = zip_code[:5]
        self.status = Person.Status.Valid

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
        """Load the person from disk with a given ID.

        Args:
            id (str, optional): the ID to load from disk. Defaults to self.id.
        """
        if id == "":
            id = self.id

        path = self.get_file(id)

        if not path.is_file():
            print(f"Could not load person with ID {id} from disk.")
            return False

        with open(path, 'r') as file:
            self.__dict__.update(json.load(file))
            
        return True

    @staticmethod
    def get_file(id):
        """Get the file that the person is stored in."""
        return utils.get_top_directory() / "restricted" / "users" / f"{id}.json"
