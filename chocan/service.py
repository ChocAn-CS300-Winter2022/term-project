import json
from datetime import datetime
from pathlib import Path

from chocan import utils


class Service:
    def __init__(self, date_provided: datetime.date, provider, member,
        service_code, comments=""):
        """Create a new Service object.

        Args:
            date_provided (datetime.date): date the service was provided
            provider (Person): provider who gave the service
            member (Person): member who received the service
            service_code (str): service code
            comments (str, optional): comments about the service. Defaults to "".
        """
        self.current_date = datetime.now()

        try:
            self.date_provided = date_provided.date()
        except AttributeError:
            self.date_provided = date_provided

        self.provider = provider
        self.member = member
        self.service_code = service_code
        self.comments = comments[:100]

    def display(self, provider_directory):
        """Display the Service.

        Args:
            provider_directory (dict): provider directory loaded in ChocAn
        """
        print(f"---- {provider_directory[self.service_code]['name']} ----")
        print(f"Provider: {self.provider.name}")
        print(f"Member:   {self.member.name}")
        print(f"Date:     {self.date_provided.strftime('%m-%d-%Y')}")
        print(f"Comments: {self.comments}")

    def generate_record(self, provider_directory):
        """Generate a record to write to the logs folder.

        Args:
            provider_directory (dict): provider directory loaded in ChocAn
        """
        record = {
            "current_date": self.current_date.strftime("%m-%d-%Y %H:%M:%S"),
            "date_provided": self.date_provided.strftime("%m-%d-%Y"),
            "provider": self.provider.id,
            "member": self.member.id,
            "service_code": provider_directory[self.service_code]["name"],
            "comments": self.comments
        }

        # filename = 111111111_888888888_20220101_000000.json
        filename = (f"{self.provider.id}_{self.member.id}_"
                    f"{self.current_date.strftime('%Y%m%d_%H%M%S')}"
                    f".json")

        path = utils.get_top_directory() / "restricted" / "logs" / filename

        if not utils.check_file(path):
            print("Could not write record to disk.")
            return

        with open(path, "w") as file:
            json.dump(record, file, indent=4, sort_keys=False)
