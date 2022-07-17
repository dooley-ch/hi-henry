# *******************************************************************************************
#  File:  commands.py
#
#  Created: 17-07-2022
#
#  History:
#  17-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['app']

from pathlib import Path

import click


# noinspection PyUnusedLocal
def show_file_details(ctx: click.Context, param: click.Option, value: bool) -> None:
    print('File List')
    ctx.exit()


# noinspection PyUnusedLocal
def _abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '--version', '-v')
def app() -> None:
    """
    This application generates DTO classes based on the given database structure
    """
    pass


@app.command()
@click.option('--files', is_flag=True, callback=show_file_details, expose_value=False, is_eager=True)
def setup() -> None:
    """
    This command configures the application
    """
    pass


@app.group()
def projects() -> None:
    """
    This set of commands manage the projects
    """
    pass


# region Project Commands

@projects.command("list")
def projects_list() -> None:
    """
    Lists the defined projects
    """
    pass


@projects.command("add")
@click.argument("name", type=click.STRING, required=True)
def projects_add(name: str) -> None:
    """
    Defines a new project

    NAME: The name of the project to add.
    """
    pass


@projects.command("edit")
@click.argument("name", type=click.STRING, required=True)
def projects_edit(name: str) -> None:
    """
    Edit an existing project

    NAME: The name of the project to edit.
    """
    pass


@projects.command("delete")
@click.argument("name", type=click.STRING, required=True)
def projects_delete(name: str) -> None:
    """
    Delete an existing project

    NAME: The name of the project to delete.
    """
    pass


# endregion

@app.group()
def code() -> None:
    """
    This set of commands handle the code generation process
    """
    pass


# region Code Commands


@code.command("generate")
@click.argument("name", type=click.STRING, required=True)
@click.option('--folder', '-f', 'folder', type=click.types.Path(file_okay=False, writable=True), required=False,
              help="The output folder")
@click.option('--yes', is_flag=True, callback=_abort_if_false, expose_value=False,
              prompt='Are you sure you want to generate code?', help="Confirm the wish to execute the command")
def code_generate(name: str, folder: Path) -> None:
    """
    Generates code for the given project

    NAME: The name of the project to use.

    If no folder is supplied, the current folder is assumed
    """
    pass


@code.command("clear")
@click.option('--folder', '-f', 'folder', type=click.types.Path(file_okay=False, writable=True, exists=True),
              required=False, help="The output folder")
@click.option('--yes', is_flag=True, callback=_abort_if_false, expose_value=False,
              prompt='Are you sure you want to delete the code?', help="Confirm the wish to execute the command")
def code_clear(folder: Path) -> None:
    """
    This command deletes the code in a folder.

    If no folder is supplied, the current folder is assumed
    """
    pass


@code.command("explore")
@click.argument("table", type=click.STRING, required=False)
def code_explore(table: str | None) -> None:
    """
    Allows the user to explore the generated code

    TABLE: The name of table to explore
    """
    pass

# endregion
