# -*- coding: UTF-8 -*-
"""
Database
========
@ Flask SQLAlchemy Compat - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the purely use the database loaded by the Flask SQLAlchemy extensions.
The applications will not be loaded.
"""

import sys
import itertools
import contextlib
import logging

from typing import TYPE_CHECKING
from typing import Any

try:
    from typing import Generator
    from typing import Tuple, Type
except ImportError:
    from collections.abc import Generator
    from builtins import tuple as Tuple, type as Type

import pytest

from werkzeug.exceptions import NotFound

import sqlalchemy as sa
import flask_sqlalchemy_compat as fsc

from .utils import import_app, import_model_types, create_test_db, dispose_test_db


if TYPE_CHECKING:
    import examples.models_fsqla as m_fsqla
    import examples.models_fsqla_lite as m_fsqla_lite
else:
    m_fsqla = fsc.backends.ModulePlaceholder("examples.models_fsqla")
    m_fsqla_lite = fsc.backends.ModulePlaceholder("examples.models_fsqla_lite")


__all__ = ("init_db_data", "TestFlaskSQLAlchemy", "TestFlaskSQLAlchemyLite")


@pytest.fixture(scope="module", autouse=True)
def init_db_data() -> Generator[None, None, None]:
    """Initialize the data in the database, and dispose the data when quitting from
    the tests in this module."""
    log = logging.getLogger("flask_sqlalchemy_compat.test")
    log.info("Create the testing data.")
    create_test_db("main.db")
    yield None
    log.info("Dispose the testing data.")
    dispose_test_db("main.db")


