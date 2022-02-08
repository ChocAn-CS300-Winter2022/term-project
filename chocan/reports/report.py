from chocan import utils


class Report:
    def __init__(self):
        """Initialize the report."""
        self.services = []
        self.report = ""

        # TODO: Instead of overriding write() in each subclass, set self.folder
        # to determine which folder it should go in?
        # self.folder = ""

    def write(self):
        """Write the report to disk."""
        self.report = self.generate_report()

        # TODO: write to disk

    def display(self):
        """Display the report in the terminal."""
        if not self.report:
            if utils.confirmation("No report found. Generate it?"):
                self.generate_report()
            else:
                print("No report to display.")
                return

        print(self.report)
        self.report = ""

    def generate_report(self):
        """Generate the report text."""
        # TODO: generate the report
        pass
