import pathlib

import click
from colorama import Fore

from functions.gen_student_names import gen_students_yml


@click.group()
def _root():
    """DataWeaver"""
    pass


@_root.command("update")
@click.option("--target", "-t", required=True)
@click.option("--image-path", "-i", required=False)
@click.option("--name-only", "-n", is_flag=True, default=False)
def _update(target: str, image_path: str, name_only: bool):
    """Update data"""
    from functions.student import get_student
    click.echo("Updating data")
    target_file_path = pathlib.Path(target)
    click.echo(f"{Fore.BLUE}Update data to [{target_file_path}]{Fore.RESET}")
    get_student(target_file_path, image_path, name_only)


@_root.command("generate-student-names")
@click.option("--target", "-t", default="settings/student_names.yml")
def _generate_student_names(target: str):
    """Generate student names"""
    click.echo("Generate student names")
    target_file_path = pathlib.Path(target)
    click.echo(f"{Fore.BLUE}Generate to [{target_file_path}]{Fore.RESET}")
    gen_students_yml(target_file_path)


if __name__ == '__main__':
    _root()
