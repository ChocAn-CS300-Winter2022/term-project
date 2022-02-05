import json
from pathlib import Path


class Person:
    def __init__(self, id="000000000", name="", address="", city="", state="",
        zip_code="00000"):
        """Create a new instance of Person."""
        self.id = int(id[:9])
        self.name = name[:25]
        self.address = address[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = int(zip_code[:5])

    def display(self):
        """Display the person on the command line."""
        print(f"---- ID: {self.id} ----")
        print(f"Name:    {self.name}")
        print(f"Address: {self.address}, {self.city}, {self.state} "
              f"{self.zip_code}")

    def save(self):
        """Save the person to disk."""
        if self.id.startswith("8"):
            folder = "providers"
        elif self.id.startswith("9"):
            folder = "managers"
        else:
            folder = "members"

        file = Path(".") / "restricted" / "users" / folder / f"{self.id}.json"

        if file.is_dir() or file.is_symlink():
            print(f"Could not write person with ID {self.id} to disk.")

        with open(file, "w") as f:
            json.dump(self.__dict__, f, indent=4, sort_keys=False)

    def load(self, id=""):
        """Load the person from disk with a given ID."""
        if id == "":
            id = self.id

        file = Path(".") / "restricted" / "users" / self.get_folder(id) /\
            f"{id}.json"

        if not file.is_file():
            print(f"Could not load person with ID {id} from disk.")
            return

        with open(file, 'r') as file:
            self.__dict__.update(json.load(file))

    @staticmethod
    def get_folder(id):
        """Get the folder that the person is stored in."""
        if str(id).startswith("8"):
            return "providers"
        elif str(id).startswith("9"):
            return "managers"

        return "members"
