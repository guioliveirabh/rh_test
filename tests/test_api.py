import unittest

from rh_test.flask_app import URL_PREFIX, create_app
from rh_test.models.color import ColorManager
from rh_test.util import html_codes


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.black_color = {
            "color": "black",
            "value": "#000"
        }
        self.color_manager = ColorManager()

    def test_empty_colors(self):
        self.color_manager.delete_all()
        with self.app.test_client() as client:
            response = client.get(URL_PREFIX + '/colors')
            self.assertEqual(len(response.get_json()), 0)

    def test_insert_and_get(self):
        self.color_manager.delete_all()
        with self.app.test_client() as client:
            response = client.post(URL_PREFIX + '/colors', json=self.black_color)
            self.assertEqual(response.get_json(), self.black_color)
            self.assertEqual(response.status_code, html_codes.CREATED)
            response = client.get(URL_PREFIX + '/colors/%23000')
            self.assertEqual(response.get_json(), self.black_color)
            self.assertEqual(response.status_code, html_codes.OK)
            response = client.get(URL_PREFIX + '/colors/black')
            self.assertEqual(response.get_json(), self.black_color)
            self.assertEqual(response.status_code, html_codes.OK)

    def test_conflict(self):
        self.color_manager.delete_all()
        self.color_manager.load_from_json()
        with self.app.test_client() as client:
            response = client.post(URL_PREFIX + '/colors', json=self.black_color)
            self.assertEqual(response.status_code, html_codes.CONFLICT)

    def test_get_non_existent(self):
        self.color_manager.delete_all()
        with self.app.test_client() as client:
            response = client.get(URL_PREFIX + '/colors/%23000')
            self.assertEqual(response.status_code, html_codes.NOT_FOUND)

    def test_insert_with_wrong_content(self):
        self.color_manager.delete_all()
        self.color_manager.load_from_json()
        with self.app.test_client() as client:
            response = client.post(URL_PREFIX + '/colors', json={})
            self.assertEqual(response.status_code, html_codes.BAD_REQUEST)

            response = client.post(URL_PREFIX + '/colors', json={
                "color": "black",
                "value": "000"
            })
            self.assertEqual(response.status_code, html_codes.BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
