import os
from pathlib import WindowsPath
import re
from pprint import pprint


def get_path() -> WindowsPath:
    path = WindowsPath(os.environ['USERPROFILE']).joinpath('AppData/Roaming/1C/1CEStart/ibases.v8i')
    if path.exists():
        return path


def get_ibases() -> dict:
    path = get_path()
    with open(path, 'r', encoding='utf-8-sig') as f:
        dct = {}
        sections = re.findall(r'\[[^\[]*', f.read())
        for section in sections:
            name, data = re.findall(r'\[(.*)\]([\w\W]*)', section)[0]
            result = re.findall(r'(\w*)=(.*)', data)
            dct[name] = {key: value for key, value in result}
        return dct


if __name__ == '__main__':
    ibases = get_ibases()
    pprint(ibases)
