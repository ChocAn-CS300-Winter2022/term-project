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
    def run_test(program: ChocAn, report_count, service_count):
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

        service_names = list(program.provider_directory.keys())
        sampled_members = random.sample(members,
            min(report_count, len(members)))

        provider_reports = {}

        for member in sampled_members:
            report = Report()

            for i in range(service_count):
                service = Service(datetime.now(), random.choice(providers),
                    member, random.choice(service_names))

                report.services.append(service)

                if service.provider.id not in provider_reports:
                    provider_reports[service.provider.id] = []

                provider_reports[service.provider.id].append(service)

            report.write()

        for id, services in provider_reports.items():
            provider_report = ProviderReport()

            for service in services:
                provider_report.services.append(service)

            provider_report.write(program.provider_directory)
