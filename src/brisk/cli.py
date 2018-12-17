"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mbrisk` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``brisk.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``brisk.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import click
from brisk.contacts import contact


@click.group()
@click.version_option()
def main():
    """Brisk SMS
    Quickly send template based SMS to one or more recipients
    """


main.add_command(contact)
