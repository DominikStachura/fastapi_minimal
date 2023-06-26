# fastapi_minimal

Minimal FastAPI project configuration

## Build

You can build application using

```shell
docker-compose up
```

To provide all required environment variables you can create _.env_ file out of example _local.env_ file in this
repository. Docker-compose will automatically take all envs from the file and use it inside your containers.  
If you want to build Production Ready API Container you can use the following command:  
_docker build -f api/Dockerfile --target base --tag api ._  
By setting _target_ to _base_ you can make sure that all development requirements, such as MyPy, Flake etc. will not be
installed inside container.

## Migrations

To set up the database you need to run alembic migrations:  
_alembic upgrade head_  
Or directly inside the container, if you work using docker-compose environment:

```shell
docker-compose exec -T api alembic upgrade head
```

Migrations will be also automatically created when running tests, so you can run _pytest_ and after all tests succeeded,
database will be ready.  
After changing something in the Database Models, you need to generate new migrations, running:  
_alembic revision --autogenerate -m "migration message"_

## Tests and static analysis

Backend app is configured to work with Flake8 and MyPy for checking the typing and styling of the code.  
Running Pytest will generate coverage report in _api/reports_.  
Before committing, make sure to test your changes with Flake, Mypy and Pytest. It can be done by running the following
Shell script:

```shell
#!/bin/sh
docker-compose up -d
docker-compose exec -T api flake8 --config=.flake8 -v
docker-compose exec -T api mypy app
docker-compose exec -T api pytest tests
docker-compose stop
```

