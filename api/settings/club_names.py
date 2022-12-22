import pathlib

import yaml

current = pathlib.Path(__file__).parent.absolute()

club_name_setting_path = current.joinpath("..", "..", "settings", "club_names.yml")

with open(club_name_setting_path, "r", encoding="utf-8") as f:
    club_names = yaml.load(f, Loader=yaml.CLoader)
