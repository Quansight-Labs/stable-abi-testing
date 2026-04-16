Python Stable ABI Testing
=========================

This repository contains example packages for testing the new limited
API proposals, along with a test suite.  Currently, it uses the
[reference
implementation](https://github.com/python/cpython/pull/136505) of [PEP
803](https://peps.python.org/pep-0803/) found in CPython 3.15.0a2.


Implementation notes
--------------------
This is a work-in-progress, based on the state as of 2026-03-05.
Whenever possible, official or semi-official support is used.
Elsewhere, hacks are employed, or the packages are as close to the new
API as currently possible.

- In packages using the C API, the new limited API is enabled via
  setting `-DPy_TARGET_ABI3T=0x30f0000` as described in PEP 803.
  This is also done on some packages that have explicit switches for
  limited API, since these do not account for PEP 803.
- A minimal [fork of
  meson-python](https://github.com/mgorny/meson-python/tree/freethreading-limited-api)
  is used, in order to remove the explicit check that blocks disabling
  GIL while using limited API.
- [A preview freethreading-limited-api branch of
  Cython](https://github.com/cython/cython/tree/freethreading-limited-api-preview)
  is used.
- Forks of [PyO3](https://github.com/PyO3/pyo3/pull/5807) and
  [maturin](https://github.com/PyO3/maturin/pull/3113) are used that add
  preliminary PEP 803 support.
- nanobind has preliminary support for PEP 793 and PEP 803 in the [`abi3t`
  branch](https://github.com/wjakob/nanobind/compare/master...abi3t).  The test
  package uses regular limited API or freethreading API currently.
  [nanobind#1187](https://github.com/wjakob/nanobind/discussions/1187)
  [nanobind#1284](https://github.com/wjakob/nanobind/discussions/1284)
  .
- A minimal [fork of CFFI](https://github.com/python-cffi/cffi/pull/232) is
  used, to bypass code paths that do not allow limited API builds on the
  free-threaded build.
- A minimal [fork of setuptools](https://github.com/pypa/setuptools/pull/5193)
  is used, to add support for the `abi3t` ABI tag and `abi3.abi3t` compressed
  tag set.
