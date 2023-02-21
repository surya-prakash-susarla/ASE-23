import sys

from globals import *

def get_full_option_for_short_version(option) -> str:
    if option == 's':
        return K_SEED
    elif option == 'g':
        return K_START_ACTION
    elif option == 'h':
        return K_HELP
    elif option == 'f':
        return K_FILE
    elif option == 'F':
        return K_FAR
    elif option == 'm':
        return K_MIN
    elif option == 'M':
        return K_MAX
    elif option == 'p':
        return K_DISTANCE_COEF
    elif option == 'b':
        return K_BINS
    elif option == 'c':
        return K_CLIFFS
    elif option == 'H':
        return K_HALVES
    elif option == 'r':
        return K_REST
    elif option == 'R':
        return K_REUSE
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

    global_options[K_FAR] = K_FAR_DEFAULT_VALUE
    global_options[K_MIN] = K_MIN_DEFAULT_VALUE
    global_options[K_MAX] = K_MAX_DEFAULT_VALUE
    global_options[K_HALVES] = K_HALVES_DEFAULT_VALUE
    global_options[K_REST] = K_REST_DEFAULT_VALUE
    global_options[K_REUSE] = K_REUSE_DEFAULT_VALUE
    global_options[K_DISTANCE_COEF] = K_DEFAULT_DISTANCE_COEF
    global_options[K_CLIFFS] = K_CLIFFS_DEFAULT_VALUE

def initialize_from_cli():
    default_cli_options()
    parse_cli_options()

def get_option_key_and_value_requirement(key) -> tuple[str, bool]:
    full_options_with_value = [K_SEED, K_START_ACTION, K_FILE, K_BINS, K_CLIFFS, K_FAR, K_HALVES, K_MIN, K_MAX, K_DISTANCE_COEF, K_REST, K_REUSE]
    short_options_with_value = ['s', 'g', 'f', 'b', 'c', 'F', 'H', 'm', 'M', 'p', 'r', 'R']
    
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
    -b or --bins            -> initial number of bins               = 16
    -c or --cliffs          -> cliff's delta threshold              = .147
    -d or --dump            -> on crash, dump stack                 = false
    -h or --help            -> Show this message.
    -F or --Far             -> distance to "faraway"                = .95
    -f or --file            -> Name of file = 'data/auto93.csv'
    -g or --go              -> Default action = 'data'
    -m or --min             -> stop clusters at N^min               = .5
    -M or --Max             -> numbers                              = 512
    -p or --p               -> distance coefficient                 = 2
    -s or --seed            -> random number seed                   = 937162211
    -S or --Sample          -> sampling data size                   = 512
    -H or --Halves          -> search space for clustering          = 512
    -r or --rest            -> how many of rest to sample           = 4
    -R or --Reuse           -> child splits reuse a parent pole     = true
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

