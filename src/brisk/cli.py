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
import os
import click
from tinydb import TinyDB, Query
from PyInquirer import style_from_dict, Token, prompt, Separator


db = TinyDB("briskdb.json")
contacts_db = db.table("contacts")

custom_style_2 = style_from_dict(
    {
        Token.Separator: "#6C6C6C",
        Token.QuestionMark: "#FF9D00 bold",
        # Token.Selected: '',  # default
        Token.Selected: "#5F819D",
        Token.Pointer: "#FF9D00 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#5F819D bold",
        Token.Question: "",
    }
)


def get_delivery_options(answers):
    options = ["bike", "car", "truck"]
    if answers["size"] == "jumbo":
        options.append("helicopter")
    return options


@click.group()
@click.version_option()
def main():
    """Brisk SMS
    Quickly send template based SMS to one or more recipients
    """


@main.group()
def contact():
    """Manages SMS contacts"""


@contact.command("create")
def contact_create():
    """Creates a new contact"""
    questions = [
        {"type": "input", "name": "name", "message": "Contact name"},
        {
            "type": "input",
            "name": "phonenumber",
            "message": "Contact phone number (E.164 international format)",
        },
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select diminutives (select at least 1)",
            "name": "diminutive",
            "choices": [
                Separator("= The Bros ="),
                {"name": "Bro"},
                {"name": "Buddy"},
                {"name": "Dude"},
                {"name": "Matey"},
                {"name": "Pal"},
                Separator("= The Sweethearts ="),
                {"name": "Baby"},
                {"name": "Bae"},
                {"name": "Darling"},
                {"name": "Sweetheart"},
                {"name": "Sugar"},
                Separator("= The Scots/Irish/Aussies ="),
                {"name": "Bawbag"},
                {"name": "Eejit"},
                {"name": "Fannybaws"},
                {"name": "Numpty"},
            ],
            "validate": lambda answer: "You must choose at least one diminutive."
            if len(answer) == 0
            else True,
        },
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select greetings (select at least 1)",
            "name": "greeting",
            "choices": [
                {"name": "Alright"},
                {"name": "Greetings"},
                {"name": "Hello"},
                {"name": "Hey"},
                {"name": "Hi"},
                {"name": "Oi"},
                {"name": "Wasssssup"},
                {"name": "Yo"},
            ],
            "validate": lambda answer: "You must choose at least one greeting."
            if len(answer) == 0
            else True,
        },
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select valediction (select at least 1)",
            "name": "valediction",
            "choices": [
                {"name": "Bye"},
                {"name": "Cya"},
                {"name": "Love you x"},
                {"name": "Peace"},
                {"name": "xox"},
            ],
            "validate": lambda answer: "You must choose at least one valediction."
            if len(answer) == 0
            else True,
        },
    ]

    answers = prompt(questions, style=custom_style_2)
    contacts_db.insert(answers)

    click.secho(
        f"New contact {answers['name']} created", fg="black", bg="cyan", bold=True
    )


@contact.command("list")
def contact_list():
    """List all contacts"""
    for contact in contacts_db.all():
        click.echo(f"{contact['name']} - {contact['phonenumber']}")


@contact.command("remove")
def contact_remove():
    """Delete one or more contacts"""

    questions = [
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select contacts to delete",
            "name": "delete",
            "choices": [
                {
                    "name": f"{contact['name']} - {contact['phonenumber']}",
                    "value": contact.doc_id,
                }
                for contact in contacts_db.all()
            ],
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    contacts_db.remove(doc_ids=answers["delete"])

    click.echo(f"Removed {len(answers)} contact(s)")
