# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

import pytest

import typing

if typing.TYPE_CHECKING:
    from pathlib import Path


def test_install(test_case: Path, venv) -> None:
    venv.pip("install", str(test_case))
