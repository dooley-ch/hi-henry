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
from datetime import datetime
from logging import Logger, getLogger
from pathlib import Path
import typer
import core.utils as utils
import core.custom_types as types
import core.generate as generate

app = typer.Typer(
    help="""This application extracts a database schema and generates a set of Pydantic classes representing 
    the tables in the database.""")


@app.command('create', help="This command creates a new project file.")
def create_project(
        database: str = typer.Argument(..., help="The name of the database to to base the code generation on."),
        user: str = typer.Argument(..., help="The user account to use to connect to the database."),
        password: str = typer.Argument(..., help="The user password to use to connect to the database."),
        driver: str = typer.Argument('mysql', help="The DBMS hosting the database."),
        host: str = typer.Argument('127.0.0.1', help="The host where the DBMS is running."),
        port: int = typer.Argument(3306, help="The port on which the DMBS is listening")) -> None:
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if file.exists():
        typer.echo(f"A project for the database: {database.lower()}, exists.")
        typer.Exit()

    now: datetime = datetime.now()
    now_str: str = now.strftime("%d-%m-%Y, %H:%M:%S")

    contents: list[str] = [
        f"# Hi-Henry Configuration File: {now_str}\n",
        f"HIH_DATABASE={database}\n",
        f"HIH_USER={user}\n",
        f"HIH_PASSWORD={password}\n",
        f"HIH_DRIVER={driver}\n",
        f"HIH_HOST={host}\n"
        f"HIH_PORT={port}"
    ]

    with open(file, 'w') as f:
        f.writelines(contents)

    log: Logger = getLogger()
    log.info(f"Project file created for: {database}")

    typer.echo('Project file created')


@app.command('delete', help="This command deletes an existing project.")
def delete_project(
        database: str = typer.Argument(..., help="The name of the database used to generate code.")) -> None:
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if not file.exists():
        typer.echo(f"No project file exists for the database: {database.lower()}.")
        typer.Exit()

    file.unlink()

    log: Logger = getLogger()
    log.info(f"Project file deleted: {database}")

    typer.echo('DFile deleted successfully')


@app.command('generate', help=" This command generates the code for the given database")
def generate_code(
        database: str = typer.Argument(..., help="The name of the database to use in generate the code."),
        folder: str = typer.Argument(None, help="If provided, code will be generated in this folder")) -> None:
    file: Path = utils.get_config_folder().joinpath(f"{database.lower()}.env")
    if not file.exists():
        typer.echo(f"No configuration file exists for the database: {database.lower()}.")
        typer.Exit()

    if typer.confirm('Are you sure you wish to generate code', default=True):
        # Ensure the output folder exists
        output_folder: Path = utils.get_output_folder()

        if folder:
            output_folder = pathlib.Path(folder)

        if not output_folder.exists():
            output_folder.mkdir(parents=True, exist_ok=True)

        # Get the connection info
        project: types.IProject = utils.get_config(file)

        # Generate code
        return generate.generate_code(project, output_folder)

    typer.echo('No code generated')


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
