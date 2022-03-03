import argparse
from argparse import RawTextHelpFormatter

# import the ChocAn class from the file chocan/chocan.py
from chocan.chocan import ChocAn
from chocan.random_generator import RandomGenerator
from chocan.tester import Tester

if __name__ == "__main__":
    types = ("members", "providers", "managers")

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
        epilog="REPORT_COUNT, SERVICE_COUNT, and USER_COUNT must be between 1 "
            "and 100, inclusive.\nREPORT_COUNT will generate the requested "
            "reports up to the number of available\nmember files.\n\n"
            "REPORT_COUNT member reports will be generated with SERVICE_COUNT "
            "random services\nfor each. Each service will also  receive a "
            "randomly-assigned provider, and for\neach a provider report will "
            "also be generated.")
    parser.add_argument("--generate-reports", "-gr", type=int, nargs=2,
        metavar=("REPORT_COUNT", "SERVICE_COUNT"),
        action=Tester.TesterArgumentValidator,
        help="generate REPORT_COUNT member reports, each with SERVICE_COUNT "
            "services on load")
    parser.add_argument("--generate-users", "-gu", nargs=2,
        action=RandomGenerator.RandomGeneratorArgumentValidator,
        help=f"generate users. USER_TYPE must be one of: {', '.join(types)}.",
        metavar=("USER_TYPE", "USER_COUNT"))

    args = parser.parse_args()
    program = ChocAn()

    if args.generate_users:
        RandomGenerator.generate(args.generate[0], args.generate[1])

    if args.generate_reports:
        Tester.generate_reports(program, args.test[0], args.test[1])

    program.run()
