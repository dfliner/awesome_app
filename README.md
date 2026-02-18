## create a poetry project:

if poetry not installed:
```sh
curl -sSL https://install.python-poetry.org | python3 -
# check poetry version
poetry --version
```

create a new project `awesomeapp`:
```sh
poetry new awesomeapp
```

the above command generates a project structure like:
```txt
awesomeapp/
├── pyproject.toml       # project metadata + dependencies
├── README.md
├── src/awesomeapp       # your package code
│   └── __init__.py
└── tests/
    └── __init__.py
```

**if you just want to start in an existing folder:**

```sh
poetry init   # similar to `git init`, it creates a poetry project in current folder.
```

## virtual environment

By default, poetry creates the virtual environment under `~/.cache/pypoetry/virtualenvs/<project>-<hash>`. To enable the .venv under the project root folder, you need to change poetry config:

```sh
poetry config virtualenvs.in-project true
# confirm the config settings
popetry config --list
# or just confirm the .venv path
poetry env info --path
```

`virtualenvs.in-project` must be set through `poetry config` command. It cannot be set in `pyproject.toml` file because poetry treats them as developer-specific preferences, not project metadata.

> NOTE: poetry treats config in two scopes:
> - global: `poetry config` writes to `~/.config/pypeotry/config.toml`
> - local:  `poetry config --local` writes to `./.poetry/config.toml`

To set `virtualenvs.in-project` to local scope (apply to project only), run

```sh
poetry config virtualenvs.in-project --local
```

This creates a .poetry/config.toml inside your project.

## manage dependencies

To install dependencies into .venv, run

```sh
poetry install
```

### add dependency

poetry requires virtual environment. `poetry add <package>` command will create .venv as needed.

runtime dependency:

```sh
poetry add requests
```

dev/test dependency:

```sh
poetry add --dev pytest
```

### install dependency listed in pyproject.toml

```sh
poetry install
```

### build and pack app into distributable artifacts.

```sh
poetry build
```

This creates artifacts under `dist/` folder.

```txt
awesomeapp-0.1.0-py3-none-any.whl    # wheel (binary package)
awesomeapp-0.1.0.tar.gz              # source distribution
```

install the app:

```sh
pip install dist/awesomeapp-0.1.0-py3-none-any.whl
```

upload the add to PyPI:

```sh
pip publish awesomeapp
```






## ChatGPT generated

Example: Using `pipx` + `Poetry` + `pyproject.toml` + `poetry.toml`

1. Install Poetry the Recommended Way

The official Poetry docs now recommend using `pipx` for installation:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install poetry
```

Verify:

```sh
poetry --version
```

This installs `Poetry` in an isolated venv under: `~/.local/pipx/venvs/poetry`and exposes the poetry CLI globally.

2. Create a New Project

```sh
poetry new myproject
cd myproject
```

This generates the structure:

```txt
myproject/
├── pyproject.toml    # Project metadata & dependencies
├── README.md
├── myproject/        # Package source code
│   └── __init__.py
└── tests/            # Test folder
    └── __init__.py
```

3. Configure `Poetry` to Use `.venv` Inside Project

By default, Poetry creates venvs in a central cache folder (e.g., `~/.cache/pypoetry/virtualenvs/...`). To make Poetry put the venv inside the project root:

```sh
poetry config virtualenvs.in-project true --local
```

This creates `poetry.toml` in your project root:

```toml
# myproject/poetry.toml

[virtualenvs]
in-project = true
```

Now, when you install dependencies, Poetry creates:

```txt
myproject/.venv/
```

This `.venv/` is Poetry-managed and should not be committed to Git.

4. Install Dependencies

Example:

```sh
poetry add requests numpy
```

This updates `pyproject.toml`:

```toml
# myproject/pyproject.toml

[tool.poetry]
name = "myproject"
version = "0.1.0"
description = ""
authors = ["Daofa Li <daofa@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.32.3"
numpy = "^1.27.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Poetry also generates or updates `poetry.lock` to lock versions.

5. Run Your Code

There are two ways:

(a) Using Poetry’s Shell

```sh
poetry shell
```

This activates the .venv automatically:

```sh
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate     # Windows
```
(b) Running Commands Directly

```sh
poetry run python myproject/main.py
```

Or run pytest:

```sh
poetry run pytest
```

6. Check the Active Virtual Environment

```sh
poetry env info --path
```

Example output:

```txt
/home/user/dev/myproject/.venv
```

If you hadn’t enabled in-project venvs, it would show something like:

```txt
/home/user/.cache/pypoetry/virtualenvs/myproject-abc123
```

7. Updated Project Tree (Latest Best Practices)

```txt
myproject/
├── .venv/                # Poetry-managed venv (not tracked by Git)
├── myproject/            # Your source code
│   └── __init__.py
├── tests/                # Your tests
│   └── __init__.py
├── poetry.toml           # Local Poetry config (in-project venv, etc.)
├── pyproject.toml        # Project metadata, dependencies, build settings
├── poetry.lock           # Locked dependencies for reproducible builds
├── README.md
└── .gitignore            # Make sure `.venv/` is ignored
```

Example `.gitignore`:

```txt
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
```

8. How Config Files Work (Latest Poetry ≥1.8)

File	        Purpose	                        Should Commit?	Example Setting
pyproject.toml	Project metadata & dependencies	✅ Yes	      requests = "^2.32.3"
poetry.lock	    Locked dependency versions	    ✅ Yes	      Exact pinned versions
poetry.toml	Local Poetry config (new in 1.2+)	❌ Usually no  virtualenvs.in-project=true
.venv/	        Local virtual environment	    ❌ No	Installed dependencies
pipx env	Global isolated Poetry installation	N/A	Managed by pipx

9. Best Practices for 2025

Use pipx to install Poetry → clean global environment.

Use .venv inside the project → better IDE integration & portability.

Commit pyproject.toml & poetry.lock → ensures consistent builds.

Do NOT commit .venv/ or poetry.toml → keep them local.

For teams, document in README.md:

poetry config virtualenvs.in-project true --local

Final Workflow
# 1. Install Poetry via pipx
pipx install poetry

# 2. Create a new project
poetry new myproject && cd myproject

# 3. Enable in-project venv
poetry config virtualenvs.in-project true --local

# 4. Add dependencies
poetry add requests numpy

# 5. Run app
poetry run python myproject/main.py

# 6. Activate shell if needed
poetry shell
