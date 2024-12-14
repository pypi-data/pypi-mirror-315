# -*- coding: UTF-8 -*-
"""
Utilities
=========
@ Flask SQLAlchemy Compat - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Extra utilities used in the tests.
"""

import os
import sys
import importlib
import contextlib

from typing import Any

try:
    from typing import Generator
    from typing import Tuple
except ImportError:
    from collections.abc import Generator
    from builtins import tuple as Tuple

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from flask import Flask


__all__ = (
    "import_app",
    "import_model_types",
    "db_engine",
    "create_test_db",
    "dispose_test_db",
)


def import_app(app_name: str, models_name: str) -> Tuple[Flask, Any]:
    """Import a testing application.

    An application imported by this function needs to contain two module files.
    1. The module defining the application.
    2. The module defining the database object relationship mapping (ORM) models of
       the application.

    When this function is called, it will check whether the application has been
    imported before. If so, reload the existing two module files. If not, import
    the modules directly.

    Arguments
    ---------
    app_name: `str`
        The full name of the application module. Its format should be like
        `examples.app_...` (like how the module is imported by `import`).

    models_name: `str`
        The full name of the ORM model module.

    Returns
    -------
    #1: `Flask`
        The imported Flask application.

    #2: `SQLAlchemy`
        The database extension bound to the app #1.
    """
    if models_name not in sys.modules:
        importlib.import_module(models_name)
    else:
        importlib.reload(sys.modules[models_name])
    if app_name not in sys.modules:
        module = importlib.import_module(app_name)
    else:
        module = sys.modules[app_name]
        module = importlib.reload(module)
    return module.app, module.db


def import_model_types(models_name: str) -> Tuple[Any, Any, Any, Any]:
    """Import model types for testing purpose.

    The model types are the subclasses of the `Base` class in a database object
    relationship mapping (ORM) module.

    When this function is called, it will check whether the application has been
    imported before. If so, acquire the models directly. If not, import
    the modules and get the models. Note that this method will not let the model
    reloaded.

    Arguments
    ---------
    models_name: `str`
        The full name of the ORM model module.

    Returns
    -------
    #1: `type[Base]`
        The base class of all models.

    #2: `type[Role]`
        The model type `Role`.

    #3: `type[User]`
        The model type `User`.

    #4: `type[Entry]`
        The model type `Entry`.
    """
    if models_name not in sys.modules:
        module = importlib.import_module(models_name)
    else:
        module = sys.modules[models_name]
    return module.Base, module.Role, module.User, module.Entry


@contextlib.contextmanager
def db_engine(url: str) -> Generator[sa.Engine, None, None]:
    """Acquire a new SQLAlchemy Engine as a context. When the context is closed,
    dispose the engine."""
    engine = sa.create_engine(url)
    try:
        yield engine
    finally:
        engine.dispose()


def create_test_db(db_name: str) -> None:
    """Create a testing database.

    Arguments
    ---------
    db_name: `str`
        The database name formatted like `xxxx.db`. The SQLite3 DB file will be
        stored in the `instance` folder of the source code folder.
    """
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)
    with contextlib.ExitStack() as stk:
        engine = stk.enter_context(
            db_engine("sqlite:///{0}".format(os.path.join(folder, db_name)))
        )

        Session = sa_orm.sessionmaker(bind=engine)
        models_name = "examples.models_fsqla_lite"
        if models_name not in sys.modules:
            module = importlib.import_module(models_name)
        else:
            module = importlib.reload(sys.modules[models_name])

        sess = stk.enter_context(Session())

        Base = module.Base
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        Role = module.Role
        role_admin = Role(name="admin", level=0)
        role_reader = Role(name="reader", level=100)

        sess.add(role_admin)
        sess.add(role_reader)
        sess.commit()

        User = module.User
        Entry = module.Entry
        user = User(name="admin01")
        user.set_password("imadmin")
        user.roles.append(role_admin)
        user.roles.append(role_reader)
        Entry(data="admin's data 1", user_id=user.id, user=user)
        Entry(data="admin's data 2", user_id=user.id, user=user)
        sess.add(user)

        user = User(name="reader01")
        user.set_password("regular")
        user.roles.append(role_reader)
        Entry(data="reader's data 1", user_id=user.id, user=user)
        Entry(data="reader's data 2", user_id=user.id, user=user)
        sess.add(user)

        user = User(name="admin02")
        user.set_password("imanotheradmin")
        user.roles.append(role_admin)
        Entry(data="admin's data 3", user_id=user.id, user=user)
        Entry(data="admin's data 4", user_id=user.id, user=user)
        sess.add(user)

        user = User(name="reader02")
        user.set_password("regular2")
        user.roles.append(role_reader)
        Entry(data="reader's data 3", user_id=user.id, user=user)
        sess.add(user)
        sess.commit()


def dispose_test_db(db_name: str) -> None:
    """Dispose a testing database.

    This method will completely remove the database after dropping all tables.

    Arguments
    ---------
    db_name: `str`
        The database name formatted like `xxxx.db`. The SQLite3 DB file will be
        stored in the `instance` folder of the source code folder.
    """
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    folder = os.path.abspath(folder)
    os.makedirs(folder, exist_ok=True)
    db_path = os.path.join(folder, db_name)
    if not os.path.isfile(db_path):
        return
    with contextlib.ExitStack() as stk:
        engine = stk.enter_context(db_engine("sqlite:///{0}".format(db_path)))

        models_name = "examples.models_fsqla_lite"
        if models_name not in sys.modules:
            module = importlib.import_module(models_name)
        else:
            module = importlib.reload(sys.modules[models_name])

        Base = module.Base
        Base.metadata.drop_all(engine)

    if os.path.isfile(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass
