from typing import Optional, List
from pydantic import BaseModel, validator


class StudentName(BaseModel):
    cn: Optional[str] = ''
    jp: str
    en: Optional[str] = ''
    kr: Optional[str] = ''
    tw: Optional[str] = ''


class Student(BaseModel):
    id: int = 0
    familyName: StudentName
    name: StudentName
    nickname: List[str] = []
    club: str = '无社团'
    affiliation: str = '无所属'
    rarity: int = 1
    type: str = 'Striker'
    armorType: str = 'LightArmor'
    weapon: str = 'AR'

    @validator("type")
    def validate_type(cls, validateValue):
        if validateValue not in ['Striker', 'Special']:
            raise ValueError(f"{validateValue} not in {['Striker', 'Special']}")
        return validateValue

    @validator("armorType")
    def validate_armor_type(cls, validateValue):
        if validateValue not in ['LightArmor', 'HeavyArmor', 'Unarmed']:
            raise ValueError(f"{validateValue} not in {['LightArmor', 'HeavyArmor', 'Unarmed']}")
        return validateValue

    @validator("weapon")
    def validate_weapon(cls, validateValue):
        if validateValue not in ['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT']:
            raise ValueError(f"{validateValue} not in {['SG', 'SMG', 'AR', 'GL', 'HG', 'RL', 'SR', 'RG', 'MG', 'MT']}")
        return validateValue


class RawStudent(BaseModel):
    id: int = 0
    familyName: str = ''
    name: str = ''
    nickname: List[str] = []
    club: str = '无社团'
    affiliation: str = '无所属'
    rarity: int = 1
    type: str = 'Striker'
    armorType: str = 'LightArmor'
    weapon: str = 'AR'
