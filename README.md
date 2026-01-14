Python Stable ABI Testing
=========================

This repository contains example packages for testing the new limited
API proposals, along with a test suite.  Currently, it uses the
[reference
implementation](https://github.com/python/cpython/pull/136505) of [PEP
803](https://peps.python.org/pep-0803/) found in CPython 3.15.0a2.


Implementation notes
--------------------
This is a work-in-progress, based on the state as of 2026-01-10.
Whenever possible, official or semi-official support is used.
Elsewhere, hacks are employed, or the packages are as close to the new
API as currently possible.

- In packages using the C API, the new limited API is enabled via
  setting `-D_Py_OPAQUE_PYOBJECT` as required by Python 3.15.0a2.
  According to PEP 803, the final implementation should not require
  this.  This is also done on packages that have explicit switches for
  limited API, since these do not account for PEP 803.
- A minimal [fork of
  meson-python](https://github.com/mgorny/meson-python/tree/freethreading-limited-api)
  is used, in order to remove the explicit check that blocks disabling
  GIL while using limited API.
- [A preview freethreading-limited-api branch of
  Cython](https://github.com/cython/cython/tree/freethreading-limited-api-preview)
  is used.
- PyO3 does not support PEP 793, PEP 803 or Python 3.15 yet.  The test
  currently builds a limited API extension targeting Python 3.14.
  [PyO3#5610](https://github.com/PyO3/pyo3/issues/5610).
- nanobind does not support PEP 793 yet.  The test package uses regular
  limited API or freethreading API currently.
  [nanobind#1187](https://github.com/wjakob/nanobind/discussions/1187).
- None of the build systems implement the new wheel tags found in PEP
  803.  As such, tests are not currently looking at wheel tags.
