# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

from build import ProjectBuilder
import pytest

from pathlib import Path
import sysconfig


IS_FREETHREADING = sysconfig.get_config_var("Py_GIL_DISABLED") == 1
XFAIL_CYTHON = pytest.mark.xfail(
    IS_FREETHREADING,
    reason="https://github.com/cython/cython/issues/7399#issuecomment-3710960697",
)
XFAIL_NANOBIND = pytest.mark.xfail(
    IS_FREETHREADING,
    reason="nanobind does not support PEP 803 yet",
)
XFAIL_PYO3 = pytest.mark.xfail(
    IS_FREETHREADING,
    reason="pyo3 does not support 3.15 (or PEP 803) yet",
)

TOP_DIR = Path(__file__).parent.parent
TEST_CASES = [
    pytest.param("maturin/rust", marks=[XFAIL_PYO3]),
    "meson-python/c",
    pytest.param("meson-python/cython", marks=[XFAIL_CYTHON]),
    "scikit-build-core/c",
    pytest.param("scikit-build-core/cython", marks=[XFAIL_CYTHON]),
    pytest.param("scikit-build-core/nanobind", marks=[XFAIL_NANOBIND]),
    "setuptools/c",
    pytest.param("setuptools/cython", marks=[XFAIL_CYTHON]),
]

TEST_PROGRAM = """
from pathlib import Path

import limited

# if the build system created a package, import the actual extension
if hasattr(limited, "__path__"):
    from limited import limited

value = limited.add(1, 2)
assert value == 3, f"add(1, 2) == {value} instead of 3"

assert ".abi3" in Path(limited.__file__).name, (
    f"{limited.__file__} is not abi3 extension")
"""


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_install(test_case: str, tmp_path: Path, venv) -> None:
    builder = ProjectBuilder(TOP_DIR / test_case)
    dist_path = builder.build("wheel", tmp_path)
    venv.pip("install", dist_path)
    # -Werror to catch the exception when extension is not freethreading-compatible
    venv.python("-Werror", "-c", TEST_PROGRAM)
