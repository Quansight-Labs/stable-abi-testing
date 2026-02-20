from setuptools import setup, find_packages, Extension

setup(
    packages = find_packages(
        where="src",
        include = ["limited*"],
    ),
    ext_modules = [Extension(
        name = "limited",
        sources = ["src/limited/limited.c"],
        py_limited_api = True,
        extra_compile_args = [
            "-D_Py_OPAQUE_PYOBJECT",
            "-DPy_LIMITED_API=0x030f0000",
        ],
    ),],
)
