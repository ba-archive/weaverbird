import json
import pathlib
import re

import click
import urllib3
import yaml
from colorama import Fore

from api.url import student_json_cn, student_json_jp
from models.Student import RawStudent

http = urllib3.PoolManager()

regex_str = r"(.*)[（\(](.*)[\)）]"


def gen_students_yml(target_file_path: pathlib.Path):
    def get_student_json(url: str):
        response = http.request('GET', url)
        response_raw = json.loads(response.data.decode('utf-8'))
        data = []
        for student_raw in response_raw:
            student = RawStudent(
                id=student_raw['Id'],
                familyName=student_raw['FamilyName'],
                name=student_raw['Name'],
                # nickname=[],
                # club=student_raw['Club'],
                # affiliation=student_raw['School'],
                # rarity=student_raw['StarGrade'],
                # type=transform_student_type(student_raw['SquadType']),
                # armorType=student_raw['ArmorType'],
                # bulletType=student_raw['BulletType'],
                # weapon=student_raw['WeaponType'],
                # CollectionTexture=student_raw['CollectionTexture'],
            )
            data.append({
                "id": student.id,
                "familyName": student.familyName,
                "name": student.name,
                # "nickname": student.nickname,
                # "club": student.club,
                # "affiliation": student.affiliation,
                # "rarity": student.rarity,
                # "type": student.type,
                # "armorType": student.armorType,
                # "bulletType": student.bulletType,
                # "weapon": student.weapon,
                # "CollectionTexture": student.CollectionTexture,
            })
        return data

    def handle_diff_student(name: str):
        reg_match = re.findall(regex_str, name)
        if len(reg_match) == 0:
            return None
        return reg_match[0]

    def data_exist(array, string: str):
        for item in array:
            if item['stringJP'] == string:
                return True
        return False

    data_jp = get_student_json(student_json_jp)
    # data_jp_sorted = sorted(data_jp, key=lambda x: x['id'])
    data_cn = get_student_json(student_json_cn)
    student_data = []

    for student_jp in data_jp:
        student_id = student_jp['id']
        student_family_name_jp = student_jp['familyName']
        student_name_jp = student_jp['name']

        if len(student_family_name_jp) == 0 or len(student_name_jp) == 0:
            click.echo(f'{Fore.RED}ID:{student_id}, JP name is empty !{Fore.RESET}')
            print(student_family_name_jp, student_name_jp)
            continue

        for student_cn in data_cn:
            if student_cn['id'] == student_id:
                student_family_name_cn = student_cn['familyName']
                student_name_cn = student_cn['name']

                if len(student_family_name_cn) == 0 or len(student_name_cn) == 0:
                    click.echo(f'{Fore.RED}ID:{student_id}, CN name is empty !{Fore.RESET}')
                    break

                match_jp = handle_diff_student(student_name_jp)
                match_cn = handle_diff_student(student_name_cn)
                if match_jp is None or match_cn is None:
                    if not data_exist(student_data, student_name_jp):
                        student_data_item = {
                            "stringJP": student_name_jp,
                            "stringCN": student_name_cn,
                        }
                        student_data.append(student_data_item)
                else:
                    if not data_exist(student_data, match_jp[1]):
                        student_data_item = {
                            "stringJP": match_jp[1],
                            "stringCN": match_cn[1],
                        }
                        student_data.append(student_data_item)
                if not data_exist(student_data, student_family_name_jp):
                    student_data_item = {
                        "stringJP": student_family_name_jp,
                        "stringCN": student_family_name_cn,
                    }
                    student_data.append(student_data_item)
                break

    with open(target_file_path, "w", encoding="utf-8") as f:
        yaml.dump(student_data, f, allow_unicode=True, sort_keys=False, Dumper=yaml.CDumper)

    click.echo("Done.")