class TestFlaskSQLAlchemy:
    """Test the functionalities of Flask SQLAlchemy and its proxy class. The coverage
    of the applications in this class scope contains the following cases:
    1. Use Flask SQLAlchemy.
    2. Use Flask SQLAlchemy Lite to mimic the usages of Flask SQLAlchemy.
    """

    ModelTypes = Tuple[
        Type["m_fsqla.Base"],
        Type["m_fsqla.Role"],
        Type["m_fsqla.User"],
        Type["m_fsqla.Entry"],
    ]

    @pytest.fixture(
        scope="class", params=(True,) if sys.version_info < (3, 8) else (True, False)
    )
    def db_models(
        self, request: Any
    ) -> Generator[Tuple[fsc.SQLAlchemyProxy, ModelTypes], None, None]:
        """Database fixture. This fixture will deliver the Flask SQLAlchemy database
        extension from two cases of applications. Each database will be applied to all
        testing methods in this class scope.

        Arguments
        ---------
        request: `_pytest.fixtures.SubRequest`
            The parameter set. Each time it is used, it will deliver the configurations
            of an application.

        Yields
        ------
        #1: `db: SQLAlchemyProxy`
            The SQLAlchemy database session.

        #2: `models: tuple[type[Base], type[Role], type[User], type[Entry]]`
            The models in the context of the current application.
        """
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        name = "fsqla"
        use_module = request.param
        log.info(
            'Initialize the Flask app "{0}" and its SQLAlchemy'
            "extension.".format(name)
        )
        log.debug(
            "Flask SQLAlchemy: {0}".format("Enabled" if use_module else "Disabled")
        )
        fsc.backends.proxy.fsa = use_module
        with contextlib.ExitStack() as stk:
            app, db = import_app(
                "examples.app_{0}".format(name), "examples.models_{0}".format(name)
            )
            stk.enter_context(app.app_context())
            models = import_model_types("examples.models_{0}".format(name))
            yield db, models
        fsc.backends.proxy.fsa = True
        log.info("Remove the Flask app.")
        del app
        del db

    def test_fsa_dbname(
        self, db_models: Tuple[fsc.SQLAlchemyProxy, ModelTypes]
    ) -> None:
        """Test: Display the Flask SQLAlchemy extension currently used by this case."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, _ = db_models
        log.info({"db": str(db), "module": db.__module__})

    def test_fsa_get_by_id(
        self, db_models: Tuple[fsc.SQLAlchemyProxy, ModelTypes]
    ) -> None:
        """Test: Check whether the get-by-ID functionality works or not."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")

        db, (_, Role, User, Entry) = db_models
        role = db.get_or_404(Role, 1)
        assert role.name == "admin"
        assert role.is_admin is (role.level < 10)
        log.info(
            "Role: {0}".format(
                {"id": role.id, "name": role.name, "is_admin": role.is_admin}
            )
        )

        user = db.get_or_404(User, 1)
        assert user.name == "admin01"
        assert user.is_admin is (
            len(user.roles) > 0 and any(role.is_admin for role in user.roles)
        )
        assert user.validate_passowrd("imadmin")
        log.info(
            "User: {0}".format(
                {"id": user.id, "name": user.name, "is_admin": user.is_admin}
            )
        )

        entry = db.get_or_404(Entry, 1)
        assert entry.user_id == 1
        assert entry.data == "admin's data 1"
        log.info(
            "Entry: {0}".format(
                {"id": entry.id, "user": entry.user.name, "data": entry.data}
            )
        )

        with pytest.raises(NotFound, match="^404 Not Found"):
            db.get_or_404(Role, 999)
        with pytest.raises(NotFound, match="^404 Not Found"):
            db.get_or_404(User, 999)
        with pytest.raises(NotFound, match="^404 Not Found"):
            db.get_or_404(Entry, 999)

    def test_fsa_property(
        self, db_models: Tuple[fsc.SQLAlchemyProxy, ModelTypes]
    ) -> None:
        """Test: Check the model properties' behaviors."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        _, (_, Role, User, _) = db_models

        for role in Role.query:
            assert isinstance(role, Role)
            expected_is_admin = role.level < 10
            assert role.is_admin is expected_is_admin
            log.info(
                "Role: {0}".format(
                    {
                        "id": role.id,
                        "is_admin": role.is_admin,
                        "expected": expected_is_admin,
                    }
                )
            )

        for user in User.query:
            assert isinstance(user, User)
            expected_is_admin = len(user.roles) > 0 and any(
                role.is_admin for role in user.roles
            )
            assert user.is_admin is expected_is_admin
            log.info(
                "User: {0}".format(
                    {
                        "id": user.id,
                        "is_admin": user.is_admin,
                        "expected": expected_is_admin,
                    }
                )
            )

    def test_fsa_query_by_properties(
        self, db_models: Tuple[fsc.SQLAlchemyProxy, ModelTypes]
    ) -> None:
        """Test: Check the query on the hybrid properties."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        _, (_, Role, User, _) = db_models

        role_ids = tuple(
            role.id for role in Role.query.filter(Role.is_admin).order_by(Role.id)
        )
        log.info("Get all admin roles: {0}".format(role_ids))
        assert role_ids == (1,)

        role_ids = tuple(
            role.id
            for role in Role.query.filter(sa.not_(Role.is_admin)).order_by(Role.id)
        )
        log.info("Get all not admin roles: {0}".format(role_ids))
        assert role_ids == (2,)

        user_ids = tuple(
            user.id for user in User.query.filter(User.is_admin).order_by(User.id)
        )
        log.info("Get all admin users: {0}".format(user_ids))
        assert user_ids == (1, 3)

        user_ids = tuple(
            user.id
            for user in User.query.filter(sa.not_(User.is_admin)).order_by(User.id)
        )
        log.info("Get all not admin users: {0}".format(user_ids))
        assert user_ids == (2, 4)

    def test_fsa_query_by_relationships(
        self, db_models: Tuple[fsc.SQLAlchemyProxy, ModelTypes]
    ) -> None:
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, (_, Role, User, Entry) = db_models

        def group_index(item: Tuple["m_fsqla.User", int]) -> int:
            return item[0].id

        user_roles = (
            db.session.query(User, Role.id)
            .join(Role, User.roles)
            .order_by(User.id, Role.id)
        )

        user_role_groups = [
            (user_id, tuple(item[1] for item in group))
            for user_id, group in itertools.groupby(
                (tuple(item) for item in user_roles), group_index
            )
        ]
        for user_id, role_ids in user_role_groups:
            user = db.get_or_404(User, user_id)
            expected_roles = tuple(sorted(role.id for role in user.roles))
            assert role_ids == expected_roles
            log.info(
                "User: {0}, User.roles: {1}, Expected User.roles: {2}".format(
                    user_id, role_ids, expected_roles
                )
            )

        user_entries = (
            db.session.query(User, Entry.id)
            .join(Entry, User.entries)
            .order_by(User.id, Entry.id)
        )

        user_entry_groups = [
            (user_id, tuple(item[1] for item in group))
            for user_id, group in itertools.groupby(
                (tuple(item) for item in user_entries), group_index
            )
        ]
        for user_id, entry_ids in user_entry_groups:
            user = db.get_or_404(User, user_id)
            expected_entries = tuple(sorted(entry.id for entry in user.entries))
            assert entry_ids == expected_entries
            log.info(
                "User: {0}, User.entries: {1}, Expected User.entries: {2}".format(
                    user_id, entry_ids, expected_entries
                )
            )


