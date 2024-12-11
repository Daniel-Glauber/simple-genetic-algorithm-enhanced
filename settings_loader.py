# Author: Daniel Glauber
# File: settings_loader.py
# Description: Contains functions to load settings from a settings file and command line arguments.
import re
from os.path import exists
from typing import Any, List

# Constants for magic numbers and strings
DEFAULT_YES = "y"
DEFAULT_NO = "n"
DEFAULT_SETTINGS_FILE = "gasettings.dat"
DEFAULT_RAND_SEED = 123
DEFAULT_POPULATION_SIZE = 46
DEFAULT_STRING_SIZE = 80
DEFAULT_PROB_APPLY_CROSSOVER = 0.6
DEFAULT_PROB_APPLY_MUTATION = 1.0
DEFAULT_SELECTION_METHOD = 0
DEFAULT_TOURNAMENT_SIZE = 2
DEFAULT_FITNESS_FUNCTION = 0
DEFAULT_TERMINATE_ON_FAILURE = 1
DEFAULT_FAILURES_BEFORE_TERMINATION = 0
DEFAULT_CROSSOVER_OPERATOR = 0
DEFAULT_BISECTION = 0
DEFAULT_BISECTION_THRESHOLD = 0.1
DEFAULT_BISECTION_STARTING_POPULATION = 10
DEFAULT_BISECTION_MAX_GENERATION = 50

SETTINGS_THAT_MUST_BE_ONE_OR_LESS = [
    "probApplyCrossover",
    "probApplyMutation",
    "bisectionThreshold"
]
SETTINGS_THAT_MUST_BE_TWO_OR_MORE = [
    "populationSizeN",
    "bisectionStartingPopulation",
    "bisectionMaxGeneration"
]
POSSIBLE_CROSSOVER_OPERATORS = [
    0, 1, 2
]
POSSIBLE_FITNESS_EQUATIONS = [
    0, 1
]
POSSIBLE_BISECTION_OPTIONS = [
    0, 1
]
POSSIBLE_SETTINGS_LOOKUP = {
    "bisection": POSSIBLE_BISECTION_OPTIONS,
    "crossoverOperator": POSSIBLE_CROSSOVER_OPERATORS,
    "fitnessFunction": POSSIBLE_FITNESS_EQUATIONS,
}
DEFAULT_SETTINGS = {
    "randSeed": DEFAULT_RAND_SEED,
    "populationSizeN": DEFAULT_POPULATION_SIZE,
    "stringSizeN": DEFAULT_STRING_SIZE,
    "probApplyCrossover": DEFAULT_PROB_APPLY_CROSSOVER,
    "probApplyMutation": DEFAULT_PROB_APPLY_MUTATION,
    "selectionMethod": DEFAULT_SELECTION_METHOD,
    "tournamentSizeK": DEFAULT_TOURNAMENT_SIZE,
    "fitnessFunction": DEFAULT_FITNESS_FUNCTION,
    "terminateOnFailure": DEFAULT_TERMINATE_ON_FAILURE,
    "failuresBeforeTermination": DEFAULT_FAILURES_BEFORE_TERMINATION,
    "crossoverOperator": DEFAULT_CROSSOVER_OPERATOR,
    "bisection": DEFAULT_BISECTION,
    "bisectionThreshold": DEFAULT_BISECTION_THRESHOLD,
    "bisectionStartingPopulation": DEFAULT_BISECTION_STARTING_POPULATION,
    "bisectionMaxGeneration": DEFAULT_BISECTION_MAX_GENERATION
}

ga_settings = {}
user_settings_file = DEFAULT_SETTINGS_FILE

def display_help_message() -> None:
    """
    Displays help message when user includes -h in command line arguments.
    """
    print("Simple GA Help Message")
    print("The command to run program is: python3 sga.py settings.dat")
    print("settings.dat is an optional argument to specify a custom settings file.")
    print("If you do not include a settings file the default settings file gasettings.dat is used.")
    print("To turn on limited debugging use command: python3 sga.py -g settings.dat")
    print("To turn on full debugging use command: python3 sga.py -G settings.dat")

def get_setting(key: str) -> Any:
    """
    Returns the value of key from settings.

    Args:
        key (str): The key to retrieve the value for.

    Returns:
        Any: The value associated with the key.
    """
    return ga_settings[key]

def set_setting(key: str, value: Any) -> None:
    """
    Sets the value for a given key in the settings.

    Args:
        key (str): The key to set the value for.
        value (Any): The value to set.
    """
    global ga_settings
    ga_settings[key] = value

def ask_user_continue_question(question: str, default: str = DEFAULT_YES) -> None:
    """
    Asks the user if they want to continue running the program or terminate.

    Args:
        question (str): The question to ask the user.
        default (str, optional): The default answer if the user just presses enter. Defaults to "y".
    """
    while True:
        user_response = input(f"{question}\n(default={default}) (y/n): ").strip().lower()
        if user_response in ["", "y", "yes"]:
            return
        elif user_response in ["n", "no"]:
            quit()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def create_default_settings_file(settings_file: str = DEFAULT_SETTINGS_FILE) -> None:
    """
    Creates the default settings file if it is missing.

    Args:
        settings_file (str, optional): The path to the settings file. Defaults to DEFAULT_SETTINGS_FILE.
    """
    try:
        lines = [f"{key} {value}" for key, value in DEFAULT_SETTINGS.items()]
        with open(settings_file, "w") as file:
            file.write('\n'.join(lines))
    except IOError as e:
        print(f"Error creating default settings file: {e}")
        quit()

