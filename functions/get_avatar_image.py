from models.Student import Avatar
from typing import List
import urllib3
import pathlib
import shutil
import click
from colorama import Fore
from webptools import cwebp
from webptools import grant_permission


def get_avatar_image(students: List[Avatar], image_output_path: pathlib.Path):
    raw_output_path = image_output_path.joinpath("avatar_raw")
    raw_output_path.mkdir(parents=True, exist_ok=True)
    image_output_path.mkdir(parents=True, exist_ok=True)

    http = urllib3.PoolManager()

    for student in students:
        id = student.id
        avatar_name = student.avatarName

        url = f'https://lonqie.github.io/SchaleDB/images/student/collection/{avatar_name}.webp'

        response = http.request('GET', url)

        with open(raw_output_path.joinpath(f'{id}.webp'), 'wb') as f:
            click.echo(f'{Fore.BLUE}Writing {id}.webp{Fore.RESET}')
            f.write(response.data)

    raw_files = list(raw_output_path.glob('*.webp'))
    grant_permission()

    for raw_file in raw_files:
        filename = raw_file.stem
        click.echo(
            f'{Fore.BLUE}Compressing {filename}.webp to {image_output_path.joinpath(f"{filename}.webp").as_posix()}')
        input_image = raw_file.as_posix()
        output_image = image_output_path.joinpath(f"{filename}.webp").as_posix()

        cwebp(input_image=input_image, output_image=output_image,
              option='-af -m 6 -mt -noalpha', logging="-v")

    click.echo(f'{Fore.BLUE}Deleting temporary directory {raw_output_path.as_posix()}{Fore.RESET}')
    shutil.rmtree(raw_output_path.as_posix())
