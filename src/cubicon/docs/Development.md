# Development workflow with Docker (In progress)


## Prerequisites

You will need:

- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`
- Install `docker` and `docker-compose`
- Install [pre-commit](https://pre-commit.com/#install) and  run command `pre-commit install` inside project root
- Run a command to configure custom hooks in the project root: `./config/add_git_hooks.sh`


### Code editors
- [`editorconfig`](http://editorconfig.org/) plugin (**required**)


### Development with docker
Put `.env` file to `config` directory (See `config/env.template` example) and `config_ini.test`

To start development server inside docker you will need to run:

```sh
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml run --rm platform python manage.py migrate --noinput
docker-compose -f docker-compose.dev.yml up
```

Running tests:
```sh
docker-compose -f docker-compose.dev.yml run --rm platform pytest tests
```

### Code quality
[wemake-python-styleguide](https://wemake-python-styleguide.readthedocs.io/en/latest/)

Run tests and linters:

```sh
pre-commit run qa
```

