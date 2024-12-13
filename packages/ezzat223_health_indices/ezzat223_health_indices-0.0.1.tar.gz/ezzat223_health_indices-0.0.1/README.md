# No more Dependency hell!
- Creates virtual environments.
- Manages dependencies.
- Publish packages to PyPI.

- You define everything in the pyproject.toml file.

## Commands
----------------
- To create a new project using it: >`poetry new <project-name>`
- Create a new project with the src directory: >`poetry new <project-name> --src`
- To init the pyproject.toml only: >`poetry init`
- Check everything is correct: >`poetry check`

***Packages***
- Add new package from cli (This will add it to current pyproject.toml file) and installs it in the venv:
>`poetry add <package-name>`
- Specify the version of the package: >`poetry add <package-name>@<version>`
- Add a package for dev only: >`poetry add <package-name> --group=dev`
- If you changed any package's version from the file not cli (update lock): >`poetry update`

- Show all packages: >`poetry show`
- Show a specific package: >`poetry show <package-name>`
- Remove a package: >`poetry remove <package-name>`

- Now to create a venv and install all specified packages: >`poetry install`
- Install without dev dependencies: >`poetry install --without dev`
- Install ONLY dev dependencies: >`poetry install --with dev`

------------
***VENV***
- To make your venv be in current working directory: >`poetry config virtualenvs.in-project true`
- Open a shell or activate the venv: >`poetry shell`
- Exit the shell: >`exit`
- Deactivate the virtualenv: >`deactivate`
- Get env info: >`poetry env info`
- List envs: >`poetry env list`
- Remove a venv: >`poetry env remove <venv-name>`
- Select a specific python version (You must have that version's exe): >`poetry env use <version>`

- If you're not in the venv and wanna execute a command using it: >`poetry run <command`

-----------------
***Versioning***
- Pump major version: >`poetry version major`
- Pump minor version: >`poetry version minor`
- Pump patch version: >`poetry version patch`

---------------------------
***Publish the package***
- First configure it: >`poetry config repositories.test-pypi https://test.pypi.org/legacy`
- Get a token and add it to the configurations: >`poetry config pypi-token.<token-name> <token>`
- Build: >`poetry build`
- Publish: >`poetry publish -r <token-name>`

---------------
***export***
- Export packages to a requirements.txt file: >`poetry export -f requirements.txt --output requirements.txt`
- Include dev or any group packages too:
>`poetry export -f requirements.txt --output requirements.txt --with <group-name>`
- By default, Poetry exports dependencies with hashes for security. If you want to exclude hashes:
>`poetry export -f requirements.txt --without-hashes --output requirements.txt`