import unittest

from rh_test.models.color import ColorDoesNotExistException, ColorManager


class TestHexColor(unittest.TestCase):
    def test_expected(self):
        for hex_value in ['#000', '#000FFF', '#FFF']:
            ColorManager.convert_hex_color(hex_value)

    def test_not_expected(self):
        for hex_value in ['#XXX', '000FFF', '#/*-FFF']:
            with self.assertRaises(ValueError):
                ColorManager.convert_hex_color(hex_value)


class TestColorModel(unittest.TestCase):
    def setUp(self) -> None:
        self.black_color = {
            "color": "black",
            "value": "#000"
        }
        self.color_manager = ColorManager()

    def test_clean(self):
        self.color_manager.delete_all()
        self.assertEqual(len(self.color_manager.get_all_colors()), 0)

    def test_insert_and_get_by_value(self):
        self.color_manager.delete_all()
        self.color_manager.insert_color(**self.black_color)
        self.assertEqual(len(self.color_manager.get_all_colors()), 1)
        self.assertEqual(self.color_manager.get_color_by_value(self.black_color['value']), self.black_color)

    def test_insert_and_get_by_name(self):
        self.color_manager.delete_all()
        self.color_manager.insert_color(**self.black_color)
        self.assertEqual(len(self.color_manager.get_all_colors()), 1)
        self.assertEqual(self.color_manager.get_color_by_name(self.black_color['color']), self.black_color)

    def test_get_non_existent(self):
        self.color_manager.delete_all()
        with self.assertRaises(ColorDoesNotExistException):
            self.color_manager.get_color_by_value(self.black_color['value'])

        with self.assertRaises(ColorDoesNotExistException):
            self.color_manager.get_color_by_name(self.black_color['color'])


if __name__ == '__main__':
    unittest.main()
