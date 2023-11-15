from os import system, name

from simple_term_menu import TerminalMenu

from terminaltables import AsciiTable, SingleTable

# define our clear function
def clear_term():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def format_title(title):
    title = '   ' + title + '   '
    return '\n' + title.center(70, '*') + '\n'


def prompt_ok():
    print('\n')
    terminal_menu = TerminalMenu(
        ['Valider'],
        menu_highlight_style=('standout', 'bg_purple'),
        # clear_screen=True,
        # title=content
        )

    return terminal_menu.show()


def display_table(args):
    table = SingleTable(args)
    table.inner_heading_row_border = False
    table.inner_row_border = True
    print(table.table)