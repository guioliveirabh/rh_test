from rh_test.flask_app import app


def main():
    # TODO: use env vars
    app.run(host='0.0.0.0', port=5000, debug=True)
