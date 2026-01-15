# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

from build import ProjectBuilder
import pytest

from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
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
def test_install(test_case: str, tmp_path: Path, subtests) -> None:
    build_system, _, language = test_case.partition("/")

    builder = ProjectBuilder(TOP_DIR / test_case)
    with subxfail(
        IS_FREETHREADING and language == "rust",
        reason="pyo3 does not support 3.15 (or PEP 803) yet",
    ):
        dist_path = builder.build("wheel", tmp_path)

    subprocess.run([sys.executable, "-m", "venv", tmp_path / "venv"], check=True)
    venv_python = tmp_path / "venv/bin/python"
    subprocess.run([venv_python, "-m", "pip", "install", dist_path], check=True)

    with subtests.test(msg="extension works"):
        subprocess.run([venv_python, "-c", TEST_CALL], check=True)

    if IS_FREETHREADING:
        with subtests.test(msg="extensions does not enable GIL"):
            subprocess.run([venv_python, "-Werror", "-c", "import limited"], check=True)

    with subtests.test(msg="extension has .abi3 suffix"):
        with subxfail(
            IS_FREETHREADING and language == "nanobind",
            reason="nanobind does not support PEP 803 yet",
        ):
            subprocess.run([venv_python, "-c", TEST_ABI3], check=True)

    # if we're testing with non-freethreading pythonX.Y, try pythonX.Yt
    # otherwise, try pythonX.Y (presumably non-freethreading)
    other_executable = f"python{sys.version_info.major}.{sys.version_info.minor}"
    if not IS_FREETHREADING:
        other_executable += "t"
    # try other python only if it works and is different than ours
    other_result = subprocess.run(
        [
            other_executable,
            "-c",
            "import sysconfig; print(sysconfig.get_config_var('Py_GIL_DISABLED'))",
        ],
        capture_output=True,
    )
    if other_result.returncode != 0:
        return
    other_freethreading = other_result.stdout.strip() == b"1"
    if other_freethreading == IS_FREETHREADING:
        return

    subprocess.run([other_executable, "-m", "venv", tmp_path / "venv2"], check=True)
    venv2_python = tmp_path / "venv2/bin/python"
    with subtests.test(msg=f"wheel can be installed by {other_executable}"):
        with subxfail(True, reason="no build backend creates .abi3t wheels currently"):
            subprocess.run(
                [venv2_python, "-m", "pip", "install", "--force", dist_path], check=True
            )
