# -*- coding: UTF-8 -*-
"""
Applications
============
@ Flask SQLAlchemy Compat - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the complete applications, where each application implements the APIs
accessing the database, respectively. The applications are defined in the `examples`
folder.
"""

import sys
import itertools
import collections.abc
import logging

from typing import Any

try:
    from typing import Mapping, Generator
except ImportError:
    from collections.abc import Mapping, Generator

import pytest

from flask import Flask
from flask import url_for
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

import flask_sqlalchemy_compat as fsc

from .utils import import_app, create_test_db, dispose_test_db


__all__ = ("init_db_data", "TestFlaskApps")


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


class TestFlaskApps:
    """Test the functionalities of complete Flask apps implemented with
    `flask_sqlalchemy`, `flask_sqlalchemy_lite`, and their proxies. The same set
    of requests will be sent to the following four application cases:
    1. Use Flask SQLAlchemy.
    2. Use Flask SQLAlchemy Lite to mimic the usages of Flask SQLAlchemy.
    3. Use Flask SQLAlchemy Lite.
    4. Use Flask SQLAlchemy to mimic the usages of Flask SQLAlchemy Lite.
    """

    @pytest.fixture(
        scope="class",
        params=itertools.product(
            ("fsqla", "fsqla_lite"),
            (True,) if sys.version_info < (3, 8) else (True, False),
        ),
    )
    def app(self, request: Any) -> Generator[Flask, None, None]:
        """Application fixture. This fixture will deliver four cases of applications.
        Each application will be applied to all testing methods in this class scope.

        Arguments
        ---------
        request: `_pytest.fixtures.SubRequest`
            The parameter set. Each time it is used, it will deliver the configurations
            of an application.
        """
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        name, use_module = request.param
        log.info("Initialize the Flask app: {0}.".format(name))
        if name == "fsqla":
            log.debug(
                "Flask SQLAlchemy: {0}".format("Enabled" if use_module else "Disabled")
            )
            fsc.backends.proxy.fsa = use_module
        elif name == "fsqla_lite":
            log.debug(
                "Flask SQLAlchemy Lite: {0}".format(
                    "Enabled" if use_module else "Disabled"
                )
            )
            fsc.backends.proxy.fsa_lite = use_module
        app, _ = import_app(
            "examples.app_{0}".format(name), "examples.models_{0}".format(name)
        )
        yield app
        fsc.backends.proxy.fsa = True
        fsc.backends.proxy.fsa_lite = True
        log.info("Remove the Flask app.")
        del app

    @staticmethod
    def _get_json_data(
        resp: TestResponse, need_status: bool = True
    ) -> Mapping[str, Any]:
        """Require a mapping of JSON-formatted data from the response.

        Arguments
        ---------
        resp: `TestResponse`
            The reponse to be parsed.

        need_status: `bool`
            If enabled, will check whether the response has a status code `<400`.
        """
        if need_status:
            assert resp.status_code < 400
        assert resp.is_json
        data = resp.get_json()
        assert isinstance(data, collections.abc.Mapping)
        return data

    def test_apps_dbname(self, client: FlaskClient) -> None:
        """Test: Display the Flask SQLAlchemy extension currently used by this case."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")
        resp = client.get(url_for("dbname"), follow_redirects=True)
        assert resp.status_code < 400
        assert resp.is_json
        log.info(resp.get_json())

    def test_apps_as_admin(self, client: FlaskClient) -> None:
        """Test: Test the application by logging in with an administrator account."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")

        user_name = "admin01"
        log.info("Test the performance with the user name: {0}".format(user_name))

        resp = client.get(url_for("login"), follow_redirects=True)
        data = self._get_json_data(resp)
        assert data["message"].startswith("Use POST method")
        log.info(data)

        resp = client.post(
            url_for("login"),
            json={"user": user_name, "password": "imadmin"},
            follow_redirects=True,
        )
        data = self._get_json_data(resp)
        assert data["message"].startswith("Hi, {0}".format(user_name))
        log.info(data)

        resp = client.get(url_for("user"), follow_redirects=True)
        data = self._get_json_data(resp)
        log.info(data)

        assert "users" in data
        users = data["users"]
        assert isinstance(users, collections.abc.Sequence)
        assert len(users) == 4
        user = users[0]
        for _user in users:
            assert isinstance(_user, collections.abc.Mapping)
            if _user["name"] != user_name:
                user = _user
                break
        assert isinstance(user, collections.abc.Mapping)
        user_id = user["id"]
        assert isinstance(user_id, int)

        resp = client.get(
            url_for("user"), query_string={"id": user_id}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["id"] == user_id
        assert data["name"] == user["name"]

        resp = client.get(url_for("entry"), follow_redirects=True)
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 1
        assert tuple(data["entries"]) == (1, 2)

        resp = client.get(
            url_for("entry"), query_string={"user": 2}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 2
        assert tuple(data["entries"]) == (3, 4)

        resp = client.get(
            url_for("entry"), query_string={"id": 1}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 1
        assert data["data"] == "admin's data 1"

        resp = client.get(
            url_for("entry"), query_string={"user": 2, "id": 4}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 2
        assert data["data"] == "reader's data 2"

        resp = client.post(url_for("logout"), follow_redirects=True)
        data = self._get_json_data(resp)
        assert data["message"].startswith("Use POST method")
        log.info(data)

    def test_apps_as_reader(self, client: FlaskClient) -> None:
        """Test: Test the application by logging in with a plain user account."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")

        user_name = "reader01"
        log.info("Test the performance with the user name: {0}".format(user_name))

        resp = client.get(url_for("login"), follow_redirects=True)
        data = self._get_json_data(resp)
        assert data["message"].startswith("Use POST method")
        log.info(data)

        resp = client.post(
            url_for("login"),
            json={"user": user_name, "password": "regular"},
            follow_redirects=True,
        )
        data = self._get_json_data(resp)
        assert data["message"].startswith("Hi, {0}".format(user_name))
        log.info(data)

        resp = client.get(url_for("user"), follow_redirects=True)
        assert resp.status_code >= 400
        data = self._get_json_data(resp, need_status=False)
        log.info(data)

        resp = client.get(url_for("entry"), follow_redirects=True)
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 2
        assert tuple(data["entries"]) == (3, 4)

        resp = client.get(
            url_for("entry"), query_string={"user": 1}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 2
        assert tuple(data["entries"]) == (3, 4)

        resp = client.get(
            url_for("entry"), query_string={"id": 3}, follow_redirects=True
        )
        data = self._get_json_data(resp)
        log.info(data)
        assert data["user"] == 2
        assert data["data"] == "reader's data 1"

        resp = client.get(
            url_for("entry"), query_string={"user": 1, "id": 1}, follow_redirects=True
        )
        assert resp.status_code > 400
        data = self._get_json_data(resp, need_status=False)
        log.info(data)
        assert "data" not in data
        assert data["message"] == "Requested entry is not found."

        resp = client.post(url_for("logout"), follow_redirects=True)
        data = self._get_json_data(resp)
        assert data["message"].startswith("Use POST method")
        log.info(data)

    def test_apps_not_login(self, client: FlaskClient) -> None:
        """Test: Test the application by not logging in."""
        log = logging.getLogger("flask_sqlalchemy_compat.test")

        log.info("Test the performance when not logging in.")

        resp = client.get(url_for("login"), follow_redirects=True)
        data = self._get_json_data(resp)
        assert data["message"].startswith("Use POST method")
        log.info(data)

        resp = client.get(url_for("user"), follow_redirects=True)
        assert resp.status_code >= 400
        data = self._get_json_data(resp, need_status=False)
        log.info(data)

        resp = client.get(url_for("entry"), follow_redirects=True)
        assert resp.status_code >= 400
        data = self._get_json_data(resp, need_status=False)
        log.info(data)

        resp = client.get(url_for("logout"), follow_redirects=True)
        assert resp.status_code >= 400
        data = self._get_json_data(resp, need_status=False)
        log.info(data)
