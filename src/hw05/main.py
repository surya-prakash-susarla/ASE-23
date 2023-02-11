import sys
import math
import collections

from test import *
from test_runner import TestRunner
from cli import initialize_from_cli, print_help
from globals import global_options, K_HELP, K_START_ACTION

def run_tests() -> int:
    # List of all test and test bodies. Empty string evaluates to running all tests.
    tests = { 
             'the': test_global_options,
             'rand': test_rand,
             'some': test_some,
             'clone': test_clone,
             'dist': test_dist,
             'cliffs': test_cliffs,
             'tree': test_tree,
             'sway': test_sway,
             'bins': test_bins,
             'read': test_read_from_csv,
             'half': test_half
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

