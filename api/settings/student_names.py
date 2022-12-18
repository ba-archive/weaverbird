import yaml
import pathlib

current = pathlib.Path(__file__).parent.absolute()

student_name_setting_path = current.joinpath("..", "..", "settings", "student_names.yml")

with open(student_name_setting_path, "r", encoding="utf-8") as f:
    student_names = yaml.load(f, Loader=yaml.CLoader)
