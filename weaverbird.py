import click
from colorama import Fore
import pathlib

from functions.student import get_student


@click.group()
def _root():
    """DataWeaver"""
    pass


@_root.command("update")
@click.option("--source", "-s", required=True)
def _update(source: str):
    """Update data"""
    click.echo("Updating data")
    output_resource_path = pathlib.Path(source)
    output_resource_path.mkdir(parents=True, exist_ok=True)
    click.echo(f"{Fore.BLUE}Update data to [{output_resource_path}]{Fore.RESET}")
    get_student()


if __name__ == '__main__':
    _root()
