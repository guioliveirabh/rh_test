.PHONY: build run regression test

build:
	podman build -t rh_test --ignorefile .containerignore .

run: build
	podman run --rm -p 5000:5000 rh_test

test: build
	podman run --rm -i --entrypoint make rh_test regression

# run inside container
regression:
	coverage erase
	coverage run --source rh_test -m unittest discover tests
	coverage report -m
	pylint -E rh_test
