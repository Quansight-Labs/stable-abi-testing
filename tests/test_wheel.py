# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

from build import ProjectBuilder

import typing

if typing.TYPE_CHECKING:
    from pathlib import Path


def test_install(test_case: Path, tmp_path: Path, venv) -> None:
    builder = ProjectBuilder(test_case)
    dist_path = builder.build("wheel", tmp_path)
    venv.pip("install", dist_path)
