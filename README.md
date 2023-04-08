# FastAPI Template
A simple and ready to go FastAPI template using:

* [Python 3.10](https://www.python.org/downloads/release/python-3100/)
* [FastAPI](https://fastapi.tiangolo.com/) 
* [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
* [PostgreSQL](https://www.postgresql.org/)
* [Poetry](https://python-poetry.org/)
* [Docker](https://www.docker.com/)

This template is free to use and aimed to be used as a base for your projects. It includes a simple User CRUD and a JWT authentication system.
It includes a Dockerfile and a docker-compose.yml file to run the project using Docker. Also, some basic GitHub Actions are included to run the tests and linters.

## Usage

To use this template you must have [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/) installed. If you don't have it, you can install it using the following command:

```bash
pip install cookiecutter
```

Then you can use the following command to create a new project:

```bash
cookiecutter https://github.com/LeoMo-27/FastAPI-template
```

You will be asked to enter some information about your project, such as the name, description, the author name and email.
Once you have entered all the information, a new folder will be created with the name of your project. Inside this folder you will find
a README.md file with the instructions to run it.
