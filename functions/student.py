import json
import pathlib
from api.url import student_json_cn, student_json_en, student_json_jp, student_json_kr, student_json_tw

import urllib3


def get_student():
    """Get student data from SchaleDB."""
    http = urllib3.PoolManager()
    request = http.request('GET', 'https://lonqie.github.io/SchaleDB/data/cn/students.json')
    data = json.loads(request.data.decode('utf-8'))

    output_resource_path = pathlib.Path('test')

    with open(output_resource_path / 'students_cn.json', 'w', encoding='utf8') as fd:
        json.dump(data, fd, ensure_ascii=False, indent=4)
