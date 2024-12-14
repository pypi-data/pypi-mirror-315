# SPDX-FileCopyrightText: b5327157 <b5327157@protonmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import fnmatch
import itertools
import logging
import os
import pathlib
import shutil
import subprocess

from collections.abc import Iterable, Mapping, Sequence
from typing import IO, Any, Literal, Optional, Protocol, overload

import nox
import nox.command
import nox.logger
import nox.popen

nox.needs_version = ">= 2024.4.15"

nox.options.default_venv_backend = "uv|venv"
nox.options.error_on_external_run = True
nox.options.error_on_missing_interpreters = True
nox.options.sessions = ["lint"]


def tag_cachedir(dir: pathlib.Path) -> None:  # noqa: A002
    dir.mkdir(parents=True, exist_ok=True)
    pathlib.Path(dir, "CACHEDIR.TAG").write_bytes(b"Signature: 8a477f597d28d172789f06886806bc55\n")


if __file__:
    tag_cachedir(pathlib.Path(__file__).parent / ".nox")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("black[colorama] >= 24.10.0, < 25")
    session.install("flake8 >= 7.1.1, < 8")
    session.install("flake8-bandit >= 4.1.1, < 5")
    session.install("flake8-builtins >= 2.5.0, < 3")
    session.install("flake8-deprecated >= 2.2.1, < 3")
    session.install("flake8-pep585 >= 0.1.7, < 1")
    session.install("isort[colors] >= 5.13.2, < 6")
    session.install("mypy[faster-cache] >= 1.13.0, < 2")
    session.install("nox >= 2024.10.9, < 2025")
    session.install("pep8-naming >= 0.14.1, < 1")
    session.install("pyright >= 1.1.390, < 2")
    session.install("reuse >= 5.0.2, < 6")
    session.install("shellcheck-py >= 0.10.0.1, < 1")
    session.install("shfmt-py >= 3.7.0.1, < 4")

    session.install(".")

    posargs_paths = session.posargs

    fix = False
    if posargs_paths and posargs_paths[0] == "--fix":
        posargs_paths = posargs_paths[1:]
        fix = True

    posargs_paths = [str(pathlib.Path(session.invoked_from, path)) for path in posargs_paths]

    default_paths = ["no_vtf_desktop", "noxfile.py", "builds"]

    paths = [pathlib.Path(path) for path in (posargs_paths or default_paths)]
    py_paths = [path for path in paths if path.is_dir() or path.name.endswith(".py")]
    sh_paths = list(
        itertools.chain.from_iterable(
            (
                path.rglob("*.sh*")
                if path.is_dir()
                else [path] if fnmatch.fnmatch(path.name, "*.sh*") else []
            )
            for path in paths
        )
    )

    shfmt = ["shfmt", "--simplify", "--func-next-line"]

    if not fix:
        if py_paths:
            session.run(
                "mypy",
                "--pretty",
                "--show-error-context",
                "--explicit-package-bases",
                "--",
                *py_paths,
            )
            session.run("pyright", "--warnings", *py_paths)
            session.run("flake8", "--", *py_paths, silent=True)
            session.run("isort", "--check", "--diff", "--", *py_paths)
            session.run("black", "--check", "--diff", "--", *py_paths)

        if sh_paths:
            session.run(
                "shellcheck",
                "--norc",
                "--external-sources",
                "--severity=style",
                "--enable=all",
                "--exclude=" + ",".join(["SC2016", "SC2032", "SC2033", "SC2250", "SC2292"]),
                "--format=gcc",
                "--",
                *sh_paths,
            )
            session.run(*shfmt, "--diff", "--", *sh_paths)

        session.run("reuse", "lint", silent=True)
    else:
        if py_paths:
            session.run("isort", "--", *py_paths)
            session.run("black", "--", *py_paths)

        if sh_paths:
            session.run(*shfmt, "--write", "--", *sh_paths)


@nox.session
def package(session: nox.Session) -> None:
    session.install("build >= 1.2.2.post1, < 2")

    nox_session_install_only_end(session)

    path_dist = pathlib.Path("dist")
    if path_dist.is_dir():
        dist_files = [path for path in path_dist.iterdir() if path.is_file()]
        for dist_file in dist_files:
            dist_file.unlink()

    session.run("python", "-m", "build", silent=True)

    path_sdist = next(path_dist.glob("*.tar.gz"))
    path_wheel = next(path_dist.glob("*.whl"))

    nox_session_run_pip(session.run, "install", "--force-reinstall", str(path_wheel))

    executable = ["no_vtf-desktop"]
    session.run(*executable, "--version")

    if len(session.posargs) >= 1:
        shutil.copy2(path_sdist, pathlib.Path(session.invoked_from, session.posargs[0]))

    if len(session.posargs) >= 2:
        shutil.copy2(path_wheel, pathlib.Path(session.invoked_from, session.posargs[1]))


@nox.session
def publish(session: nox.Session) -> None:
    session.install("twine >= 6.0.1, < 7")

    nox_session_install_only_end(session)

    if not session.posargs:
        session.error("Path to API token file was not provided")

    dist = pathlib.Path("dist")
    dist_files = [path for path in dist.iterdir() if path.is_file()]
    dist_args = [str(path) for path in dist_files]

    session.run("twine", "check", "--strict", *dist_args)

    upload_args: list[str] = []
    upload_args.append("--non-interactive")
    upload_args.append("--disable-progress-bar")
    upload_args.extend(dist_args)

    env = session.env.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = (
        pathlib.Path(session.invoked_from, session.posargs[0]).read_text().strip()
    )

    nox_command_run(
        ["twine", "upload", *upload_args],
        env=env,
        paths=session.bin_paths,
    )


