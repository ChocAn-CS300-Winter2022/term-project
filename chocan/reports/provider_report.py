from chocan import utils
from chocan.utils import Alignment
from chocan.reports.report import Report


class ProviderReport(Report):
    def generate_report(self, provider_directory):
        self.report = ""
        provider = self.services[0].provider
        self.path = self.get_file(provider)

        self.report += f"{provider.name} (ID: {provider.id})\n" \
                       f"{provider.address}, {provider.city}, {provider.state} " \
                       f"{provider.zip_code}\n\n"

        self.report += utils.tabulate(
            ["Date", "Received", "Member Name", "Member ID", "Service",
                "Fee"],
            [(service.date_provided.strftime("%m-%d-%Y"),
              service.current_date.strftime("%m-%d-%Y %H:%M:%S"),
              service.member.name,
              service.member.id,
              service.service_code,
              "$" + provider_directory[service.service_code]["fee"]) \
                  for service in self.services],
            col_alignments=[Alignment.Left, Alignment.Left, Alignment.Left,
                Alignment.Right, Alignment.Right, Alignment.Right])
