"""Color model - contains all classes and types needed to handle colors"""
import json
import re
from typing import List, TypedDict

from pkg_resources import resource_filename

from rh_test.util.singleton import Singleton

ColorName = str
RGBHexValue = str


class Color(TypedDict):
    """Alias type of dict"""
    color: ColorName
    value: RGBHexValue


class ColorManager(metaclass=Singleton):
    """Manage color database"""
    hex_color_re = re.compile(r'^#(?:[A-Fa-f0-9]{3}){1,2}$')

    def __init__(self):
        self._color_db = None
        self.load_from_json()

    def load_from_json(self):
        """Fill the database from provided json"""
        filename = resource_filename('rh_test', 'resources/colors.json')
        with open(filename, encoding='utf-8') as file:
            # TODO: validate/warn about duplicated keys (include cases like #000 and #000000)
            self._color_db = {color['value']: Color(**color) for color in json.load(file)}

    def delete_all(self):
        """Empty the database"""
        self._color_db = {}

    def get_all_colors(self) -> List[Color]:
        """Return all colors on database"""
        return list(self._color_db.values())

    def get_color_by_value(self, value: RGBHexValue) -> Color:
        """Return a color from database using its hex value as key"""
        try:
            return self._color_db[value]
        except KeyError as exception:
            raise ColorDoesNotExistException(f"Color '{value}' does not exist") from exception

    def get_color_by_name(self, color_name: ColorName) -> Color:
        """Return a color from database using its name as key"""
        for color in self._color_db.values():
            if color['color'] == color_name:
                return color

        raise ColorDoesNotExistException(f"Color '{color_name}' does not exist")

    def insert_color(self, color: ColorName, value: RGBHexValue) -> Color:
        """Create a color and inserts it on database"""
        if value in self._color_db:
            raise ColorAlreadyExistsException(f"Color with value '{value}' already exits. "
                                              f"Color: '{self._color_db[value]['color']}'")
        inserted = Color(color=color, value=value)
        self._color_db[value] = inserted
        return inserted

    @classmethod
    def convert_hex_color(cls, value: str) -> RGBHexValue:
        """Make sure that the value string matches the RGB hex pattern"""
        if cls.hex_color_re.match(value):
            return value
        raise ValueError(f"Value '{value}' does not match the RGB hex color pattern")


class ColorAlreadyExistsException(Exception):
    """Exception to be raised when a color already exists on database"""


class ColorDoesNotExistException(Exception):
    """Exception to be raised when a color does not exist on database"""
