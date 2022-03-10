from pathlib import Path

from chocan import utils

#      Name      | Consultations |   Fee
# -----------------------------------------
# Cecelia Carson |            10 |  $999.99
# Jessica Ware   |             3 |  $124.99
# Kyle Wilkinson |            29 | $1049.99

# Total providers:     3
# Total consultations: 42
# Total fee:           $2174.97

# TODO: Summary Report
class SummaryReport:
    def __init__(self):
        self.providers = {}
        self.report = ""

    def write(self, provider_directory):
        """Write the report to disk."""
        self.generate_report(provider_directory)

        if not utils.check_file(self.path):
            print(f"Could not write summary report to disk.")
            return

        with open(self.path, 'w') as file:
            file.write(self.report)

    def display(self, provider_directory):
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

    def generate_report(self):
        pass
