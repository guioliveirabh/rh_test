FROM docker.io/library/python:3.9

ENV PYTHONUNBUFFERED 1

# TODO: use ARG to install tests dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install --no-install-recommends -y make && apt clean && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# TODO: install dependencies first and copy code later
COPY . .

# TODO: use ARG to install tests dependencies
RUN pip install .[test]

EXPOSE 5000/tcp
ENTRYPOINT rh_test
