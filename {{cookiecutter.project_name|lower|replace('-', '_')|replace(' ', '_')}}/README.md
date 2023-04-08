# {{ cookiecutter.project_name }}
{{ cookiecutter.project_description }}

## Features

This project comes with a set of features that are used to make the development easier. Here is a list of the most important ones:

* [Python 3.10](https://www.python.org/downloads/release/python-3100/) - The version used to develop this project.
* [Poetry](https://python-poetry.org/) - The dependency manager used to manage the dependencies.
* [Docker](https://www.docker.com/) - The containerization tool used to run the project. It can be used to run the project and the database in a container.
* [PyJWT](https://pyjwt.readthedocs.io/en/stable/) - The library used to manage the JWT tokens.
* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used to develop the API. It is based on [Starlette](https://www.starlette.io/) and it provides support for asynchronous code.
* [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) - The ORM used to interact with the database. The 2.0 is the latest version of SQLAlchemy and it provides asynchronous support.
* [Alembic](https://alembic.sqlalchemy.org/en/latest/) - The migration tool used to manage the database migrations. It is integrated with SQLAlchemy, so it will try to detect the changes in the models and generate the migrations automatically.
* [PyTest](https://docs.pytest.org/en/7.2.x/) - The testing framework used to run the tests. It uses a plugin called [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) which provides support for coroutines as test functions. This allows users to await code inside their tests.
* [Black](https://black.readthedocs.io/en/stable/) - The code formatter used to manage the code style.
* [Isort](https://pycqa.github.io/isort/) - The import sorter used to manage the imports.
* [GitHub Actions](https://docs.github.com/en/actions) - The CI/CD tool used to run the tests and linters. It is "free" to use and it is integrated with GitHub.

This project also includes a simple User CRUD and a JWT authentication system.

## Setup

You must have [Python 3.10](https://www.python.org/downloads/release/python-3100/) and [Poetry](https://python-poetry.org/) installed. Install the dependencies with:

```bash
poetry install
```

And poetry will create a new virtual environment and will install the dependencies for the project. 

## Manual setup

You can choose to run this project manually, without using Docker. As the project need a PostgreSQL database, you must have one running, the recommended way to do this is using [Docker](https://www.docker.com/). You can use the following command to run a PostgreSQL container:

```bash
make docker-compose-db
```

Then you will have to run the migrations to create the tables in the database. To do this, you can use the following command:

```bash
alembic upgrade head
```

And finally, you can run the project using the following command:

```bash
uvicorn src.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.


## Docker setup

For an easier setup, you can use Docker to run the project. To do this, you must have [Docker](https://www.docker.com/) installed. First you will need to create a new `.env` file inside the `docker` folder, using the `.env.example` file as a template. Then build the image with:

```bash
make docker-compose-build
```

Then you will have to run the migrations to create the tables in the database:

```bash
make docker-compose-migrate
```

And finally, you can run the project using:

```bash
make docker-compose-d # Detached mode
# or
make docker-compose
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the API documentation.

## Linters

This project uses [Black](https://black.readthedocs.io/en/stable/) and [Isort](https://pycqa.github.io/isort/) to manage the code style. To run them use:

```bash
make black! # To run black and fix the errors
make isort! # To run isort and fix the errors
```

## Tests

This project uses [PyTest](https://docs.pytest.org/en/7.2.x/) to run the tests. You can use the following run them:

```bash
make docker-compose-test
```

The tests will run inside a Docker container, so you don't need to have a PostgreSQL database running. The tests will create a new database just for the tests, 
which will be destroyed after they are finished.
