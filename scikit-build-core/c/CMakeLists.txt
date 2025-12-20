cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C VERSION ${SKBUILD_PROJECT_VERSION})

find_package(Python COMPONENTS Interpreter Development.SABIModule REQUIRED)

Python_add_library(
  limited
  MODULE
  WITH_SOABI
  USE_SABI 3.15
  limited.c
)
target_compile_definitions(limited PRIVATE -D_Py_OPAQUE_PYOBJECT)
install(TARGETS limited DESTINATION ${SKBUILD_PLATLIB_DIR})
