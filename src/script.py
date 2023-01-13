# FILE TO BUILD CLONE OF "https://github.com/timm/tested/blob/main/src/script.lua"
import sys

K_HELP = 'help'
K_SEED = 'seed'
K_DEFAULT_SEED_VALUE = 937162211
K_TEST = 'test'

global_options = {}

class Num:
    def __init__(self):
        print("TODO - fill the constructor")
    
    def add(self, value):
        print("TODO - fill adding value to the num class")

    def mid(self):
        print("TODO - get mid value")
    
    def div(self):
        print("TODO - implement standard deviation using Wolford's algorithm")

class Sym:
    def __init__(self):
        print("TODO - fill the constructor for Sym")

    def add(self, value):
        print("TODO - fill add symbol value")
    
    def mid(self):
        print("TODO - return the mode value")

    def div(self):
        print("TODO - return the standard entropy")


def rand(low, hi):
    # return float value
    print("TODO - return random number between lo and hi")

def rand_n(n, nPlaces):
    # return float value
    print("TODO - return random number with precision 'n'")

def rand_int(n):
    # return int value
    print("TODO - return random number using rand")

def print_help():
    print('''
    OPTIONS:
    -h or --help            -> Show this message.
    -s or --seed            -> Set seed value for random number generator.
    ''')

def handle_unknown_cli_option():
    print("Unknown option, please run -h (or) --help for more details.")

def get_option_key_and_value_requirement(key) -> tuple[str, bool]:
    if key == '-h' or key ==  K_HELP:
        return (K_HELP, False)
    elif key == '-s' or key == K_SEED:
        return (K_SEED, True)
    elif key == '-t' or key == K_TEST:
        return (K_TEST, True)
    else:
        return (K_HELP, False)

def parse_cli_options():
    print("TODO - parse cli options")
    print("initial cli : ", sys.argv)
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
    print("Final options status : " , global_options)

def default_cli_options():
    # initialize default seed value 
    global_options[K_SEED] = K_DEFAULT_SEED_VALUE

def initialize_from_cli():
    default_cli_options()
    parse_cli_options()

#### MAIN
def __main__():
    # TODO:
    # 1. build cli options
    initialize_from_cli()
    # 2. start up main functions 
    # 3. test framework

__main__()

