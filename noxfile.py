"""Nox sessions."""

import os
import shlex
import sys
from pathlib import Path
from textwrap import dedent

import nox
import toml

try:
    from nox_poetry import Session
    from nox_poetry import session
except ImportError:
    message = f"""\
    Nox failed to import the 'nox-poetry' package.

    Please install it using the following command:

    {sys.executable} -m pip install nox-poetry"""
    raise SystemExit(dedent(message)) from None


package = "repo_manager"
python_versions = [
    "3.11",
]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = (
    # "safety",
    # "mypy",
    "tests",
)
pyproject = toml.load("pyproject.toml")
test_requirements = pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"].keys()
mypy_type_packages = [requirement for requirement in test_requirements if requirement.startswith("types-")]


@session(python=python_versions[0])
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    requirements = session.poetry.export_requirements()
    session.install("safety")
    # ignore https://github.com/pytest-dev/py/issues/287
    # its an irresposnbily filed CVE causing nose
    session.run("safety", "check", "--full-report", f"--file={requirements}", "--ignore=51457")


@session(python=python_versions)
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or ["repo_manager", "--follow-imports=silent", "--ignore-missing-imports"]
    session.install(".")
    session.install("mypy", "pytest")
    if len(mypy_type_packages) > 0:
        session.install(*mypy_type_packages)
    session.run("mypy", *args)


@session(python=python_versions)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.install(".")
    session.install(*test_requirements)
    session.run("poetry", "run", "pytest", *session.posargs)
