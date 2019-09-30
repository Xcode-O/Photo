# -*- coding: utf-8 -*-

from enum import Enum

token = "935353731:AAHukB283QDutqiq7uq7rYetrQpyM2OudkE"
db_file = "database.vdb"
photo_path = '/Users/dmytro/Documents/images/telebotIMG/'

class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_TEXT = "1"
    S_SET_PICK = "2"
    S_ENTER_NAME = "3"

