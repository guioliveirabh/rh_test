"""Contains the package entrypoint"""
from rh_test.flask_app import create_app


def main():
    """Run flask server"""
    # TODO: use env vars
    # TODO: deploy with a proper server
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
