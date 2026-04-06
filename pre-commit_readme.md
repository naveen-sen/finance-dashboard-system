# Pre-commit Hook Setup for Python Projects

## Introduction
This repository uses `pre-commit` to enforce code quality and formatting before commits. The pre-commit hooks ensure that code follows best practices and maintains consistency.

## Configuration
The hooks are defined in `.pre-commit-config.yaml`. Below is an example configuration:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.1.0
    hooks:
      - id: black
        args: ["--line-length", "100", "--skip-string-normalization"]

  - repo: https://github.com/pycqa/isort
    rev: 6.0.1
    hooks:
      - id: isort
```


## Usage

### Manually Running Pre-commit Hooks
To check all files manually stages file:
```bash
pre-commit run --hook-stage manual
```
To check all files manually stages file:
```bash
pre-commit run --hook-stage manual --all-files
```
To check specific files:
```bash
pre-commit run --hook-stage manual --files <filename>
```

To check specific folder:
```bash
pre-commit run --hook-stage manual --files $(find app/models/ -name "*.py")
```

**Note:** If you install dependencies using:  
```bash
poetry install --no-dev
```  
and later need to install all dependencies (including development dependencies), run:  
```bash
poetry install
```  
```bash
pip show pre-commit
```

pre-commit install
```
```bash
git add <your_file(s)>
```
Attempt a Commit:
```
git commit -m "Test commit"
```