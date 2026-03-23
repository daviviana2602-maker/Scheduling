# ==============================
# INPUT VALIDATION MODULE
# Reusable functions for user input handling and validation
# ==============================

from datetime import datetime
from colorama import Fore, Style, init
init()



# ==============================
# INTERNAL UTILITIES
# ==============================

def _print_error(msg, use_color):
    if use_color:
        print(Fore.RED + msg + Style.RESET_ALL)
    else:
        print(msg)




# ==============================
# TEXT INPUT FUNCTIONS
# ==============================

# ------------------------------
# Accept only alphabetic input (letters and spaces)
# Example: 'Blue Shirt'
# ------------------------------
def input_alpha(msg, error_msg = 'Invalid value.', case = 'title', use_color = False):
    while True:
        value = input(msg).strip()

        if case == 'title':
            value = value.title()
        elif case == 'upper':
            value = value.upper()
        elif case == 'lower':
            value = value.lower()
        elif case == 'capitalize':
            value = value.capitalize()

        if value.replace(' ', '').isalpha():
            return value

        _print_error(error_msg, use_color)




# ------------------------------
# Accept non-empty input
# ------------------------------
def input_non_empty(msg, error_msg = 'Invalid value.', case = 'title', use_color = False):
    while True:
        value = input(msg).strip()
        if value:
            
            if case == 'title':
                value = value.title()
            elif case == 'upper':
                value = value.upper()
            elif case == 'lower':
                value = value.lower()
            elif case == 'capitalize':
                value = value.capitalize()
            
            return value

        _print_error(error_msg, use_color)




# ==============================
# NUMERIC INPUT FUNCTIONS
# ==============================

# ------------------------------
# Accept integer with optional range validation
# ------------------------------
def input_int(msg, min_value = None, max_value = None, error_msg = 'Invalid number.', use_color = False):
    while True:
        try:
            value = int(input(msg))

            if min_value is not None and value < min_value:
                _print_error(error_msg, use_color)
                continue

            if max_value is not None and value > max_value:
                _print_error(error_msg, use_color)
                continue

            return value

        except ValueError:
            _print_error(error_msg, use_color)




# ------------------------------
# Accept float with optional range validation
# ------------------------------
def input_float(msg, min_value = None, max_value = None, error_msg = 'Invalid number.', use_color = False):
    while True:
        try:
            value = float(input(msg))

            if min_value is not None and value < min_value:
                _print_error(error_msg, use_color)
                continue

            if max_value is not None and value > max_value:
                _print_error(error_msg, use_color)
                continue

            return value

        except ValueError:
            _print_error(error_msg, use_color)




# ==============================
# DATE INPUT FUNCTIONS
# ==============================

# ------------------------------
# Accept date in DD/MM/YYYY format
# ------------------------------
def input_date(msg, error_msg = 'Invalid date. Use DD/MM/YYYY', use_color = False):
    while True:
        try:
            value = input(msg).strip()
            return datetime.strptime(value, '%d/%m/%Y').date()

        except ValueError:
            _print_error(error_msg, use_color)




# ------------------------------
# Accept a valid date range
# ------------------------------
def input_date_range(start_msg = 'Start date (DD/MM/YYYY): ', end_msg = 'End date (DD/MM/YYYY): ', format_error_msg = 'Invalid date. Use DD/MM/YYYY.',
                    range_error_msg = 'End date must be after start date.', use_color = False):
    while True:
        try:
            start_str = input(start_msg).strip()
            start = datetime.strptime(start_str, '%d/%m/%Y').date()
        except ValueError:
            _print_error(format_error_msg, use_color)
            continue

        try:
            end_str = input(end_msg).strip()
            end = datetime.strptime(end_str, '%d/%m/%Y').date()
        except ValueError:
            _print_error(format_error_msg, use_color)
            continue

        if end < start:
            _print_error(range_error_msg, use_color)
            continue

        return start, end




# ==============================
# CONTROL / SELECTION FUNCTIONS
# ==============================

# ------------------------------
# Confirmation input (yes/no)
# ------------------------------
def get_confirm(msg = 'Continue? (yes/no): ', yes = 'yes', no = 'no', error_msg = 'Invalid option.', use_color = False):
    while True:
        value = input(msg).strip().lower()

        if value == yes:
            return True
        elif value == no:
            return False

        _print_error(error_msg, use_color)
    



# ------------------------------
# Select from valid numeric options
# ------------------------------
def input_choice(msg, valid_options, error_msg = 'Invalid option.', use_color = False):
    while True:
        try:
            value = int(input(msg))

            if value in valid_options:
                return value

        except ValueError:
            pass

        _print_error(error_msg, use_color)