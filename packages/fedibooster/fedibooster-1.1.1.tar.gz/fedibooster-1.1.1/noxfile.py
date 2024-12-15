# ruff: noqa: D100, D103


import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = [
    "mypy",
    "ruff",
    "refactor",
    "interrogate",
    "pip_audit",
    "bandit",
    "pytest",
]


@nox.session(python=["3.11", "3.12", "3.13"])
def mypy(session):
    session.install("mypy", "types-toml", "types-aiofiles")
    session.run("mypy", "src/")


@nox.session
def ruff(session):
    session.install("ruff")
    session.run("ruff", "format", "src/")
    session.run("ruff", "check", "src/")


@nox.session
def refactor(session):
    session.install("codelimit<0.14.0")
    session.run("codelimit", "--version")
    session.run("codelimit", "check", "src")


@nox.session
def interrogate(session):
    session.install("interrogate", "setuptools")
    session.run("interrogate", "-vv", "src/")


@nox.session(python=["3.9", "3.10", "3.11", "3.12", "3.13"])
def pip_audit(session):
    session.install("pip-audit")
    session.run("pip-audit")


@nox.session(python=["3.11", "3.12", "3.13"])
def bandit(session):
    session.install("bandit", "PyYAML", "tomli", "GitPython", "sarif-om", "jschema-to-python")
    session.run("bandit", "-r", "src/")


@nox.session(python=["3.11", "3.12"])  # Python 3.13 not yet supported... again something to do with msgspec
def pytest(session):
    session.install("-e", ".")
    session.install("pytest-cov", "pytest-asyncio", "pytest-httpx")
    session.run("pytest", "-vv", "--cov-report", "term-missing", "--cov=fedibooster", "tests")
