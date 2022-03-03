import argparse
import random
import unittest
from datetime import datetime
from pathlib import Path

from chocan.chocan import ChocAn
from chocan.menu import Menu
from chocan.person import Person
from chocan.reports.report import Report
from chocan.reports.provider_report import ProviderReport
from chocan.reports.summary_report import SummaryReport
from chocan.service import Service


class Tester(unittest.TestCase):
    class TesterArgumentValidator(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            """Ensure Tester arguments are valid."""
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
    def generate_reports(program: ChocAn, report_count, service_count):
        """Generate example reports.

        Args:
            program (ChocAn): main program instance
            report_count (int): number of reports to generate
            service_count (int): number of services to generate
        """
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

        service_codes = list(program.provider_directory.keys())
        sampled_members = random.sample(members,
            min(report_count, len(members)))

        provider_reports = {}

        for member in sampled_members:
            report = Report()

            for i in range(service_count):
                service = Service(datetime.now(), random.choice(providers),
                    member, random.choice(service_codes))

                report.services.append(service)

                if service.provider.id not in provider_reports:
                    provider_reports[service.provider.id] = []

                provider_reports[service.provider.id].append(service)

            report.write(program.provider_directory)

        for id, services in provider_reports.items():
            provider_report = ProviderReport()

            for service in services:
                provider_report.services.append(service)

            provider_report.write(program.provider_directory)

    def test_report_init_success(self):
        """Test Report initialization."""
        report = Report()
        self.assertEqual((report.services, report.report), ([], ""))

    def test_provider_report_init_success(self):
        """Test Provider Report initialization."""
        provider_report = ProviderReport()
        self.assertEqual((provider_report.services, provider_report.report),
            ([], ""))

    def test_summary_report_init_success(self):
        """Test Summary Report initialization."""
        summary_report = SummaryReport()
        # TODO: assert summary report

    def test_chocan_init_success(self):
        """Test ChocAn initialization."""
        chocan = ChocAn()
        self.assertEqual((chocan.menu.page, chocan.current_person),
            (Menu.MenuPage.LogIn, None))

    def test_menu_init_success(self):
        """Test Menu initialization."""
        menu = Menu()
        self.assertEqual(menu.page, Menu.MenuPage.LogIn)

    def test_person_init_success(self):
        """Test Person initialization."""
        person = Person()
        self.assertEqual(())
