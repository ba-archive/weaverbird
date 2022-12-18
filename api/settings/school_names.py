import yaml
import pathlib

current = pathlib.Path(__file__).parent.absolute()

school_name_setting_path = current.joinpath("..", "..", "settings", "club_names.yml")

with open(school_name_setting_path, "r", encoding="utf-8") as f:
    school_names = yaml.load(f, Loader=yaml.CLoader)
