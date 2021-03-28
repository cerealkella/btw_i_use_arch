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
    ( "BTW I use Arch. Er, well, actually Manjaro KDE." )
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
    click.echo("Let's install some stuff!")
    btw = Install()
    options = [f for f in dir(btw) if not f.startswith("_")]
    terminal_menu = TerminalMenu(
        options,
        # preview_command=f"Preview",
        preview_command=get_docstring,
        # multi_select=True,
        show_multi_select_hint=True,
    )
    menu_entry_indices = terminal_menu.show()
    print(menu_entry_indices)
    # print(terminal_menu.chosen_menu_entries)
    getattr(btw, terminal_menu.chosen_menu_entry)()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
