# Flask SQLAlchemy Compat

{:toc}

## CHANGELOG

### 0.2.0 @ 12/13/2024

#### :mega: New

1. Make `backends.fsa` and `backends.fsa_lite` protected by `backends.proxy`. The other parts of this project will access backends module by this newly added `proxy`. This change allows users to deliberately change `proxy` for testing purposes. For example, the users can disable `flask-sqlalchemy` by setting `proxy.fsa = None` even if the package is already installed.
2. Provide two new methods `get_flask_sqlalchemy_proxy_ver(...)` and `get_flask_sqlalchemy_lite_proxy_ver(...)`. In run time, they are totally the same as `get_flask_sqlalchemy(...)` and `get_flask_sqlalchemy_lite(...)`, respectively. The only difference is that the returned values of `_proxy_ver(...)` are notated by the the proxy classes like `SQLAlchemyProxy`. Users can use these methods to check the compatibility with the falling back version via the static type checker.
3. Add three examples (demos): `examples.app_fsqla`, `examples.app_fsqla_lite`, `usage`.
4. Add unit tests and the corresponding configurations.
5. Add the GitHub workflow for running the unit tests.

#### :wrench: Fix

1. Fix: When the module is reloaded, accessing the `SQLAlchemyProxy().Model.query` may cause `RuntimeError`. Now, this error has been catched.
2. Fix: Prevent `flake8` from raising `F722` when working with older python versions (`Python<3.10`).

#### :floppy_disk: Change

1. Update the metadata of the package. The chages are made for adjusting the new optional dependencies and tests.
2. Update the project information for preparing to upload a new PyPI release.

### 0.1.3 @ 12/11/2024

#### :wrench: Fix

1. Fix: Previously, running `db.init_app(...)` outside the app context will fail if `db` is provided by the proxy class. Now, the `init_app` can be used without limitations.

#### :floppy_disk: Change

1. Adjust the readme file to make the examples consistent with the `db.init_app` behavior in the new version.

### 0.1.2 @ 12/10/2024

#### :wrench: Fix

1. Fix: Adjust the dependency versions to make the requirements satisfy the usage in `Python=3.13`.

### 0.1.1 @ 12/10/2024

#### :wrench: Fix

1. Fix: Stabilize the backend import when using `Python=3.7`, where the compatible backend will provide an version that would not be overridden by other installations.
2. Fix: Correct the package information. The package should be zip-safe and does not include extra data.
3. Fix: Correct some out-of-date information in the readme file.
4. Fix: Make some type hint excluded from the run time to improve the stability.
5. Fix: Adjust the dependency versions to match the requirements specified in `flask-sqlalchemy-lite`.

#### :floppy_disk: Change

1. Add more files to the exclude list of `black`.

### 0.1.0 @ 12/09/2024

#### :mega: New

1. Create this project.
2. Finish the first version of the pacakge `flask-sqlalchemy-compat`.
3. Add configurations `pyproject.toml`.
4. Add the devloper's environment folder `./docker` and the `Dockerfile`.
5. Add the community guideline files: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SECURITY.md`.
6. Add the issue and pull request templates.
7. Configure the github workflows for publishing the package.
8. Add the banner and adjust the format in the readme.

#### :wrench: Fix

1. Fix: Adjust the formats of the `requirements` to make them compatible with `pyproject.toml`.
2. Fix: A Git-sourced dependency is not approved by PyPI. Therefore, replace the Git source by a customized related package: [`Flask-SQLAlchemy-compat-backend-py37`](https://pypi.org/project/Flask-SQLAlchemy-compat-backend-py37).

#### :floppy_disk: Change

1. Adjust the metadata according to the current project status.
