import json
from datetime import datetime
from pathlib import Path

from chocan import utils


class Service:
    def __init__(self, date_provided: datetime.date, provider, member,
        service_name, comments=""):
        self.current_date = datetime.now()
        self.date_provided = date_provided
        self.provider = provider
        self.member = member
        self.service_name = service_name
        self.comments = comments[:100]

    def generate_bill(self, provider_directory):
        bill = {
            "current_date": self.current_date.strftime("%m-%d-%Y %H:%M:%S"),
            "date_provided": self.date_provided.strftime("%m-%d-%Y"),
            "provider": self.provider.id,
            "member": self.member.id,
            "service_code": provider_directory[self.service_name]["id"],
            "comments": self.comments
        }

        filename = self.current_date.strftime("%m-%d-%Y_%H-%M-%S") + ".json"
        path = Path(".") / "restricted" / "logs" / filename

        if not utils.check_file(path):
            print("Could not write bill to disk.")
            return

        with open(path, "w") as file:
            json.dump(bill, file, indent=4, sort_keys=False)

    # Do we want to generate reports from the Service class directly, instead
    # of having another class called Reports?
    def generate_report(self):
        pass

    def generate_provider_report(self):
        pass
