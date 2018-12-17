import os
import click
import random
from tinydb import TinyDB
from PyInquirer import prompt, Separator
from jinja2 import Template
import nexmo
from brisk.settings import questions_style


db = TinyDB("briskdb.json")
contacts_db = db.table("contacts")
templates_db = db.table("templates")
nexmo_client = nexmo.Client(
    key=os.environ["NEXMO_KEY"], secret=os.environ["NEXMO_SECRET"]
)


@click.command()
def send():
    """Send SMS"""

    questions = [
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select contacts to message",
            "name": "contacts",
            "choices": [
                {
                    "name": f"{contact['name']} - {contact['phonenumber']}",
                    "value": contact,
                }
                for contact in contacts_db.all()
            ],
            "validate": lambda answer: "You must choose at least one contact."
            if len(answer) == 0
            else True,
        },
        {
            "type": "list",
            "message": "Select template",
            "name": "template",
            "choices": [
                {"name": f"{template['name']}", "value": template["template"]}
                for template in templates_db.all()
            ],
        },
    ]

    answers = prompt(questions, style=questions_style)
    template = Template(answers["template"])

    with click.progressbar(answers["contacts"], label="Sending messages") as contacts:
        for contact in contacts:
            message = template.render(
                name=contact["name"],
                phonenumber=contact["phonenumber"],
                diminutive=random.choice(contact["diminutive"]),
                greeting=random.choice(contact["greeting"]),
                valediction=random.choice(contact["valediction"]),
            )

            nexmo_client.send_message(
                {
                    "from": os.environ["MY_NUMBER"],
                    "to": contact["phonenumber"],
                    "text": message,
                }
            )
