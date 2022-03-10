import argparse
import random
from shutil import register_unpack_format
import unittest
from unittest.mock import Mock
from unittest.mock import patch
from datetime import datetime
from pathlib import Path

from defer import return_value

from chocan import utils
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
        loaded_users = [file.stem for file in
            (utils.get_top_directory() / "restricted" / "users").glob("*.json")]
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
                service.generate_record(program.provider_directory)

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

    def test_chocan_init_success(self):
        """Test ChocAn initialization."""
        chocan = ChocAn()
        self.assertEqual((chocan.menu.page, chocan.current_person),
            (Menu.MenuPage.LogIn, None))

    @patch('chocan.utils.confirmation', return_value = True)
    @patch('chocan.person')
    def test_remove_user_pick_yes(self, mock_confirmation, mock_user):
        """Test Selecting to Remove User"""
        chocan = ChocAn()

        chocan.remove_user(mock_user)
        mock_user.save.assert_called_once()

        self.assertEqual(mock_user.status, Person.Status.Invalid)

    @patch('chocan.utils.confirmation', return_value = False)
    @patch('chocan.person')
    def test_remove_user_pick_no(self, mock_confirmation, mock_user):
        """Test Selecting to Not Remove User"""
        chocan = ChocAn()

        mock_user.status = Person.Status.Valid
        chocan.remove_user(mock_user)
        mock_user.save.assert_not_called()

        self.assertEqual(mock_user.status, Person.Status.Valid)


    """MENU.PY"""
    def test_menu_init_success(self):
        """Test Menu initialization."""
        menu = Menu()
        self.assertEqual(menu.page, Menu.MenuPage.LogIn)


    """PERSON.PY"""
    def test_person_init_success(self):
        """Test Person initialization."""
        person = Person()
        self.assertEqual((person.id, person.name, person.address,
        person.city, person.state, person.zip_code, person.status),
            ("", "", "", "", "", "", Person.Status.Valid))

    def test_person_is_provider_success(self):
        """Test Person is_provider."""
        person = Person()
        person.id = '800000000'
        self.assertTrue(person.is_provider())
    
    def test_person_is_provider_failure(self):
        """Test Person is_provider."""
        person = Person()
        person.id = '900000000'
        self.assertFalse(person.is_provider())

    def test_person_is_manager_success(self):
        """Test Person is_manager."""
        person = Person()
        person.id = '900000000'
        self.assertTrue(person.is_manager())
    
    def test_person_is_manager_failure(self):
        """Test Person is_manager."""
        person = Person()
        person.id = '800000000'
        self.assertFalse(person.is_manager())

    @patch('chocan.utils.get_top_directory', 
            return_value = Path("test"))
    def test_person_get_file_success(self, mock_get_top_directory):
        """Test Person get_file"""
        actual_file_path = Person.get_file('123456789')
        expected_file_path = Path("test/restricted/users/123456789.json")
        self.assertEqual(actual_file_path, expected_file_path)


    """SERVICE.PY"""
   # @patch('datetime.now', return_value=10)
    def test_service_init_provided_datetime(self):
        """Test Service init with datetime provided"""
        date = datetime.today().date()
        provider = Person()
        member = Person()
        service_code = "999999"
        service = Service(date, provider, member, service_code)
        self.assertEqual((service.date_provided, service.provider, 
            service.member, service.service_code, service.comments),
            (date, provider, member, service_code, 
            ""))

    def test_service_init_provided_string(self):
        """Test Service init with string provided"""
        date = "2020-03-10"
        provider = Person()
        member = Person()
        service_code = "999999"
        service = Service(date, provider, member, service_code)
        self.assertEqual((service.date_provided, service.provider, 
            service.member, service.service_code, service.comments),
            (date, provider, member, service_code, 
            ""))


    """REPORT.PY"""
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
        self.assertEqual((summary_report.services, summary_report.report), 
            ([], ""))

