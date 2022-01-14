"""Console script for btw_i_use_arch."""
import sys
import click
from datetime import date
from simple_term_menu import TerminalMenu
from .btw_i_use_arch import Install


def get_docstring(function_name, obj=Install()):
    return getattr(obj, function_name).__doc__


@click.command()
def main(args=None):
    """Console script for btw_i_use_arch."""
    click.echo(
        """
    ( "BTW I use Arch" )
        o   ^__^
         o  (oo)\_______
            (__)\       )\/
                ||----w |
                ||     ||
    """
    )
    click.echo("computer, what year is it?")
    click.echo(f"> Beep boop. {date.today().year}.")
    click.echo(f"{date.today().year} is the year of the Linux Desktop!")
    click.echo("Let's install/configure some stuff!")
    btw = Install()
    options = [f for f in dir(btw) if not f.startswith("_")]
    options.sort()
    do_stuff = True
    while do_stuff:
        terminal_menu = TerminalMenu(
            options,
            # preview_command=f"Preview",
            preview_command=get_docstring,
            # multi_select=True,
            show_multi_select_hint=True,
        )
        terminal_menu.show()
        if getattr(btw, terminal_menu.chosen_menu_entry)() == -1:
            break
        print("Configure/install more stuff?")
        terminal_menu = TerminalMenu(['Yes', 'No'])
        terminal_menu.show()
        do_stuff = terminal_menu.chosen_menu_entry == 'Yes'
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
