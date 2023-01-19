# FILE TO BUILD CLONE OF "https://github.com/timm/tested/blob/main/src/script.lua"
import sys
import math
import collections

from test import test_rand, test_global_options, test_sym, test_num
from test_runner import TestRunner
from config import global_options, K_SEED, K_DEFAULT_SEED_VALUE

K_HELP = 'help'
K_TEST = 'test'

def print_help():
    print('''
    OPTIONS:
    -h or --help            -> Show this message.
    -s or --seed            -> Set seed value for random number generator.
    ''')

def handle_unknown_cli_option():
    print("Unknown option, please run -h (or) --help for more details.")

def get_option_key_and_value_requirement(key) -> tuple[str, bool]:
    if key == '-h' or key ==  "--"+K_HELP:
        return (K_HELP, False)
    elif key == '-s' or key == "--"+K_SEED:
        return (K_SEED, True)
    elif key == '-t' or key == "--"+K_TEST:
        return (K_TEST, True)
    else:
        return (K_HELP, False)

def parse_cli_options():
    # skip 0 for script name.
    next_arg_is_value = False
    option_key = ""
    for arg in sys.argv[1:]:
        if not next_arg_is_value:
            option_details = get_option_key_and_value_requirement(arg)
            if option_details[1]:
                next_arg_is_value = True
                option_key = option_details[0]
            else:
                # Options which do not require value might expect different handling.
                if option_details[0] == K_HELP:
                    print_help()
                    return
        else:
            global_options[option_key] = arg
            next_arg_is_value = False

def default_cli_options():
    # initialize default seed value 
    global_options[K_SEED] = K_DEFAULT_SEED_VALUE
    # initalize to run all tests if unspecified
    global_options[K_TEST] = ""

def initialize_from_cli():
    default_cli_options()
    parse_cli_options()

def run_tests() -> int:
    # List of all test and test bodies. Empty string evaluates to running all tests.
    tests = {
            'rand': test_rand,
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

