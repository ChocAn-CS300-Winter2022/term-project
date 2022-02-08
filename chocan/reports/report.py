from pathlib import Path
from datetime import datetime

from chocan import utils


class Report:
    def __init__(self):
        """Initialize the report."""
        self.services = []
        self.report = ""

    def write(self):
        """Write the report to disk."""
        self.generate_report()

        if not utils.check_file(self.path):
            print(f"Could not write report for member with ID "
                  f"{self.services[0].member.id} to disk.")
            return

        with open(self.path, 'w') as file:
            file.write(self.report)

    def display(self):
        """Display the report in the terminal."""
        if not self.report:
            if utils.confirmation("No report found. Generate it?"):
                self.generate_report()
                print()
            else:
                print("No report to display.")
                return

        print(self.report)
        self.report = ""

    def generate_report(self):
        """Generate the report text."""
        self.report = ""
        member = self.services[0].member
        self.path = self.get_file(member)

        self.report += f"{member.name} (ID: {member.id})\n" \
                       f"{member.address}, {member.city}, {member.state} " \
                       f"{member.zip_code}\n\n"

        for i in range(0, len(self.services)):
            service = self.services[i]

            self.report += f"Date:     " \
                           f"{service.date_provided.strftime('%Y-%m-%d')}\n" \
                           f"Provider: {service.provider.name}\n" \
                           f"Service:  {service.service_name}"

            if i < (len(self.services) - 1):
                self.report += "\n\n"

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