def nox_session_is_install_only(session: nox.Session) -> bool:
    logger = nox.logger.logger
    logger_level = logger.level
    try:
        logger.setLevel(logging.WARNING)
        return session.run("python", "--version", silent=True, log=False) is None
    finally:
        logger.setLevel(logger_level)


def nox_session_install_only_end(session: nox.Session) -> None:
    if nox_session_is_install_only(session):
        session.log("Skipping rest of the session, as --install-only is set.")
        session.skip()


class NoxSessionRunner(Protocol):
    def __call__(
        self,
        *args: str | os.PathLike[str],
        env: Mapping[str, str | None] | None = None,
        include_outer_env: bool = True,
        silent: bool = False,
        success_codes: Iterable[int] | None = None,
        log: bool = True,
        external: nox.command.ExternalType | None = None,
        stdout: int | IO[str] | None = None,
        stderr: int | IO[str] = subprocess.STDOUT,
        interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
        terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
    ) -> Any | None: ...


def nox_session_get_runner(
    session: nox.Session, *, install_only: bool = False, no_install: bool = True
) -> NoxSessionRunner:
    match nox_session_is_install_only(session), install_only, no_install:
        case _, False, True:
            return session.run
        case _, True, False:
            return session.run_install
        case False, True, True:
            return session.run
        case True, True, True:
            return session.run_install
        case False, False, False:
            return session.run_install
        case True, False, False:
            return session.run

    assert False, "unreachable"  # noqa S101


@overload
def nox_session_run_pip(
    runner: NoxSessionRunner,
    *args: str,
    env: Mapping[str, str] | None = None,
    include_outer_env: bool = True,
    silent: Literal[False] = False,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> Optional[bool]: ...


@overload
def nox_session_run_pip(
    runner: NoxSessionRunner,
    *args: str,
    env: Mapping[str, str] | None = None,
    include_outer_env: bool = True,
    silent: Literal[True] = True,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> Optional[str]: ...


@overload
def nox_session_run_pip(
    runner: NoxSessionRunner,
    *args: str,
    env: Mapping[str, str] | None = None,
    include_outer_env: bool = True,
    silent: bool = False,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> Optional[str | bool]: ...


def nox_session_run_pip(
    runner: NoxSessionRunner,
    *args: str,
    env: Mapping[str, str] | None = None,
    include_outer_env: bool = True,
    silent: bool = False,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> Optional[str | bool]:
    session = getattr(runner, "__self__", None)
    if not isinstance(session, nox.Session):
        raise ValueError(f"runner.__self__: expected nox.Session, got {type(session).__name__}")

    if external is None:
        external = "error" if nox.options.error_on_external_run else False

    env = {
        **(env or {}),
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PIP_NO_INPUT": "1",
        "PIP_PROGRESS_BAR": "off",
        "PIP_NO_PYTHON_VERSION_WARNING": "1",
    }

    pip = (
        ["uv", "--no-progress", "pip"] if session.venv_backend == "uv" else ["python", "-m", "pip"]
    )

    return runner(
        *pip,
        *args,
        env=env,
        include_outer_env=include_outer_env,
        silent=silent,
        success_codes=success_codes,
        log=log,
        external=external,
        stdout=stdout,
        stderr=stderr,
        interrupt_timeout=interrupt_timeout,
        terminate_timeout=terminate_timeout,
    )


@overload
def nox_command_run(
    args: Sequence[str | os.PathLike[str]],
    *,
    env: Mapping[str, str | None] | None = None,
    silent: Literal[False] = False,
    paths: Sequence[str] | None = None,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> bool: ...


@overload
def nox_command_run(
    args: Sequence[str | os.PathLike[str]],
    *,
    env: Mapping[str, str | None] | None = None,
    silent: Literal[True] = True,
    paths: Sequence[str] | None = None,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> str: ...


@overload
def nox_command_run(
    args: Sequence[str | os.PathLike[str]],
    *,
    env: Mapping[str, str | None] | None = None,
    silent: bool = False,
    paths: Sequence[str] | None = None,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> str | bool: ...


def nox_command_run(
    args: Sequence[str | os.PathLike[str]],
    *,
    env: Mapping[str, str | None] | None = None,
    silent: bool = False,
    paths: Sequence[str] | None = None,
    success_codes: Iterable[int] | None = None,
    log: bool = True,
    external: Optional[nox.command.ExternalType] = None,
    stdout: int | IO[str] | None = None,
    stderr: int | IO[str] = subprocess.STDOUT,
    interrupt_timeout: float | None = nox.popen.DEFAULT_INTERRUPT_TIMEOUT,
    terminate_timeout: float | None = nox.popen.DEFAULT_TERMINATE_TIMEOUT,
) -> str | bool:
    if external is None:
        external = "error" if nox.options.error_on_external_run else False
    assert external is not None  # noqa S101 type narrowing

    return nox.command.run(
        args,
        env=env,
        silent=silent,
        paths=paths,
        success_codes=success_codes,
        log=log,
        external=external,
        stdout=stdout,
        stderr=stderr,
        interrupt_timeout=interrupt_timeout,
        terminate_timeout=terminate_timeout,
    )
