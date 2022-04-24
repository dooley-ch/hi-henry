# *******************************************************************************************
#  File:  command_line.py
#
#  Created: 16-04-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  16-04-2022: Initial version
#
# *******************************************************************************************

"""
This module implements the application command line features
"""

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"
__all__ = ['app']

import pathlib
from logging import Logger, getLogger
from pathlib import Path
from typing import List

import typer

import core.generate as generate
import core.project_config as project_config
import core.utils as utils

app = typer.Typer(
    help="""This application extracts a database schema and generates a set of Pydantic classes representing 
    the tables in the database.""")


@app.command('list', help="This command lists the defined projects.")
def list_projects() -> None:
    names: List[str] = project_config.get_project_list()

    if names:
        for name in names:
            typer.echo(name)
        return

    typer.echo('No projects found')


@app.command('generate', help=" This command generates the code for the given database")
def generate_code(
        name: str = typer.Argument(..., help="The name of project to use."),
        folder: str = typer.Argument(None, help="If provided, code will be generated in this folder")) -> None:

    project = project_config.get_project(name)
    output_folder: Path = utils.get_output_folder()

    if folder:
        output_folder = pathlib.Path(folder)

    if not output_folder.exists():
        output_folder.mkdir(parents=True, exist_ok=True)

    # Generate code
    if generate.generate_code(project, output_folder):
        typer.echo('Code generated.')
    else:
        typer.echo('No code generated, see log file for details.')


@app.command('clear', help="This command deletes the generated code")
def delete_code(folder: str = typer.Argument(None, help="If provided, code will be generated in this folder")) -> None:
    output_folder: Path = utils.get_output_folder()
    if folder:
        output_folder = folder
    if not output_folder.exists():
        typer.echo(f"Code folder not found: {output_folder}.")
        typer.Exit()

    # Makre sure there are files to delete
    files = list(output_folder.glob('*.py'))

    if files:
        if typer.confirm('Are you sure you wish to delete the code', default=True):
            for file in files:
                file.unlink()

    log: Logger = getLogger()
    log.info(f"Code deleted from folder: {output_folder}")

    typer.echo("No code files deleted.")
