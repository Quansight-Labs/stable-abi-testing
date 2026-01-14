# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

from build import ProjectBuilder
import pytest

from contextlib import contextmanager
from pathlib import Path
import sysconfig


IS_FREETHREADING = sysconfig.get_config_var("Py_GIL_DISABLED") == 1

TOP_DIR = Path(__file__).parent.parent
TEST_CASES = [
    "maturin/rust",
    "meson-python/c",
    "meson-python/cython",
    "scikit-build-core/c",
    "scikit-build-core/cython",
    "scikit-build-core/nanobind",
    "setuptools/c",
    "setuptools/cython",
]

TEST_CALL = """
import limited

value = limited.add(1, 2)
assert value == 3, f"add(1, 2) == {value} instead of 3"
"""

TEST_ABI3 = """
from pathlib import Path

import limited

# if the build system created a package, import the actual extension
if hasattr(limited, "__path__"):
    from limited import limited

assert ".abi3" in Path(limited.__file__).name, (
    f"{limited.__file__} is not abi3 extension")
"""


class XPASS(Exception):
    pass


@contextmanager
def subxfail(condition: bool, reason: str) -> None:
    if not condition:
        yield
    else:
        try:
            yield
        except Exception:
            pytest.xfail(reason)
        else:
            raise XPASS(reason)


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_install(test_case: str, tmp_path: Path, venv, subtests) -> None:
    build_system, _, language = test_case.partition("/")

    builder = ProjectBuilder(TOP_DIR / test_case)
    with subxfail(
        IS_FREETHREADING and language == "rust",
        reason="pyo3 does not support 3.15 (or PEP 803) yet",
    ):
        dist_path = builder.build("wheel", tmp_path)
    venv.pip("install", dist_path)

    with subtests.test(msg="extension works"):
        venv.python("-c", TEST_CALL)

    if IS_FREETHREADING:
        with subtests.test(msg="extensions does not enable GIL"):
            venv.python("-Werror", "-c", "import limited")

    with subtests.test(msg="extension has .abi3 suffix"):
        with subxfail(
            IS_FREETHREADING and language == "nanobind",
            reason="nanobind does not support PEP 803 yet",
        ):
            venv.python("-c", TEST_ABI3)
