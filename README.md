# SSL Analyzer

![CI Workflow](https://github.com/antibagr/python-ssl-analyzer/actions/workflows/makefile.yml/badge.svg?event=push)![coverage badge](./coverage.svg)


## Description

This is a SSL Analyzer that can be used to check the SSL certificate of a given domain. It checks for supported
protocols, and alt names specified in the certificate.

It uses an awesome [testssl.sh](https://github.com/drwetter/testssl.sh) tool to perform the analysis. The tool is
packaged in a Docker container and is run in parallel using [GNU Parallel](https://www.gnu.org/software/parallel/).

The output is written to a [Clickhouse](https://clickhouse.tech/) database.

## Table of Contents

- [SSL Analyzer](#ssl-analyzer)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
    - [Installation](#installation)
    - [Environment Variables](#environment-variables)
    - [Input File](#input-file)
    - [Run](#run)
  - [Contributing](#contributing)
    - [Poetry](#poetry)
    - [Dependencies](#dependencies)
    - [Development](#development)


## Usage

> **Note for Windows Users:**
>
> If you are using Windows, it's important to ensure that you have Windows Subsystem for Linux (WSL) 2 installed and configured correctly before running the provided commands under a WSL terminal. WSL 2 provides a Linux-compatible environment that can be used for development tasks.
>
> To install and set up WSL 2 on your Windows machine, please follow the official Microsoft documentation: [Install Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install).
>
> Once WSL 2 is set up, make sure to use the WSL terminal for running the commands specified in this documentation for a seamless development experience.
>
> If you encounter any issues related to WSL or need further assistance, please refer to the Microsoft WSL documentation or seek support from the WSL community.


### Installation

1. Install [Docker](https://docs.docker.com/desktop/)
2. Install [Docker Compose](https://docs.docker.com/compose/install/)


### Environment Variables

The following environment variables are required to run the application:

| Variable Name             | Description                                            |
| ------------------------- | ------------------------------------------------------ |
| `CLICKHOUSE_HOST`         | Clickhouse host                                        |
| `CLICKHOUSE_PORT`         | Clickhouse port                                        |
| `CLICKHOUSE_USER`         | Clickhouse user                                        |
| `CLICKHOUSE_PASSWORD`     | Clickhouse password                                    |
| `CLICKHOUSE_DB`           | Clickhouse database                                    |
| `CLICKHOUSE_TABLE`        | Clickhouse table                                       |
| `TEST_SSL_CONTAINER_NAME` | testssl container name                                 |
| `TEST_SSL_WORKDIR`        | **Warning**: Edit along with deploy/testssl/Dockerfile |
| `TEST_SSL_OUTPUT_DIR`    | **Warning**: Edit along with deploy/testssl/Dockerfile |
| `TEST_SSL_COMMANDS_FILE`  | **Warning**: Edit along with deploy/testssl/Dockerfile |


### Input File

Provide the input file as a command line argument. The input file should contain a list of `host:port`, one per
line. The output will be written to Clickhouse database.

Create a file named `input.txt` in the `data` directory and add the following content to it:

```bash
touch ./data/input.txt
echo "google.com:443" >> data/input.txt
echo "facebook.com:443" >> data/input.txt
```


### Run

Now you can run the following command to start the application:

```bash
make compose-up
```


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Poetry

Install poetry using your package manager or [official guide](https://python-poetry.org/docs/#installation).

### Dependencies

The easiest way to install required and dev dependencies is as follows:

```bash
make install
```

### Development

This will install all the dependencies and create a virtual environment for you.

Now you can format the code using:

```bash
make format
```

To run linters:

```bash
make lint
```

To run tests:

```bash
make test
```
