import sys

from globals import global_options, K_SEED, K_DEFAULT_SEED_VALUE, K_HELP, K_TEST, K_FILE, K_DEFAULT_DATA_FILE

def default_cli_options():
    # initialize default seed value 
    global_options[K_SEED] = K_DEFAULT_SEED_VALUE
    # initalize to run all tests if unspecified
    global_options[K_TEST] = ""
    global_options[K_FILE]= K_DEFAULT_DATA_FILE 

def initialize_from_cli():
    default_cli_options()
    parse_cli_options()

def get_option_key_and_value_requirement(key) -> tuple[str, bool]:
    if key == '-h' or key ==  "--"+K_HELP:
        return (K_HELP, False)
    elif key == '-s' or key == "--"+K_SEED:
        return (K_SEED, True)
    elif key == '-t' or key == "--"+K_TEST:
        return (K_TEST, True)
    elif key == '-f' or key == "--"+K_FILE:
        return (K_FILE, True)
    else:
        return (K_HELP, False)

def print_help():
    print('''
    OPTIONS:
    -h or --help            -> Show this message.
    -f or --file            -> Name of file
    -s or --seed            -> Set seed value for random number generator.
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
                    print_help()
                    return
        else:
            global_options[option_key] = arg
            next_arg_is_value = False

