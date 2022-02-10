import argparse

# import the ChocAn class from the file chocan/chocan.py
from chocan.chocan import ChocAn
from chocan.random_generator import RandomGenerator
from chocan.tester import Tester

if __name__ == "__main__":
    types = ("members", "providers", "managers")

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", "-t", type=int, nargs=2,
        metavar=("REPORT_COUNT", "SERVICE_COUNT"),
        help="generate reports on load")
    parser.add_argument("--generate", "-g", nargs=2,
        action=RandomGenerator.ArgumentValidator,
        help=f"generate users. USER_TYPE must be one of: {', '.join(types)}. "
             f"COUNT must be larger than 0.",
        metavar=("USER_TYPE", "COUNT"))
    args = parser.parse_args()

    program = ChocAn()

    if args.generate:
        RandomGenerator.generate(args.generate[0], args.generate[1])

    if args.test:
        Tester.run_test(program, args.test)

    program.run()
