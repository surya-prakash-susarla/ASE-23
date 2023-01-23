# FILE TO BUILD CLONE OF "https://github.com/timm/tested/blob/main/src/script.lua"
import sys
import math
import collections

from test import test_rand, test_global_options, test_sym, test_num
from test_runner import TestRunner
from cli import initialize_from_cli
from globals import global_options, K_TEST

def run_tests() -> int:
    # List of all test and test bodies. Empty string evaluates to running all tests.
    tests = { 'rand': test_rand,
            'num': test_num,
            'sym': test_sym,
            'opt': test_global_options
            }

    test_runner: TestRunner = TestRunner(tests)
    # Empty string is indicator to run all tests.
    test_name = "" if global_options[K_TEST] == "all" else global_options[K_TEST]
    results: tuple[bool, list[str]] = test_runner.run(test_name)

    if len(results[1]) != 0:
        print("Failed tests : {}", ",".join([i for i in results[1]]))
        return 1
    return 0

#### MAIN
def __main__():
    initialize_from_cli()
    return run_tests()

sys.exit(__main__())
