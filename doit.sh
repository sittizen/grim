export MYPYPATH=/workspace/components

poetry run isort --overwrite-in-place --line-width=120 --multi-line=3 --trailing-comma --float-to-top components
poetry run isort --overwrite-in-place --line-width=120 --multi-line=3 --trailing-comma --float-to-top development
poetry run isort --overwrite-in-place --line-width=120 --multi-line=3 --trailing-comma --float-to-top test

poetry run black --line-length=120 components
poetry run black --line-length=120 development
poetry run black --line-length=120 test

poetry run flake8 --extend-exclude=.cache,.mypy_cache,.pytest_cache,.venv --max-line-length=120 components
poetry run flake8 --extend-exclude=.cache,.mypy_cache,.pytest_cache,.venv --max-line-length=120 development
poetry run flake8 --extend-exclude=.cache,.mypy_cache,.pytest_cache,.venv --max-line-length=120 test

poetry run mypy --pretty --strict --explicit-package-bases components
poetry run mypy --pretty --strict --explicit-package-bases development
poetry run mypy --pretty --strict --explicit-package-bases test

poetry run pytest