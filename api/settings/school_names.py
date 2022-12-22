import pathlib

import yaml

current = pathlib.Path(__file__).parent.absolute()

school_name_setting_path = current.joinpath("..", "..", "settings", "school_names.yml")

with open(school_name_setting_path, "r", encoding="utf-8") as f:
    school_names = yaml.load(f, Loader=yaml.CLoader)
