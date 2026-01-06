cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX VERSION ${SKBUILD_PROJECT_VERSION})

find_package(Python COMPONENTS Interpreter Development Development.SABIModule REQUIRED)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT
)
find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(limited
  FREE_THREADED
  STABLE_ABI
  limited.cxx)
# TODO: nanobind does not implement PEP 793 / PEP 803 yet
# https://github.com/wjakob/nanobind/discussions/1187
#target_compile_definitions(limited PRIVATE -D_Py_OPAQUE_PYOBJECT)
install(TARGETS limited DESTINATION ${SKBUILD_PLATLIB_DIR})
