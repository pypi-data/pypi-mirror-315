import os
from datetime import datetime

os.system("") #

class colors:

    RESET = "\033[0m"

    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    BLACK = "\033[30m\033[47m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    AQUA = "\033[36m"
    WHITE = "\033[37m"
    #GRAY = "\033[90m"

    LIGHT_RED = "\033[91m"
    LIGHT_GREEN = "\033[92m"
    LIGHT_YELLOW = "\033[93m"
    LIGHT_BLUE = "\033[94m"
    LIGHT_PURPLE = "\033[95m"
    LIGHT_AQUA = "\033[96m"
    LIGHT_WHITE = "\033[97m"

    BLACK_BG = "\033[40m"
    RED_BG = "\033[41m"
    GREEN_BG = "\033[42m"
    YELLOW_BG = "\033[43m"
    BLUE_BG = "\033[44m"
    PURPLE_BG = "\033[45m"
    CYAN_BG = "\033[46m"
    WHITE_BG = "\033[47m"

def _values_to_string(*values: object, sep: str = ' '): return sep.join([str(v) for v in values])

class Logger:

    def __init__(self, logs_path: str = '.polinv-logs') -> None:
        self.logs_path = logs_path

    def save_today_log(self, text: str):
        path = os.path.join(self.logs_path, 'today.log')
        with open(path, 'a', encoding='utf-8') as file: file.write(text)

    def log(self, text: str, color: str = colors.RESET, save: bool = False):
        log_time = datetime.now().strftime("%H:%M:%S")
        if save: self.save_today_log(log_time + ' > ' + text + '\n')
        print(f'{color}{text}{colors.RESET}')

    def error(self, text: str):
        log_time = datetime.now().strftime("%H:%M:%S")
        self.save_today_log('(error) -> ' + log_time + ' > ' + text + '\n')
        print(f'{colors.RED}(error) -> {colors.LIGHT_RED}' + text + f'{colors.RESET}')

    def info(self, *values: object, sep: str = ' ', save: bool = False): self.log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_AQUA, save)
    def success(self, *values: object, sep: str = ' ', save: bool = False): self.log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_GREEN, save)
    def primary(self, *values: object, sep: str = ' ', save: bool = False): self.log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_PURPLE, save)
    def warning(self, *values: object, sep: str = ' ', save: bool = False): self.log(f'(WARNING) {_values_to_string(*values, sep)}', colors.LIGHT_YELLOW, save)
    def danger(self, *values: object, sep: str = ' ', save: bool = False): self.log(f'(WARNING) {_values_to_string(*values, sep)}', colors.LIGHT_RED, save)

    def info_profile(self, profile: str, *values: object, sep: str = ' ', save: bool = False): self.info(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
    def success_profile(self, profile: str, *values: object, sep: str = ' ', save: bool = False): self.success(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
    def primary_profile(self, profile: str, *values: object, sep: str = ' ', save: bool = False): self.primary(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
    def warning_profile(self, profile: str, *values: object, sep: str = ' ', save: bool = False): self.warning(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
    def danger_profile(self, profile: str, *values: object, sep: str = ' ', save: bool = False): self.danger(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)

def save_today_log(text: str):
    path = os.path.join('.polinv-logs', 'today.log')
    with open(path, 'a', encoding='utf-8') as file: file.write(text)

def log(text: str, color: str = colors.RESET, save: bool = False):
    log_time = datetime.now().strftime("%H:%M:%S")
    if save: save_today_log(log_time + ' > ' + text + '\n')
    print(f'{color}{text}{colors.RESET}')

def error(text: str):
    log_time = datetime.now().strftime("%H:%M:%S")
    save_today_log('(error) -> ' + log_time + ' > ' + text + '\n')
    print(f'{colors.RED}(error) -> {colors.LIGHT_RED}' + text + f'{colors.RESET}')

def info(*values: object, sep: str = ' ', save: bool = False): log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_AQUA, save)
def success(*values: object, sep: str = ' ', save: bool = False): log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_GREEN, save)
def primary(*values: object, sep: str = ' ', save: bool = False): log(f'(INFO) {_values_to_string(*values, sep)}', colors.LIGHT_PURPLE, save)
def warning(*values: object, sep: str = ' ', save: bool = False): log(f'(WARNING) {_values_to_string(*values, sep)}', colors.LIGHT_YELLOW, save)
def danger(*values: object, sep: str = ' ', save: bool = False): log(f'(WARNING) {_values_to_string(*values, sep)}', colors.LIGHT_RED, save)

def info_profile(profile: str, *values: object, sep: str = ' ', save: bool = False): info(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
def success_profile(profile: str, *values: object, sep: str = ' ', save: bool = False): success(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
def primary_profile(profile: str, *values: object, sep: str = ' ', save: bool = False): primary(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
def warning_profile(profile: str, *values: object, sep: str = ' ', save: bool = False): warning(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
def danger_profile(profile: str, *values: object, sep: str = ' ', save: bool = False): danger(f'({profile}) -> {_values_to_string(*values, sep)}', sep=sep, save=save)
