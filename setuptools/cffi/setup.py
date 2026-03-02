# CFFI doesn't support declarative setup for this
# see https://github.com/python-cffi/cffi/issues/55
from setuptools import setup

setup(
    cffi_modules=["src/limited/gen_limited.py:ffibuilder"],
)
