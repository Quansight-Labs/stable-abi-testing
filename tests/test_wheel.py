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

TOP_DIR = Path(__file__).parent.parent
TEST_CASES = [
    "meson-python/c",
    pytest.param("meson-python/cython", marks=[XFAIL_CYTHON]),
    "scikit-build-core/c",
    pytest.param("scikit-build-core/cython", marks=[XFAIL_CYTHON]),
    "setuptools/c",
    pytest.param("setuptools/cython", marks=[XFAIL_CYTHON]),
]


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_install(test_case: str, tmp_path: Path, venv) -> None:
    builder = ProjectBuilder(TOP_DIR / test_case)
    dist_path = builder.build("wheel", tmp_path)
    venv.pip("install", dist_path)
    # -Werror to catch the exception when extension is not freethreading-compatible
    venv.python("-Werror", "-c", "import limited; assert limited.add(1, 2) == 3")
