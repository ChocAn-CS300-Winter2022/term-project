import argparse
import json
import random

from chocan import utils
# pip install faker
from faker import Faker
from faker.providers import DynamicProvider
from pathlib import Path


class RandomGenerator:
    class RandomGeneratorArgumentValidator(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            valid_types = ("members", "providers", "managers")
            user_type, count = values

            count = int(count)

            if user_type not in valid_types:
                raise ValueError(f"invalid user type '{user_type}'")

            if count < 1:
                raise ValueError("invalid count: must be larger than 0")
            elif count > 100:
                raise ValueError("invalid count: must be 100 or less")

            setattr(args, self.dest, (user_type, count))

    @staticmethod
    def generate_id(user_type):
        if user_type == "providers":
            random_id = str(random.randint(800000000, 899999999))
        elif user_type == "managers":
            random_id = str(random.randint(900000000, 999999999))
        else:
            random_id = str(random.randint(0, 799999999)).zfill(9)

        return {
            "id": random_id,
            "path": (utils.get_top_directory() / "restricted" / "users" /
                f"{random_id}.json")
        }

    @staticmethod
    def generate(user_type, count):
        cities = [
            ("Alhambra", "91802"),
            ("Beverly Hills", "90210"),
            ("Burbank", "91502"),
            ("Calabasas", "91302"),
            ("Compton", "90220"),
            ("Culver City", "90232"),
            ("El Segundo", "90245"),
            ("Glendale", "91206"),
            ("Hermosa Beach", "90254"),
            ("Inglewood", "90301"),
            ("Long Beach", "90802"),
            ("Los Angeles", "90012"),
            ("Malibu", "90265"),
            ("Montebello", "90640"),
            ("Monterey Park", "91754"),
            ("Palmdale", "93550"),
            ("Pasadena", "91109"),
            ("Pomona", "91766"),
            ("Redondo Beach", "90277"),
            ("Santa Clarita", "91355"),
            ("Santa Monica", "90401"),
            ("West Hollywood", "90069")]

        faker = Faker()

        for i in range(count):
            random_id = None

            while random_id == None or random_id["path"].exists():
                random_id = RandomGenerator.generate_id(user_type)

            if not random_id["path"].exists():
                name = f"{faker.first_name()} {faker.last_name()}"

                while len(name) > 25:
                    name = f"{faker.first_name()} {faker.last_name()}"

                address = faker.street_address()

                while len(address) > 25:
                    address = faker.street_address()

                la_city = random.choice(cities)

                json_str = {
                    "id": random_id["id"],
                    "name": name,
                    "address": faker.street_address(),
                    "city": la_city[0],
                    "state": "CA",
                    "zip_code": la_city[1]
                }

                with open(random_id["path"], 'w') as file:
                    json.dump(json_str, file, indent=4, sort_keys=False)
