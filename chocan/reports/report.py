from pathlib import Path
from datetime import datetime

from chocan import utils


class Report:
    def __init__(self):
        """Initialize the report."""
        self.services = []
        self.report = ""

    def write(self, provider_directory={}):
        """Write the report to disk."""
        self.generate_report(provider_directory)

        if not utils.check_file(self.path):
            print(f"Could not write report for member with ID "
                  f"{self.services[0].member.id} to disk.")
            return

        with open(self.path, 'w') as file:
            file.write(self.report)

    def display(self, provider_directory={}):
        """Display the report in the terminal."""
        if not self.report:
            if utils.confirmation("No report found. Generate it?"):
                self.generate_report(provider_directory)
                print()
            else:
                print("No report to display.")
                return

        print(self.report)
        self.report = ""

    def generate_report(self, provider_directory={}):
        """Generate the report text."""
        self.report = ""
        member = self.services[0].member
        self.path = self.get_file(member)

        self.report += f"{member.name} (ID: {member.id})\n" \
                       f"{member.address}, {member.city}, {member.state} " \
                       f"{member.zip_code}\n\n"

        self.report += utils.tabulate(["Date", "Provider", "Service"],
            [(service.date_provided.strftime("%m-%d-%Y"),
              service.provider.name,
              service.service_name) for service in self.services])

    @staticmethod
    def get_file(person):
        """Get the file that the report should be written to.

        Args:
            person (Person): person to pull ID from

        Returns:
            Path: path of the text file to be written
        """
        folder = "providers" if person.id.startswith("8") else "members"

        return Path(".") / "reports" / folder / \
               f"{datetime.now().date().strftime('%Y%m%d')}_{person.id}.txt"
