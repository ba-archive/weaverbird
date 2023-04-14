import json
import pathlib
import re
from typing import Tuple

import click
import urllib3
import yaml
from colorama import Fore

from api.settings.club_names import club_names
from api.settings.school_names import school_names
from api.settings.student_names import student_names
from api.url import student_json_en, student_json_jp, student_json_kr, student_json_tw, student_json_th
from functions.get_avatar_image import get_avatar_image
from models.Student import RawStudent, Student, StudentName, Avatar, diff_name_regex, birthday_regex

http = urllib3.PoolManager()

isTest = False


def get_student(target_file_path: pathlib.Path, name_only: bool):
    """Get student data from SchaleDB."""

    def transform_student_type(raw_type: str) -> str:
        types = {
            "Main": "Striker",
            "Support": "Special",
        }
        return types[raw_type]

    def get_student_json(url: str, language: str = 'cn', isTest: bool = False):
        if isTest:
            with open(f"test/data_{language}.json", "r", encoding="utf-8") as f:
                response_raw = json.load(f)
        else:
            response = http.request('GET', url)
            response_raw = json.loads(response.data.decode('utf-8'))
        data = []
        for student_raw in response_raw:
            student = RawStudent(
                id=student_raw['Id'],
                familyName=student_raw['FamilyName'],
                name=student_raw['Name'],
                nickname=[],
                birthday=student_raw['Birthday'],
                club=student_raw['Club'],
                affiliation=student_raw['School'],
                rarity=student_raw['StarGrade'],
                type=transform_student_type(student_raw['SquadType']),
                armorType=student_raw['ArmorType'],
                bulletType=student_raw['BulletType'],
                weapon=student_raw['WeaponType'],
                CollectionTexture=student_raw['CollectionTexture'],
            )
            data.append({
                "id": student.id,
                "familyName": student.familyName,
                "name": student.name,
                "nickname": student.nickname,
                "birthday": student.birthday,
                "club": student.club,
                "affiliation": student.affiliation,
                "rarity": student.rarity,
                "type": student.type,
                "armorType": student.armorType,
                "bulletType": student.bulletType,
                "weapon": student.weapon,
                "CollectionTexture": student.CollectionTexture,
            })
        return data

    # noinspection PyShadowingNames
    def read_target_data(target_file_path: pathlib.Path):
        try:
            with open(target_file_path, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.CLoader)
        except FileNotFoundError:
            return []
        except Exception as e:
            raise e

    def find_student_name(name_jp: str = '') -> str:
        candidate = next((x for x in student_names if x['stringJP'] == name_jp), None)
        if candidate is not None:
            return candidate['stringCN']
        click.echo(f'{Fore.YELLOW}{name_jp}, CN name not found !{Fore.RESET}')
        return name_jp

    def find_student_school_name(code: str) -> str:
        candidate = next((x for x in school_names if x['code'] == code), None)
        if candidate is not None:
            return candidate['cn']
        print(f"School name not found: {code}")
        return code

    def find_student_club_name(code: str) -> str:
        candidate = next((x for x in club_names if x['code'] == code), None)
        if candidate is not None:
            return candidate['cn']
        return code

    def get_student_birthday(birthday: str) -> Tuple[int, int]:
        reg_match = re.findall(birthday_regex, birthday)
        if len(reg_match) == 0:
            raise ValueError(f"Invalid birthday format: {birthday}")
        return int(reg_match[0][0]), int(reg_match[0][1])

    def handle_diff_student(name: str):
        reg_match = re.findall(diff_name_regex, name)
        if len(reg_match) == 0:
            return None
        return reg_match[0]

    data_jp = get_student_json(student_json_jp, 'jp', isTest=isTest)
    data_jp_sorted = sorted(data_jp, key=lambda x: x['id'])
    # (未使用) data_cn = get_student_json(student_json_cn, 'cn', isTest=isTest)
    data_en = get_student_json(student_json_en, 'en', isTest=isTest)
    data_kr = get_student_json(student_json_kr, 'kr', isTest=isTest)
    data_tw = get_student_json(student_json_tw, 'tw', isTest=isTest)
    data_th = get_student_json(student_json_th, 'th', isTest=isTest)

    data_outdated = read_target_data(target_file_path)

    data_latest = []

    avatar_latest = []

    # 假定日服数据总是最新
    for student_jp in data_jp_sorted:
        student_id = student_jp['id']
        student_family_name_jp = student_jp['familyName'] or ''
        student_name_jp = student_jp['name'] or ''
        student_avatar = student_jp['CollectionTexture']
        student_object_old = next((x for x in data_outdated if x['id'] == student_id), {})

        student_name_match = handle_diff_student(student_name_jp)
        if student_name_match is None:
            student_name_cn = find_student_name(student_name_jp)
        else:
            name = find_student_name(student_name_match[0])
            name_diff = find_student_name(student_name_match[1])
            student_name_cn = f"{name}({name_diff})"

        avatar_jp = Avatar(
            id=student_id,
            avatarName=student_avatar,
        )
        avatar_latest.append(avatar_jp)

        student_latest = Student(
            id=student_jp['id'],
            familyName=StudentName(
                cn=find_student_name(student_family_name_jp),
                jp=student_family_name_jp,
                en=next((x['familyName'] for x in data_en if x['id'] == student_id), student_family_name_jp),
                kr=next((x['familyName'] for x in data_kr if x['id'] == student_id), student_family_name_jp),
                tw=next((x['familyName'] for x in data_tw if x['id'] == student_id), student_family_name_jp),
                th=next((x['familyName'] for x in data_th if x['id'] == student_id), student_family_name_jp),
            ),
            name=StudentName(
                cn=student_name_cn,
                jp=student_name_jp,
                en=next((x['name'] for x in data_en if x['id'] == student_id), student_name_jp),
                kr=next((x['name'] for x in data_kr if x['id'] == student_id), student_name_jp),
                tw=next((x['name'] for x in data_tw if x['id'] == student_id), student_name_jp),
                th=next((x['name'] for x in data_th if x['id'] == student_id), student_name_jp),
            ),
            nickname=student_object_old['nickname'] if student_object_old else [],
            birthday=get_student_birthday(student_jp['birthday']),
            club=find_student_club_name(student_jp['club']),
            affiliation=find_student_school_name(student_jp['affiliation']),
            rarity=student_jp['rarity'],
            type=student_jp['type'],
            armorType=student_jp['armorType'],
            bulletType=student_jp['bulletType'],
            weapon=student_jp['weapon'],
        )

        student_data_latest = {
            "id": student_latest.id,
            "familyName": {
                "cn": student_latest.familyName.cn,
                "jp": student_latest.familyName.jp,
                "en": student_latest.familyName.en,
                "kr": student_latest.familyName.kr,
                "tw": student_latest.familyName.tw,
                "th": student_latest.familyName.th,
            },
            "name": {
                "cn": student_latest.name.cn,
                "jp": student_latest.name.jp,
                "en": student_latest.name.en,
                "kr": student_latest.name.kr,
                "tw": student_latest.name.tw,
                "th": student_latest.name.th,
            },
            "nickname": student_latest.nickname,
            "birthday": {
                "month": student_latest.birthday[0],
                "day": student_latest.birthday[1],
            },
            "club": student_latest.club,
            "affiliation": student_latest.affiliation,
            "rarity": student_latest.rarity,
            "type": student_latest.type,
            "armorType": student_latest.armorType,
            "bulletType": student_latest.bulletType,
            "weapon": student_latest.weapon,
        }
        data_latest.append(student_data_latest)

    with open(target_file_path, "w", encoding="utf-8") as f:
        yaml.dump(data_latest, f, allow_unicode=True, sort_keys=False, Dumper=yaml.CDumper)

    image_output_path = target_file_path.parent / 'image' / 'avatar_students'

    if not name_only:
        get_avatar_image(avatar_latest, image_output_path)

    click.echo("Done.")
