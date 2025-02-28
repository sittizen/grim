# GRIM

## Polylith
The official Polylith documentation:
[high-level documentation](https://polylith.gitbook.io/polylith)

A Python implementation of the Polylith tool:
[python-polylith](https://github.com/DavidVujic/python-polylith)

[commands reference](https://davidvujic.github.io/python-polylith-docs/commands/)

### to build a project

From the folder of the project (inside the toolchain container)

```
poetry build-project
```

outside the container

```
docker build -t (basename "$PWD") .
```


## Textual

### debug console
```
poetry run textual console -x SYSTEM -x EVENT -x DEBUG -x INFO
```

### dev mode
```
poetry run textual run --dev development/app.py
```