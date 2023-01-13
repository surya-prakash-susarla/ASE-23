# FILE TO BUILD CLONE OF "https://github.com/timm/tested/blob/main/src/script.lua"

K_HELP = 'help'
K_SEED = 'seed'
K_DEFAULT_SEED_VALUE = 937162211

global_options = {}

class Num:
    def __init__(self):
        print("TODO - fill the constructor")
    
    def add(value):
        print("TODO - fill adding value to the num class")

    def mid():
        print("TODO - get mid value")
    
    def div():
        print("TODO - implement standard deviation using Wolford's algorithm")

class Sym:
    def __init__(self):
        print("TODO - fill the constructor for Sym")

    def add(value):
        print("TODO - fill add symbol value")
    
    def mid():
        print("TODO - return the mode value")

    def div():
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

def initialize_from_cli():
    print("TODO - add cli parsing and initialization")

    # initialize default seed value 
    global_options[K_SEED] = K_DEFAULT_SEED_VALUE

#### MAIN
def __main__():
    # TODO:
    # 1. build cli options
    initialize_from_cli()
    # 2. start up main functions 
    # 3. test framework

__main__()

