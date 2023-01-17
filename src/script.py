# FILE TO BUILD CLONE OF "https://github.com/timm/tested/blob/main/src/script.lua"
import sys
import math
import collections

from test import test_rand, test_global_options, test_sym, test_num
from test_runner import TestRunner

K_HELP = 'help'
K_SEED = 'seed'
K_DEFAULT_SEED_VALUE = 937162211
K_TEST = 'test'

global_options = {}

class Num:
    def __init__(self):
        self.n, self.mu, self.m2 =0, 0, 0
        self.max, self.min = -100000000000000, 100000000000000
    
    def add(self, value):
        if type(value) == int:
          self.n+=1
          d = value-self.mu
          self.mu += d/self.n
          self.m2 += d*(value-self.mu)
          self.min = min(value, self.min)
          self.max = min(value, self.max)

    def mid(self):
        return self.mu
    
    def div(self):
        if self.m2 < 0 or self.n < 2:
          return 0
        else:
          return ((self.m2)/(self.n -1))**0.5


class Sym:
    def __init__(self):
        self.n = 0 #total number of elements in the stream
        self.has = collections.defaultdict(int) #the dictionary which stores values of each alphabet in the stream
        self.most, self.mode = 0, "" # self.mode contains the alphabet which is recurring the highest number of times and self.most is its count
        
    def add(self, value):
        if value.isalpha():
            self.n+=1
            self.has[value]+=1
            if self.has[value] > self.most:
                self.most, self.mode = self.has[value], value
    def mid(self):
        return self.mode

    def div(self):
        print("TODO - return the standard entropy")
        def fun(x):
            return x*math.log(x,2)
        self.entropy = 0
        keys = list(self.has.values())
        print(keys)
        for i in keys:
            self.entropy += fun(i/self.n)
        return -self.entropy



def rnd(n, nPlaces):
    """
    Rounds of the output to nPlaces places.
    """
    if nPlaces:
        mult = 10**nPlaces
    else:
        mult = 10**3
    return math.floor(n*mult+0.5)/mult

def rand(seed = 937162211, lo = 0, hi=1):
  seed = 16807*seed % 2147483647
  return lo+(hi-lo)*seed/2147483647

def rint(lo, hi):
  return math.floor(0.5+rand(lo,hi))

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
    # TODO:
    initialize_from_cli()
    return run_tests()

__main__()