def parse_settings_file(settings_file: str, default_settings_file: str = DEFAULT_SETTINGS_FILE) -> None:
    """
    Parses the settings file and verifies that the values are valid.

    Args:
        settings_file (str): The path to the settings file.
        default_settings_file (str, optional): The path to the default settings file. Defaults to DEFAULT_SETTINGS_FILE.
    """
    global ga_settings
    default_settings_needs_fix = False
    is_default_file = settings_file == default_settings_file
    finished_parsing = False
    saved_ga_settings = ga_settings.copy()  # Save current settings in case we need to revert
    while not finished_parsing:
        if default_settings_needs_fix:
            ga_settings = saved_ga_settings  # Revert to saved settings
            create_default_settings_file(default_settings_file)  # Create default settings file
            default_settings_needs_fix = False

        try:
            with open(settings_file) as file:
                for line in file:
                    split_line = re.split(r'\s+', line)  # Split line by whitespace
                    if len(split_line) > 1:
                        setting_with_error = split_line[0]
                        error_reason = ""
                        try:
                            # Check if stringSizeN is divisible by 4 when fitnessFunction is 1
                            if "stringSizeN" in ga_settings and "fitnessFunction" in ga_settings:
                                if (ga_settings["fitnessFunction"] == 1 and
                                        ga_settings["stringSizeN"] % 4 != 0):
                                    setting_with_error = "stringSizeN"
                                    error_reason = ("evenly divisible by 4 " +
                                                    "when using fitnessFunction 1")
                                    raise ValueError(error_reason)
                            # Validate settings that must be one or less
                            if split_line[0] in SETTINGS_THAT_MUST_BE_ONE_OR_LESS:
                                error_reason = (
                                    ("a decimal number that is" +
                                     " less than or equal 1.0"))
                                float_value = float(split_line[1])
                                if float_value > 1.0:
                                    raise ValueError(("Value cannot be" +
                                                      " greater than 1.0"))
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = float_value
                            # Validate settings that have specific possible values
                            elif split_line[0] in POSSIBLE_SETTINGS_LOOKUP:
                                integer = int(split_line[1])
                                if integer not in POSSIBLE_SETTINGS_LOOKUP[split_line[0]]:
                                    error_reason = ("one of the following values: " +
                                                    ", ".join([str(x)
                                                               for x in
                                                               POSSIBLE_SETTINGS_LOOKUP[split_line[0]]]))
                                    raise ValueError(error_reason)
                                elif (split_line[0] == "fitnessFunction" and
                                      integer == 1):
                                    if "stringSizeN" in ga_settings:
                                        if ga_settings["stringSizeN"] % 4 != 0:
                                            setting_with_error = "stringSizeN"
                                            error_reason = ("evenly divisible by 4 " +
                                                            "when using fitnessFunction 1")
                                            raise ValueError(error_reason)
                                        elif split_line[0] not in ga_settings:
                                            ga_settings[split_line[0]] = integer
                                elif split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = integer
                            # Validate settings that must be two or more
                            elif split_line[0] in SETTINGS_THAT_MUST_BE_TWO_OR_MORE:
                                error_reason = ("an integer that is" +
                                                " greater than or equal 2")
                                integer = int(split_line[1])
                                if integer < 2:
                                    raise ValueError(("Value cannot be" +
                                                      " less than 2"))
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = integer
                            else:
                                error_reason = "an integer"
                                integer = int(split_line[1])
                                if split_line[0] not in ga_settings:
                                    ga_settings[split_line[0]] = integer
                        except ValueError as ve:
                            if not is_default_file:
                                print(f"Error parsing settings file {settings_file}")
                                print(f"The value for {setting_with_error} must be {error_reason}")
                                user_question = (f"Do you want to continue with the default value for "
                                                 f"{setting_with_error} from {default_settings_file}?")
                                ask_user_continue_question(user_question)
                                finished_parsing = True
                            else:
                                default_settings_needs_fix = True
                                break
        except FileNotFoundError:
            print(f"Settings file {settings_file} not found.")
            if not is_default_file:
                user_question = (f"Do you want to use the default settings from {default_settings_file} instead?")
                ask_user_continue_question(user_question)
                finished_parsing = True
            else:
                default_settings_needs_fix = True
        except IOError as e:
            print(f"Error reading settings file {settings_file}: {e}")
            quit()

        if not default_settings_needs_fix:
            finished_parsing = True

def load_settings(argv: List[str], default_settings_file: str = DEFAULT_SETTINGS_FILE) -> None:
    """
    Reads command line arguments and loads settings.

    Args:
        argv (List[str]): The list of command line arguments.
        default_settings_file (str, optional): The path to the default settings file. Defaults to DEFAULT_SETTINGS_FILE.
    """
    global user_settings_file
    ga_settings["fullDebug"] = False
    ga_settings["limitedDebug"] = False
    if len(argv) > 1:
        if "-h" in argv:
            display_help_message()
            print("Stopped")
            quit()

        if "-g" in argv:
            ga_settings["limitedDebug"] = True
        if "-G" in argv:
            ga_settings["fullDebug"] = True

        if argv[-1] not in ["sga.py", "-h", "-g", "-G"]:
            user_settings_file = argv[-1]
    if not exists(default_settings_file):
        create_default_settings_file(default_settings_file)
    if user_settings_file != default_settings_file:
        if exists(user_settings_file):
            parse_settings_file(user_settings_file, default_settings_file)
        else:
            print(f"Could not find settings file {user_settings_file}")
            user_question = (f"Do you want to use the default settings from {default_settings_file} instead?")
            ask_user_continue_question(user_question)
    parse_settings_file(default_settings_file, default_settings_file)
