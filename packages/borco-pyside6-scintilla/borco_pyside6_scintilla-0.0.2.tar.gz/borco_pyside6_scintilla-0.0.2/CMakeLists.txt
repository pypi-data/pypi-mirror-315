cmake_minimum_required(VERSION 3.29)

# ----------------
# CMake policies
# ----------------
cmake_policy(VERSION 3.29)

# Enable policy to not use RPATH settings for install_name on macOS.
if(POLICY CMP0068)
  cmake_policy(SET CMP0068 NEW)
endif()


# --------------------
# Project definition
# --------------------
if(NOT SKBUILD)
    message(STATUS "Running CMake directly.")
    set(PROJECT_NAME borco_shiboken_example)
else()
    message(STATUS "Running from 'scikit-build-core'.")
    message(PROJECT_NAME ${SKBUILD_PROJECT_NAME})
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)
