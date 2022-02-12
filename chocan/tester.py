import argparse
import random
from datetime import datetime
from pathlib import Path

from chocan.chocan import ChocAn
from chocan.person import Person
from chocan.reports.provider_report import ProviderReport
from chocan.service import Service
from chocan.reports.report import Report


class Tester:
    class TesterArgumentValidator(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            report_count, service_count = values

            if report_count < 1:
                raise ValueError("invalid report count: must be larger than 0")
            elif report_count > 100:
                raise ValueError("invalid report count: must be 100 or less")

            if service_count < 1:
                raise ValueError("invalid service count: must be larger than 0")
            elif service_count > 100:
                raise ValueError("invalid service count: must be 100 or less")

            setattr(args, self.dest, (report_count, service_count))

    @staticmethod
    def run_test(program: ChocAn, counts):

        loaded_users = [file.stem for file
            in (Path(".") / "restricted" / "users").glob("*.json")]
        loaded_members = [user for user in loaded_users
            if not (user.startswith("8") or user.startswith("9"))]
        loaded_providers = [user for user in loaded_users
            if user.startswith("8")]

        members = [Person(member) for member in loaded_members]
        providers = [Person(provider) for provider in loaded_providers]

        for member in members:
            member.load()

        for provider in providers:
            provider.load()

        for i in range(counts[0]):
            report = Report()
            provider_report = ProviderReport()

            for j in range(counts[1]):
                service = Service(
                    datetime.now(),
                    random.choice(providers),
                    random.choice(members),
                    random.choice(list(program.provider_directory.keys()))
                )

                report.services.append(service)
                provider_report.services.append(service)

            report.write()
            provider_report.write(program.provider_directory)
