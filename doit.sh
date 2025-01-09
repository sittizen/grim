export MYPYPATH=/workspace/components

poetry run ruff check --fix components
poetry run ruff format components
poetry run ruff check --fix development
poetry run ruff format development
poetry run ruff check --fix test
poetry run ruff format test

poetry run mypy --pretty --strict --explicit-package-bases components
poetry run mypy --pretty --strict --explicit-package-bases development
poetry run mypy --pretty --strict --explicit-package-bases test

poetry install

poetry run pytest