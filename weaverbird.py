import pathlib

import click
from colorama import Fore

from functions.student import get_student


@click.group()
def _root():
    """DataWeaver"""
    pass


@_root.command("update")
@click.option("--target", "-t", required=True)
def _update(target: str):
    """Update data"""
    click.echo("Updating data")
    target_file_path = pathlib.Path(target)
    click.echo(f"{Fore.BLUE}Update data to [{target_file_path}]{Fore.RESET}")
    get_student(target_file_path)


if __name__ == '__main__':
    _root()
