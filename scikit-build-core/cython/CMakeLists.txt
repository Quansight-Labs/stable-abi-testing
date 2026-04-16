cmake_minimum_required(VERSION 3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C VERSION ${SKBUILD_PROJECT_VERSION})

find_package(Python COMPONENTS Interpreter Development.SABIModule REQUIRED)
include(UseCython)

cython_transpile(limited.pyx LANGUAGE C OUTPUT_VARIABLE limited_c)

Python_add_library(
  limited
  MODULE
  WITH_SOABI
  USE_SABI 3.15
  ${limited_c}
)
target_compile_definitions(limited PRIVATE -DPy_TARGET_ABI3T=0x030f0000)
install(TARGETS limited DESTINATION ${SKBUILD_PLATLIB_DIR})
