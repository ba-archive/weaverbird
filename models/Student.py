from typing import Optional, List, Tuple

from pydantic import BaseModel, validator

diff_name_regex = r"(.*)[（\(](.*)[\)）]"
birthday_regex = r"(.*)月(.*)日"

class StudentName(BaseModel):
    cn: Optional[str] = ''
    jp: str
    en: Optional[str] = ''
    kr: Optional[str] = ''
    tw: Optional[str] = ''
    th: Optional[str] = ''


class Student(BaseModel):
    id: int = 0
    familyName: StudentName
    name: StudentName
    nickname: List[str] = []
    club: str = '无社团'
    affiliation: str = '无所属'
    birthday: Tuple[int, int] = (1, 1)
    rarity: int = 1
    type: str = 'Striker'
    armorType: str = 'LightArmor'
    bulletType: str = 'Pierce'
    weapon: str = 'AR'

    @validator("type")
    def validate_type(cls, validateValue):
        if validateValue not in ['Striker', 'Special']:
            raise ValueError(f"{validateValue} not in {['Striker', 'Special']}")
        return validateValue

    @validator("armorType")
    def validate_armor_type(cls, validateValue):
        if validateValue not in ['LightArmor', 'HeavyArmor', 'Unarmed', 'ElasticArmor']:
            raise ValueError(f"{validateValue} not in {['LightArmor', 'HeavyArmor', 'Unarmed', 'ElasticArmor']}")
        return validateValue

    @validator("bulletType")
    def validate_bullet_type(cls, validateValue):
        if validateValue not in ['Pierce', 'Explosion', 'Mystic']:
            raise ValueError(f"{validateValue} not in {['Pierce', 'Explosion', 'Mystic']}")
        return validateValue

    @validator("weapon")
    def validate_weapon(cls, validateValue):
        if validateValue not in ['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT', 'FT']:
            raise ValueError(f"{validateValue} not in {['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT', 'FT']}")
        return validateValue


class RawStudent(BaseModel):
    id: int = 0
    familyName: str = ''
    name: str = ''
    nickname: List[str] = []
    birthday: str = '1月1日'
    club: str = '无社团'
    affiliation: str = '无所属'
    rarity: int = 1
    type: str = 'Striker'
    armorType: str = 'LightArmor'
    bulletType: str = 'Pierce'
    weapon: str = 'AR'
    CollectionTexture: str = ''

    @validator("type")
    def validate_type(cls, validateValue):
        if validateValue not in ['Striker', 'Special']:
            raise ValueError(f"{validateValue} not in {['Striker', 'Special']}")
        return validateValue

    @validator("armorType")
    def validate_armor_type(cls, validateValue):
        if validateValue not in ['LightArmor', 'HeavyArmor', 'Unarmed', 'ElasticArmor']:
            raise ValueError(f"{validateValue} not in {['LightArmor', 'HeavyArmor', 'Unarmed', 'ElasticArmor']}")
        return validateValue

    @validator("bulletType")
    def validate_bullet_type(cls, validateValue):
        if validateValue not in ['Pierce', 'Explosion', 'Mystic']:
            raise ValueError(f"{validateValue} not in {['Pierce', 'Explosion', 'Mystic']}")
        return validateValue

    @validator("weapon")
    def validate_weapon(cls, validateValue):
        if validateValue not in ['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT', 'FT']:
            raise ValueError(f"{validateValue} not in {['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT', 'FT']}")
        return validateValue


class Avatar(BaseModel):
    id: int = 0
    avatarName: str = ''
