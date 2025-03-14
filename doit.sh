export MYPYPATH=/workspace/components

poetry run ruff check --fix components/
#poetry run ruff check --select I --fix components/
poetry run ruff format components/
poetry run ruff check --fix development/
#poetry run ruff check --select I --fix development/
poetry run ruff format development/
poetry run ruff check --fix test/
#poetry run ruff check --select I --fix test/
poetry run ruff format test/

poetry run mypy --pretty --strict .

poetry install

poetry run pytest