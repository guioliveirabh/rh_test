image_name = rh_test

.PHONY: build run regression test

build:
	podman build -t $(image_name) --ignorefile .containerignore .

run: build
	podman run --rm -p 5000:5000 $(image_name)

test: build
	podman run --rm -i --entrypoint make $(image_name) regression

# run inside container
regression:
	coverage erase
	coverage run --source rh_test -m unittest discover tests
	coverage report -m
	pylint -E rh_test
