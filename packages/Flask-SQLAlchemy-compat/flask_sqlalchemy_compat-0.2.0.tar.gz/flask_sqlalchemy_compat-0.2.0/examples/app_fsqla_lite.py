# -*- coding: UTF-8 -*-
"""
Application with Flask SQLAlchemy Lite
======================================
@ Flask SQLAlchemy Compat - Examples

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The implementation of services based on Flask SQLAlchemy Lite.
"""

import os
from hashlib import blake2b

from typing import Optional, cast

import sqlalchemy as sa

import flask
from flask import request

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
    LoginManager,
)

from werkzeug.exceptions import HTTPException

from .models_fsqla_lite import db, Base, User, Role, Entry


def get_secret(key: str) -> bytes:
    h_blake2b = blake2b(key=key.encode("utf-8"), digest_size=16)
    h_blake2b.update(key[::-1].encode("utf-8"))
    return h_blake2b.digest()


app = flask.Flask(
    __name__,
    instance_path=os.path.abspath(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    ),
)
app.config.update({"SQLALCHEMY_ENGINES": {"default": "sqlite:///main.db"}})
APP_SECRET: str = "Something random, used as the secret key."
app.secret_key = get_secret(APP_SECRET)

login_manager = LoginManager()

db.init_app(app)
print(db)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: int) -> Optional[User]:
    return db.session.get(User, user_id)


@app.route("/")
def index():
    """Index: Welcome message."""
    user = cast(Optional[User], current_user)
    if user is None or user.is_anonymous:
        return flask.redirect(flask.url_for("login"))
    if user.is_admin:
        return flask.make_response(
            {
                "message": (
                    "Hi, {0}! As an admin, you can review /user or "
                    "/entry.".format(user.name)
                )
            }
        )
    return flask.make_response(
        {"message": "Hi, {0}! You can review /entry.".format(user.name)}
    )


@app.route("/dbname")
def dbname():
    """Currently used DB name."""
    return flask.make_response(
        {"message": "Get the DB name.", "name": str(db), "module": db.__module__}
    )


@app.route("/user")
@login_required
def user():
    _current_user = cast(User, current_user)
    if not _current_user.is_admin:
        return flask.abort(
            flask.make_response(
                {"message": "You do not have the access to this page."}, 403
            )
        )
    args = request.args
    user_id = args.get("id", None)
    if user_id is None:
        return flask.make_response(
            {
                "message": "Users are found.",
                "users": tuple(
                    {"id": val[0], "name": val[1]}
                    for val in db.session.execute(
                        sa.select(User.id, User.name).order_by(User.id)
                    )
                ),
            }
        )
    try:
        user_id = int(user_id)
    except ValueError:
        return flask.abort(
            flask.make_response(
                {"message": "Specify a invalid id.", "id": str(user_id)}, 404
            )
        )
    _user: Optional[User] = db.session.get(User, user_id)
    if _user is None:
        return flask.abort(
            flask.make_response(
                {"message": "Requested user is not found.", "id": user_id}, 404
            )
        )
    return flask.make_response(
        {
            "message": "User is found.",
            "id": _user.id,
            "name": _user.name,
            "roles": [{"name": role.name, "level": role.level} for role in _user.roles],
            "n_entries": db.session.scalar(
                sa.select(sa.func.count(Entry.id)).where(Entry.user_id == _user.id)
            ),
        }
    )


