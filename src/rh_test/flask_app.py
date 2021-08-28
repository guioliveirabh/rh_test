"""Configure flask and flask_restful. Define the API and routes"""

from flask import Flask
from flask_restful import Api, Resource, abort, fields, marshal_with, reqparse

from rh_test.models.color import ColorAlreadyExistsException, ColorDoesNotExistException, ColorManager
from rh_test.util import html_codes

app = Flask(__name__)
api = Api(app)
post_parser = reqparse.RequestParser()
post_parser.add_argument('color', required=True)
post_parser.add_argument('value', required=True, type=ColorManager.convert_hex_color)
resource_fields = {
    'color': fields.String,
    'value': fields.String
}


def abort_with_message(error_code, message):
    """Aborts the execution sending a message to the user"""
    abort(error_code, message=message)


class ColorListResource(Resource):
    """Handles the color list retrieval and adding a new color to the list"""
    color_manager = ColorManager()

    @marshal_with(resource_fields)
    def get(self):
        """Color list retrieval"""
        return self.color_manager.get_all_colors()

    def post(self):  # pylint: disable=R1710
        """Add a new color to the list"""
        args = post_parser.parse_args()
        try:
            inserted = self.color_manager.insert_color(color=args['color'], value=args['value'])
            return inserted, html_codes.CREATED
        except ColorAlreadyExistsException as exception:
            abort_with_message(html_codes.CONFLICT, str(exception))


class ColorResource(Resource):
    """Handles the single color retrieval"""
    color_manager = ColorManager()

    @marshal_with(resource_fields)
    def get(self, value):  # pylint: disable=R1710
        """Single color retrieval"""
        try:
            value = ColorManager.convert_hex_color(value)
            return self.color_manager.get_color_by_value(value)
        except (ValueError, ColorDoesNotExistException) as exception:
            abort_with_message(html_codes.NOT_FOUND, str(exception))


# set routes
api.add_resource(ColorListResource, '/colors')
api.add_resource(ColorResource, '/colors/<value>')
