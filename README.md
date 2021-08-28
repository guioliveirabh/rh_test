# Assignment for RH

## Spec

[infra_ma_assessment.pdf](docs/infra_ma_assessment.pdf)

1. Write a Flask application implementing a REST API to serve the content of
   the [colors.json](src/rh_test/resources/colors.json) file. Feel free to add any framework/library which you think is
   necessary for this purpose. The user should be able to perform the following operations:
    * Retrieve the whole list of colors
    * Retrieve a single color from the list
    * Insert a new color into the list
1. Write automated tests for the API. You can use any tool/framework which you think is necessary to do that.
1. Prepare your application to be deployed and executed in a containerized environment, using `podman`. Provide the
   needed files for the deployment.
1. Provide documentation for deployment and utilization of the API. You may use any kind of format for the
   documentation.

## How to use / Deployment

Prerequisites:

* `podman` and `make` commands available on PATH;
* internet connection.

### Run tests

Command: `$ make test`

It will build the image using `podman`, create a container and run the tests on it. The test suite consists of:

* Few unit tests for the model and API;
    * A coverage report is provided after the execution.
* Linting errors on code using `pylint`.

### Run server

Command: `$ make run`

It will build the image using `podman`, create a container and run the webserver on `http://localhost:5000/`.

## API documentation

* All responses from API are in JSON format;
    * The colors are represented by a dictionary having the color name and its value in RGB hex with three or six
      digits. For instance:
    ```json
    {
      "color": "black",
      "value": "#000"
    }
    ```
* All data sent (post) to API need to be in JSON format.

### Available endpoints

`http://localhost:5000/api/v1/` is the base URL for all endpoints:

| HTTP method | endpoint | JSON args | description |
| ----------- | -------- | --------- | ----------- |
| GET | /colors | - | returns a list with all the colors in database. |
| POST | /colors | color, value | inserts the color on database, if not present, returning it. Otherwise the response code will be set to `409`. |
| GET | /colors/\<RGB hex> | - | returns the color, if present on database. Otherwise the response code will be set to `404`. |
| GET | /colors/\<color name> | - | returns the color, if present on database. Otherwise the response code will be set to `404`. |
