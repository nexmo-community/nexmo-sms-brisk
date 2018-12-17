import click
from tinydb import TinyDB
from PyInquirer import prompt, Separator
from brisk.settings import questions_style

db = TinyDB("briskdb.json")
templates_db = db.table("templates")


@click.group()
def template():
    """Manages templates"""


@template.command("create")
def template_create():
    """Create a new template"""
    questions = [
        {"type": "input", "name": "name", "message": "Template name"},
        {
            "type": "editor",
            "name": "template",
            "message": "Template string",
            "eargs": {"editor": "default", "ext": ".txt"},
        },
    ]

    answers = prompt(questions, style=questions_style)
    templates_db.insert(answers)

    click.secho(
        f"New template {answers['name']} created", fg="black", bg="cyan", bold=True
    )


@template.command("list")
def template_list():
    """View all templates"""
    viewing_templates = True
    all_templates = templates_db.all()

    while viewing_templates:
        questions = [
            {
                "type": "list",
                "message": "View template",
                "name": "template",
                "choices": [
                    {"name": f"{template['name']}", "value": template}
                    for template in all_templates
                ],
            }
        ]

        answers = prompt(questions, style=questions_style)

        click.echo(answers["template"]["name"])
        click.echo("---")
        click.echo(answers["template"]["template"])

        if not click.confirm("View another template?"):
            viewing_templates = False


@template.command("remove")
def template_remove():
    """Delete one or more templates"""

    questions = [
        {
            "type": "checkbox",
            "qmark": "?",
            "message": "Select templates to delete",
            "name": "delete",
            "choices": [
                {"name": f"{template['name']}", "value": template.doc_id}
                for template in templates_db.all()
            ],
        }
    ]

    answers = prompt(questions, style=questions_style)
    templates_db.remove(doc_ids=answers["delete"])

    click.echo(f"Removed {len(answers['delete'])} template(s)")
