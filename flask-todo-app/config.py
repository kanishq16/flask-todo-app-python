"""
Configuration for the Flask Todo App.

Values can be overridden via environment variables, which is the
recommended approach for production deployments.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "instance", "todos.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
