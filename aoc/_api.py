from typing import Union
import requests
from pathlib import Path
from datetime import datetime
import os

_SESSION_FILE_NAME = "session.txt"
_YEAR_FILE_NAME = "year.txt"


def _set_read_file(filename: str, default: str = None) -> Union[str, None]:
    try:
        with open(filename) as file:
            return file.read()
    except FileNotFoundError:
        if default:
            with open(filename, "w") as file:
                file.write(default)
                return default
        return None


SESSION = _set_read_file(_SESSION_FILE_NAME)
if not SESSION:
    SESSION = _set_read_file(
        _SESSION_FILE_NAME,
        input("Enter your session cookie: "))
assert SESSION is not None
SESSION = SESSION.strip()

YEAR = _set_read_file(_YEAR_FILE_NAME)
if not YEAR:
    YEAR = _set_read_file(
        _YEAR_FILE_NAME,
        str(datetime.now().year))
    assert YEAR is not None
YEAR = int(YEAR.strip())

def get_input(day: int, year: int = YEAR, overwrite: bool = False, sample: bool = False):
    """
    Usage:
    ```python
    import aoc
    data_rows = aoc.get_input(5).splitlines()
    ```python
    """

    if sample: 
        return get_sample_input(day, year, overwrite)
    else:
        return get_full_input(day, year, overwrite)

def get_full_input(day: int, year: int = YEAR, overwrite: bool = False):

    path_str = os.path.join(f'AdventofCode{YEAR}','data')
    Path(path_str).mkdir(exist_ok=True)

    file_name = f"{year}_{day}.txt"
    file_path = os.path.join(path_str, file_name)
    data = None if overwrite else _set_read_file(file_path)
    if not data:
        response = requests.get(
                f"https://adventofcode.com/{year}/day/{day}/input",
                cookies={"session": SESSION})
        if not response.ok:
            if response.status_code == 404:
                raise FileNotFoundError(response.text)
            raise RuntimeError(f"Request failed, code: {response.status_code}, message: {response.content}")
        data = _set_read_file(
            file_path,
            response.text[:-1])
    if data is None:
        raise FileNotFoundError(f"Data could not be fetched for day {day}")
    return data

def get_multiline_input():
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        lines.append(line)
    return '\n'.join(lines)

def get_sample_input(day: int, year: int = YEAR, overwrite: bool = False):
    path_str = os.path.join(f'AdventofCode{YEAR}','data')
    Path(path_str).mkdir(exist_ok=True)

    file_name = f"sample_{year}_{day}.txt"
    file_path = os.path.join(path_str, file_name)
    data = None if overwrite else _set_read_file(file_path)
    if not data:
        print("Enter sample data, then press Ctrl-Z and Enter to finish: ")
        data = _set_read_file(file_path, get_multiline_input())

    if data is None:
        raise FileNotFoundError(f"Sample data could not be fetched for day {day}")
    return data