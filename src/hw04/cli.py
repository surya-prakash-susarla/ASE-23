import sys

from globals import *

def get_full_option_for_short_version(option) -> str:
    if option == 's':
        return K_SEED
    elif option == 'S':
        return K_SAMPLE
    elif option == 'g':
        return K_START_ACTION
    elif option == 'h':
        return K_HELP
    elif option == 'f':
        return K_FILE
    elif option == 'F':
        return K_FARAWAY
    elif option == 'm':
        return K_MIN
    elif option == 'p':
        return K_DISTANCE_COEF
    print("ERROR - UNKNOWN SHORT OPTION : {}".format(option))
    return None

def default_cli_options():
    # initialize default seed value 
    global_options[K_SEED] = K_DEFAULT_SEED_VALUE
    # initalize to run 'data_read' test if unspecified
    global_options[K_START_ACTION] = K_DEFAULT_START_ACTION
    # initialzie to use defalut csv file if unspecified
    global_options[K_FILE] = K_DEFAULT_DATA_FILE 
    # initialize 'help' to false.
    global_options[K_HELP] = False

    # cluster options initialization
    global_options[K_FARAWAY] = K_DEFAULT_FARAWAY_VALUE
    global_options[K_MIN] = K_DEFAULT_MIN_VALUE
    global_options[K_DISTANCE_COEF] = K_DEFAULT_DISTANCE_COEF
    global_options[K_SAMPLE] = K_DEFAULT_SAMPLE_VALUE

def initialize_from_cli():
    default_cli_options()
    parse_cli_options()

def get_option_key_and_value_requirement(key) -> tuple[str, bool]:
    full_options_with_value = [K_SEED, K_START_ACTION, K_FILE, K_FARAWAY, K_MIN, K_DISTANCE_COEF, K_SAMPLE]
    short_options_with_value = ['s', 'g', 'f', 'F', 'm', 'p', 'S']
    
    key = key[2:] if key[1] == '-' else key[1:]
    
    if key in full_options_with_value:
        return (key, True)
    elif key in short_options_with_value:
        return (get_full_option_for_short_version(key), True)
    else:
        return (K_HELP, False)

def print_help():
    print('''
    OPTIONS:
    -d or --dump            -> on crash, dump stack   = false
    -h or --help            -> Show this message.
    -F or --Far             -> distance to "faraway"  = .95
    -f or --file            -> Name of file = 'data/auto93.csv'
    -g or --go              -> Default action = 'data'
    -m or --min             -> stop clusters at N^min = .5
    -p or --p               -> distance coefficient   = 2
    -s or --seed            -> random number seed     = 937162211
    -S or --Sample          -> sampling data size     = 512
    ''')

def handle_unknown_cli_option():
    print("Unknown option, please run -h (or) --help for more details.")

def parse_cli_options():
    global global_options
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
                    global_options[K_HELP] = True
        else:
            global_options[option_key] = arg
            next_arg_is_value = False

