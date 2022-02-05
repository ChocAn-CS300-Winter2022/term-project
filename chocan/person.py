import json
from pathlib import Path


class Person:
    def __init__(self, id=0, name="", address="", city="", state="",
        zip_code=0):
        """Create a new instance of Person."""
        self.id = int(str(id)[:9])
        self.name = name[:25]
        self.address = address[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = int(str(zip_code)[:5])

    def display(self):
        """Display the person on the command line."""
        print(f"---- ID: {self.id} ----")
        print(f"Name:    {self.name}")
        print(f"Address: {self.address}, {self.city}, {self.state} "
              f"{self.zip_code}")

    def save(self):
        """Save the person to disk."""
        file = self.get_file(self.id)

        if file.is_dir() or file.is_symlink():
            print(f"Could not write person with ID {self.id} to disk.")

        with open(file, "w") as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=False)

    def load(self, id=0):
        """Load the person from disk with a given ID."""
        if id == 0:
            id = self.id

        file = self.get_file(id)

        if not file.is_file():
            print(f"Could not load person with ID {id} from disk.")
            return

        with open(file, 'r') as file:
            self.__dict__.update(json.load(file))

    @staticmethod
    def get_file(id):
        """Get the file that the person is stored in."""
        if str(id).startswith("8"):
            folder = "providers"
        elif str(id).startswith("9"):
            folder = "managers"
        else:
            folder = "members"

        return Path(".") / "restricted" / "users" / folder / f"{id}.json"
