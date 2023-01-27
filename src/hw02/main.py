import sys
import math
import collections

from test import test_global_options, test_sym, test_num, test_get_stats, test_read_from_csv, test_read_data_csv
from test_runner import TestRunner
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION

def run_tests() -> int:
    # List of all test and test bodies. Empty string evaluates to running all tests.
    tests = { 
        'num': test_num,
        'sym': test_sym,
        'opt': test_global_options,
        'stats': test_get_stats,
        'csv_read': test_read_from_csv,
        'data_read': test_read_data_csv
    }

    test_runner: TestRunner = TestRunner(tests)
    # Empty string is indicator to run all tests.
    test_name = "" if global_options[K_START_ACTION] == "all" else global_options[K_START_ACTION]
    results: tuple[bool, list[str]] = test_runner.run(test_name)

    if results[0] == False:
        print("Failed tests : {}".format(results[1]))
        return 1
    return 0

#### MAIN
def __main__() -> int:
    initialize_from_cli()

    if global_options[K_HELP]:
        print_help()
        return 0

    return run_tests()

sys.exit(__main__())

