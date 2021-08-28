import json
import re
from typing import List, TypedDict

from pkg_resources import resource_filename

from rh_test.util.singleton import Singleton

ColorName = str
RGBHexValue = str


class Color(TypedDict):
    color: ColorName
    value: RGBHexValue


class ColorManager(metaclass=Singleton):
    hex_color_re = re.compile(r'^#(?:[A-Fa-f0-9]{3}){1,2}$')

    def __init__(self):
        self._color_db = None
        self.load_from_json()

    def load_from_json(self):
        with open(resource_filename('rh_test', 'resources/colors.json')) as file:
            # TODO: validate/warn about duplicated keys (include cases like #000 and #000000)
            self._color_db = {color['value']: Color(**color) for color in json.load(file)}

    def delete_all(self):
        self._color_db = {}

    def get_all_colors(self) -> List[Color]:
        return list(self._color_db.values())

    def get_color_by_value(self, value: RGBHexValue) -> Color:
        try:
            return self._color_db[value]
        except KeyError:
            raise ColorDoesNotExistException(f"Color '{value}' does not exist")

    def insert_color(self, color: ColorName, value: RGBHexValue) -> Color:
        if value in self._color_db:
            raise ColorAlreadyExistsException(f"Color with value '{value}' already exits. "
                                              f"Color: '{self._color_db[value]['color']}'")
        inserted = Color(color=color, value=value)
        self._color_db[value] = inserted
        return inserted

    @classmethod
    def convert_hex_color(cls, value: str) -> RGBHexValue:
        if cls.hex_color_re.match(value):
            return value
        raise ValueError(f"Value '{value}' does not match the RGB hex color pattern")


class ColorAlreadyExistsException(Exception):
    pass


class ColorDoesNotExistException(Exception):
    pass
