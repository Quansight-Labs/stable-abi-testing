# SPDX-FileCopyrightText: 2025 Michał Górny
# SPDX-License-Identifier: MIT

from build import ProjectBuilder
import pytest

from contextlib import contextmanager
from pathlib import Path
import os
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

if hasattr(limited, "__path__"):
    if hasattr(limited, "lib"):
        # limited.lib is present for CFFI. We had to create a Python wrapper package
        # because CFFI doesn't directly expose wrapped functions in the top-level
        # namespace of an extension module
        limited = limited._limited
    else:
        # if the build system created a package, import the actual extension
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
    dist_path = builder.build("wheel", tmp_path)
    path_name = Path(dist_path).name

    with subtests.test(msg="wheel has correct ABI tag"):
        if build_system in ("meson-python", "setuptools"):
            # The setuptools fork doesn't yet have support for forcing a GIL-enabled build
            # to produce an abi3.abi3t wheel
            if IS_FREETHREADING:
                assert "abi3.abi3t" in path_name
            else:
                assert "abi3" in path_name and "abi3t" not in path_name
        else:
            with subxfail(
                build_system in ("scikit-build-core",),
                reason="scikit-build-core does not build abi3.abi3t",
            ):
                assert "abi3.abi3t" in path_name

    subprocess.run([sys.executable, "-m", "venv", tmp_path / "venv"], check=True)
    python_exe = "python.exe" if os.name == "nt" else "python"
    venv_python = (
        tmp_path / sysconfig.get_path("scripts", vars={"base": "venv"}) / python_exe
    )
    subprocess.run(
        [sys.executable, "-m", "pip", "--python", venv_python, "install", dist_path],
        check=True,
    )

    with subtests.test(msg="extension works"):
        subprocess.run([venv_python, "-c", TEST_CALL], check=True)

    if IS_FREETHREADING:
        with subtests.test(msg="extension does not enable GIL"):
            subprocess.run([venv_python, "-Werror", "-c", "import limited"], check=True)

    # .abi3 suffix is not used on Windows
    if os.name != "nt":
        with subtests.test(msg="extension has .abi3 suffix"):
            with subxfail(
                IS_FREETHREADING and language == "nanobind",
                reason="nanobind does not support PEP 803 yet",
            ):
                subprocess.run([venv_python, "-c", TEST_ABI3], check=True)

    if "abi3t" not in path_name:
        return
    # if we're testing with non-freethreading pythonX.Y, try pythonX.Yt
    # otherwise, try pythonX.Y (presumably non-freethreading)
    other_executable = f"python{sys.version_info.major}.{sys.version_info.minor}"
    if not IS_FREETHREADING:
        other_executable += "t"
    # try other python only if it works and is different than ours
    try:
        other_result = subprocess.run(
            [
                other_executable,
                "-c",
                "import sysconfig; print(sysconfig.get_config_var('Py_GIL_DISABLED'))",
            ],
            capture_output=True,
        )
    except FileNotFoundError:
        return
    if other_result.returncode != 0:
        return
    other_freethreading = other_result.stdout.strip() == b"1"
    if other_freethreading == IS_FREETHREADING:
        return

    subprocess.run([other_executable, "-m", "venv", tmp_path / "venv2"], check=True)
    venv2_python = (
        tmp_path / sysconfig.get_path("scripts", vars={"base": "venv2"}) / python_exe
    )
    subprocess.run(
        [sys.executable, "-m", "pip", "--python", venv2_python, "install", dist_path],
        check=True,
    )

    with subtests.test(msg="extension works in other"):
        subprocess.run([venv2_python, "-c", TEST_CALL], check=True)

    if other_freethreading:
        with subtests.test(msg="extension does not enable GIL in other"):
            subprocess.run(
                [venv2_python, "-Werror", "-c", "import limited"], check=True
            )
