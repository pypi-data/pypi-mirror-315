"""Pytest configurations
"""

import logging


def pytest_configure(config):
    """Pytest global configurations."""

    # Disable the most logs from werkzeug.
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
