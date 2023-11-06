from os import system, name

from simple_term_menu import TerminalMenu


# define our clear function
def clear_term():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def format_title(title):
    return '\n' + title.center(70, '*') + '\n'


def prompt_ok():
    terminal_menu = TerminalMenu(
        ['Valider'],
        menu_highlight_style=('standout', 'bg_purple'),
        # clear_screen=True,
        # title=content
        )

    return terminal_menu.show()