class TestFlaskSQLAlchemyLite:
    """Test the functionalities of Flask SQLAlchemy Lite and its proxy class. The
    coverage of the applications in this class scope contains the following cases:
    1. Use Flask SQLAlchemy Lite.
    2. Use Flask SQLAlchemy to mimic the usages of Flask SQLAlchemy Lite.
    """

    ModelTypes = Tuple[
        Type["m_fsqla_lite.Base"],
        Type["m_fsqla_lite.Role"],
        Type["m_fsqla_lite.User"],
        Type["m_fsqla_lite.Entry"],
    ]

    @pytest.fixture(
        scope="class", params=(True,) if sys.version_info < (3, 8) else (True, False)
    )
    def db_models(
        self, request: Any
    ) -> Generator[Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes], None, None]:
        """Database fixture. This fixture will deliver the Flask SQLAlchemy Lite
        database extension from two cases of applications. Each database will be
        applied to all testing methods in this class scope.

        Arguments
        ---------
        request: `_pytest.fixtures.SubRequest`
            The parameter set. Each time it is used, it will deliver the configurations
            of an application.

        Yields
        ------
        #1: `db: SQLAlchemyLiteProxy`
            The SQLAlchemy Lite database session.

        #2: `models: tuple[type[Base], type[Role], type[User], type[Entry]]`
            The models in the context of the current application.
        """
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        name = "fsqla_lite"
        use_module = request.param
        log.info(
            'Initialize the Flask app "{0}" and its SQLAlchemy'
            "extension.".format(name)
        )
        log.debug(
            "Flask SQLAlchemy Lite: {0}".format("Enabled" if use_module else "Disabled")
        )
        fsc.backends.proxy.fsa_lite = use_module
        with contextlib.ExitStack() as stk:
            app, db = import_app(
                "examples.app_{0}".format(name), "examples.models_{0}".format(name)
            )
            stk.enter_context(app.app_context())
            models = import_model_types("examples.models_{0}".format(name))
            yield db, models
        fsc.backends.proxy.fsa_lite = True
        log.info("Remove the Flask app.")
        del app
        del db

    def test_fsalite_dbname(
        self, db_models: Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes]
    ) -> None:
        """Test: Display the Flask SQLAlchemy Lite extension currently used by this
        case."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, _ = db_models
        log.info({"db": str(db), "module": db.__module__})

    def test_fsalite_get_by_id(
        self, db_models: Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes]
    ) -> None:
        """Test: Check whether the get-by-ID functionality works or not."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")

        db, (_, Role, User, Entry) = db_models
        role = db.session.get(Role, 1)
        assert role is not None
        assert role.name == "admin"
        assert role.is_admin is (role.level < 10)
        log.info(
            "Role: {0}".format(
                {"id": role.id, "name": role.name, "is_admin": role.is_admin}
            )
        )

        user = db.session.get(User, 1)
        assert user is not None
        assert user.name == "admin01"
        assert user.is_admin is (
            len(user.roles) > 0 and any(role.is_admin for role in user.roles)
        )
        assert user.validate_passowrd("imadmin")
        log.info(
            "User: {0}".format(
                {"id": user.id, "name": user.name, "is_admin": user.is_admin}
            )
        )

        entry = db.session.get(Entry, 1)
        assert entry is not None
        assert entry.user_id == 1
        assert entry.data == "admin's data 1"
        log.info(
            "Entry: {0}".format(
                {"id": entry.id, "user": entry.user.name, "data": entry.data}
            )
        )

        assert db.session.get(Role, 999) is None
        assert db.session.get(User, 999) is None
        assert db.session.get(Entry, 999) is None

    def test_fsalite_property(
        self, db_models: Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes]
    ) -> None:
        """Test: Check the model properties' behaviors."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, (_, Role, User, _) = db_models

        for role in db.session.scalars(sa.select(Role)):
            assert isinstance(role, Role)
            expected_is_admin = role.level < 10
            assert role.is_admin is expected_is_admin
            log.info(
                "Role: {0}".format(
                    {
                        "id": role.id,
                        "is_admin": role.is_admin,
                        "expected": expected_is_admin,
                    }
                )
            )

        for user in db.session.scalars(sa.select(User)):
            assert isinstance(user, User)
            expected_is_admin = len(user.roles) > 0 and any(
                role.is_admin for role in user.roles
            )
            assert user.is_admin is expected_is_admin
            log.info(
                "User: {0}".format(
                    {
                        "id": user.id,
                        "is_admin": user.is_admin,
                        "expected": expected_is_admin,
                    }
                )
            )

    def test_fsalite_query_by_properties(
        self, db_models: Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes]
    ) -> None:
        """Test: Check the query on the hybrid properties."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, (_, Role, User, _) = db_models

        role_ids = tuple(
            role.id
            for role in db.session.scalars(
                sa.select(Role).filter(Role.is_admin).order_by(Role.id)
            )
        )
        log.info("Get all admin roles: {0}".format(role_ids))
        assert role_ids == (1,)

        role_ids = tuple(
            role.id
            for role in db.session.scalars(
                sa.select(Role).filter(sa.not_(Role.is_admin)).order_by(Role.id)
            )
        )
        log.info("Get all not admin roles: {0}".format(role_ids))
        assert role_ids == (2,)

        user_ids = tuple(
            user.id
            for user in db.session.scalars(
                sa.select(User).filter(User.is_admin).order_by(User.id)
            )
        )
        log.info("Get all admin users: {0}".format(user_ids))
        assert user_ids == (1, 3)

        user_ids = tuple(
            user.id
            for user in db.session.scalars(
                sa.select(User).filter(sa.not_(User.is_admin)).order_by(User.id)
            )
        )
        log.info("Get all not admin users: {0}".format(user_ids))
        assert user_ids == (2, 4)

    def test_fsalite_query_by_relationships(
        self, db_models: Tuple[fsc.SQLAlchemyLiteProxy, ModelTypes]
    ) -> None:
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        db, (_, Role, User, Entry) = db_models

        def group_index(item: Tuple["m_fsqla.User", int]) -> int:
            return item[0].id

        user_roles = db.session.execute(
            sa.select(User, Role.id).join(Role, User.roles).order_by(User.id, Role.id)
        )

        user_role_groups = [
            (user_id, tuple(item[1] for item in group))
            for user_id, group in itertools.groupby(
                (tuple(item) for item in user_roles), group_index
            )
        ]
        for user_id, role_ids in user_role_groups:
            user = db.session.get(User, user_id)
            assert user is not None
            expected_roles = tuple(sorted(role.id for role in user.roles))
            assert role_ids == expected_roles
            log.info(
                "User: {0}, User.roles: {1}, Expected User.roles: {2}".format(
                    user_id, role_ids, expected_roles
                )
            )

        user_entries = db.session.execute(
            sa.select(User, Entry.id)
            .join(Entry, User.entries)
            .order_by(User.id, Entry.id)
        )

        user_entry_groups = [
            (user_id, tuple(item[1] for item in group))
            for user_id, group in itertools.groupby(
                (tuple(item) for item in user_entries), group_index
            )
        ]
        for user_id, entry_ids in user_entry_groups:
            user = db.session.get(User, user_id)
            assert user is not None
            expected_entries = tuple(sorted(entry.id for entry in user.entries))
            assert entry_ids == expected_entries
            log.info(
                "User: {0}, User.entries: {1}, Expected User.entries: {2}".format(
                    user_id, entry_ids, expected_entries
                )
            )
