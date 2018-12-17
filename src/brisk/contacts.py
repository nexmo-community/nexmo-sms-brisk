import click
from tinydb import TinyDB
from PyInquirer import prompt, Separator
from brisk.settings import questions_style

db = TinyDB("briskdb.json")
contacts_db = db.table("contacts")


@click.group()
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

    answers = prompt(questions, style=questions_style)
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

    answers = prompt(questions, style=questions_style)
    contacts_db.remove(doc_ids=answers["delete"])

    click.echo(f"Removed {len(answers['delete'])} contact(s)")
