import datetime
import json
import re
from pathlib import Path

from chocan import utils
from chocan.utils import Alignment
from chocan.person import Person
from chocan.reports.report import Report


class SummaryReport(Report):
    def generate_report(self, provider_directory):
        """Generate a summary report.

        Args:
            provider_directory (dict): provider directory loaded in ChocAn
        """
        self.report = ""
        self.path = self.get_file()
        loaded_records = utils.get_weekly_records()

        # Get each provider and service as a tuple
        services = [(service["provider"], service["service_code"])
                             for service in loaded_records]
        # Then get each unique provider ID
        providers = set(tuple[0] for tuple in services)

        names = []
        consultations = []
        fees = []

        for id in providers:
            provider = Person(id)

            if not provider.load():
                continue

            # Get the service IDs for each provider
            service_ids = [tuple[1] for tuple in services if tuple[0] == id]
            fee = 0.0

            # Calculate the total fee from each service code
            for consult in service_ids:
                fee += float(provider_directory[consult]["fee"])

            # Then append the name, total consultations, and total fee
            names.append(provider.name)
            consultations.append(len(service_ids))
            fees.append(fee)

        self.report += utils.tabulate(
            ["Name", "Consultations", "Fee"],
            list(zip(names, consultations, ["${:.2f}".format(fee) for fee in fees])),
            [Alignment.Left, Alignment.Right, Alignment.Right]) + "\n"
        self.report += f"Total providers:     {len(providers)}\n"
        self.report += f"Total consultations: {sum(consultations)}\n"
        self.report += f"Total fee:           ${'%.2f' % sum(fees)}\n"

    @staticmethod
    def get_week():
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())

        return [(monday + datetime.timedelta(days=d)).strftime("%Y%m%d")
                for d in range(5)]

    @staticmethod
    def get_file():
        """Get the file that the report should be written to.

        Returns:
            Path: path of the text file to be written
        """
        return utils.get_top_directory() / "reports" / "summaries" / \
               f"{datetime.datetime.now().date().strftime('%Y%m%d')}.txt"