@app.route("/entry")
@login_required
def entry():
    _current_user = cast(User, current_user)
    args = request.args
    if _current_user.is_admin:
        user_id = args.get("user", None)
        try:
            user_id = int(user_id) if user_id is not None else None
        except ValueError:
            user_id = None
    else:
        user_id = None
    entry_id = args.get("id", None)
    try:
        entry_id = int(entry_id) if entry_id is not None else None
    except ValueError:
        entry_id = None

    if user_id is None:
        user_id = _current_user.id
    if entry_id is None:
        entry_ids = db.session.scalars(
            sa.select(Entry.id).where(Entry.user_id == user_id).order_by(Entry.id)
        ).all()
        return flask.make_response(
            {
                "message": "Entries are found.",
                "user": user_id,
                "n_entries": len(entry_ids),
                "entries": entry_ids,
            }
        )
    _entry: Optional[Entry] = db.session.scalar(
        sa.select(Entry).filter(Entry.id == entry_id, Entry.user_id == user_id)
    )
    if _entry is None:
        return flask.abort(
            flask.make_response(
                {
                    "message": "Requested entry is not found.",
                    "user": user_id,
                    "id": entry_id,
                },
                404,
            )
        )
    return flask.make_response(
        {
            "message": "Entry is found.",
            "user": user_id,
            "id": entry_id,
            "data": _entry.data,
        }
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    method = request.method
    if method == "GET":
        return flask.make_response(
            {"message": "Use POST method and provide user/password to login."}
        )
    elif method == "POST":
        data = request.get_json()
        user_name = data.get("user")
        if not (isinstance(user_name, str) and user_name):
            return flask.abort(
                flask.make_response({"message": "The user name is not specified."}, 404)
            )
        user: Optional[User] = db.session.scalar(
            sa.select(User).filter(User.name == user_name)
        )
        if user is None:
            return flask.abort(
                flask.make_response({"message": "The request user is not found."}, 404)
            )
        password = data.get("password")
        if not (isinstance(password, str) and password):
            return flask.abort(
                flask.make_response({"message": "The password is not specified."}, 404)
            )
        if not user.validate_passowrd(password):
            return flask.abort(
                flask.make_response({"message": "The password is wrong."}, 403)
            )
        login_user(user)
        flask.flash("Logged in successfully.")
        return flask.redirect(flask.url_for("index"))
    return flask.abort(
        flask.make_response({"message": "The method is not allowed."}, 405)
    )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    return flask.abort(
        flask.make_response(
            {"message": "This API cannot be accessed without logging in."}, 401
        )
    )


@app.errorhandler(HTTPException)
def handle_exception(exc: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = flask.make_response(
        {
            "code": exc.code,
            "name": exc.name,
            "description": exc.description,
        },
        exc.code,
        exc.get_headers(),
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    import socket

    def get_ip(method: str = "broadcast") -> str:
        """Detect the IP address of this device."""
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            if method == "broadcast":
                s_socket.connect(("10.255.255.255", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "udp":
                s_socket.connect(("8.8.8.8", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "host":
                ip_value = socket.gethostbyname(socket.gethostname())
            else:
                raise ConnectionError
        except Exception:  # pylint: disable=broad-except
            ip_value = "localhost"
        finally:
            s_socket.close()
        return ip_value

    def init_db():
        with app.app_context():
            Base.metadata.drop_all(db.engine)
            Base.metadata.create_all(db.engine)

            role_admin = Role(name="admin", level=0)
            role_reader = Role(name="reader", level=100)

            db.session.add(role_admin)
            db.session.add(role_reader)
            db.session.commit()

            user = User(name="admin01")
            user.set_password("imadmin")
            user.roles.append(role_admin)
            user.roles.append(role_reader)
            Entry(data="admin's data 1", user_id=user.id, user=user)
            Entry(data="admin's data 2", user_id=user.id, user=user)
            db.session.add(user)

            user = User(name="reader01")
            user.set_password("regular")
            user.roles.append(role_reader)
            Entry(data="reader's data 1", user_id=user.id, user=user)
            Entry(data="reader's data 2", user_id=user.id, user=user)
            db.session.add(user)

            user = User(name="admin02")
            user.set_password("imanotheradmin")
            user.roles.append(role_admin)
            Entry(data="admin's data 3", user_id=user.id, user=user)
            Entry(data="admin's data 4", user_id=user.id, user=user)
            db.session.add(user)

            user = User(name="reader02")
            user.set_password("regular2")
            user.roles.append(role_reader)
            Entry(data="reader's data 3", user_id=user.id, user=user)
            db.session.add(user)
            db.session.commit()
            db.session.commit()

    with app.app_context():
        init_db()
    app.run(host=get_ip(), port=8080)
