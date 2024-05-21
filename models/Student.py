from typing import Optional, List, Tuple

from pydantic import BaseModel, validator

diff_name_regex = r"(.*)[（\(](.*)[\)）]"
birthday_regex = r"(.*)月(.*)日"

tactic_type = ["Striker", "Special"]
armor_type = ["LightArmor", "HeavyArmor", "Unarmed", "ElasticArmor"]
bullet_type = ["Pierce", "Explosion", "Mystic", "Sonic"]
weapon_type = ["SG", "SMG", "AR", "GL", "HG", "RL", "SR", "RG", "MG", "MT", "FT"]


class StudentName(BaseModel):
    cn: Optional[str] = ""
    jp: str
    en: Optional[str] = ""
    kr: Optional[str] = ""
    tw: Optional[str] = ""
    th: Optional[str] = ""


class Student(BaseModel):
    id: int = 0
    familyName: StudentName
    name: StudentName
    nickname: List[str] = []
    nicknameFrom: Optional[int] = 0
    club: str = "无社团"
    clubCode: str = ""
    affiliation: str = "无所属"
    schoolCode: str = ""
    birthday: Tuple[int, int] = (1, 1)
    rarity: int = 1
    type: str = "Striker"
    armorType: str = "LightArmor"
    bulletType: str = "Pierce"
    weapon: str = "AR"

    @validator("type")
    def validate_type(cls, validateValue):
        if validateValue not in tactic_type:
            raise ValueError(f"Tactic type {validateValue} not in {tactic_type}")
        return validateValue

    @validator("armorType")
    def validate_armor_type(cls, validateValue):
        if validateValue not in armor_type:
            raise ValueError(f"Armor type {validateValue} not in {armor_type}")
        return validateValue

    @validator("bulletType")
    def validate_bullet_type(cls, validateValue):
        if validateValue not in bullet_type:
            raise ValueError(f"Bullet type {validateValue} not in {bullet_type}")
        return validateValue

    @validator("weapon")
    def validate_weapon(cls, validateValue):
        if validateValue not in weapon_type:
            raise ValueError(f"Weapon type {validateValue} not in {weapon_type}")
        return validateValue


class RawStudent(BaseModel):
    id: int = 0
    familyName: str = ""
    name: str = ""
    nickname: List[str] = []
    birthday: str = "1月1日"
    club: str = "无社团"
    affiliation: str = "无所属"
    rarity: int = 1
    type: str = "Striker"
    armorType: str = "LightArmor"
    bulletType: str = "Pierce"
    weapon: str = "AR"
    CollectionTexture: int = 10000

    @validator("type")
    def validate_type(cls, validateValue):
        if validateValue not in tactic_type:
            raise ValueError(f"Tactic type {validateValue} not in {tactic_type}")
        return validateValue

    @validator("armorType")
    def validate_armor_type(cls, validateValue):
        if validateValue not in armor_type:
            raise ValueError(f"Armor type {validateValue} not in {armor_type}")
        return validateValue

    @validator("bulletType")
    def validate_bullet_type(cls, validateValue):
        if validateValue not in bullet_type:
            raise ValueError(f"Bullet type {validateValue} not in {bullet_type}")
        return validateValue

    @validator("weapon")
    def validate_weapon(cls, validateValue):
        if validateValue not in weapon_type:
            raise ValueError(f"Weapon type {validateValue} not in {weapon_type}")
        return validateValue


class Avatar(BaseModel):
    id: int = 0
    avatarName: int = 10000
