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
    set(SKBUILD_PROJECT_NAME borco_shiboken_example)
else()
    message(STATUS "Running from 'scikit-build-core'.")
endif()

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)


# --------------
# C++ features
# --------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


# ---------
# Options
# ---------
set(BINDINGS_INSTALL_DIR "." CACHE STRING "Folder where to install built bindings.")

include(CMakeDependentOption)

cmake_dependent_option(
    _CPP_DEV_MODE "Enable C++ developer mode." ON "NOT DEFINED SKBUILD" OFF
)

cmake_dependent_option(
    WITH_TESTS "Build tests." ON "_CPP_DEV_MODE" OFF
)

# Catch2: https://github.com/catchorg/Catch2
cmake_dependent_option(
    WITH_CATCH2 "Enable Catch2 tests." ON "WITH_TESTS" OFF
)

# Google Test: https://google.github.io/googletest/
cmake_dependent_option(
    WITH_GTEST "Enable Google Test/Google Mock tests." ON "WITH_TESTS" OFF
)

# C++ Sample apps
cmake_dependent_option(
    WITH_SAMPLES "Enable C++ samples." ON "_CPP_DEV_MODE" OFF
)


# ------------------
# Qt configuration
# ------------------
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
qt6_standard_project_setup()


# --------------------------------------------------------------------
# FetchContent is required to install software from remote git repos
# --------------------------------------------------------------------
include(FetchContent)


# -----------
# c++ tests
# -----------
if(${WITH_TESTS})
    include(CTest)

    if(${WITH_CATCH2})
        FetchContent_Declare(
            Catch2
            GIT_REPOSITORY https://github.com/catchorg/Catch2.git
            GIT_TAG v3.7.1 # or a later release
        )
        FetchContent_MakeAvailable(Catch2)

        # dirs with c++ tests
        add_subdirectory(tests/cpp/catch)
    endif()

    if(${WITH_GTEST})
        FetchContent_Declare(
            GoogleTest
            GIT_REPOSITORY https://github.com/google/googletest
            GIT_TAG v1.15.2
        )
        # For Windows: Prevent overriding the parent project's compiler/linker settings
        set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
        FetchContent_MakeAvailable(GoogleTest)

        # dirs with c++ tests
        add_subdirectory(tests/cpp/google)
    endif()
endif()


# ------------------
# Check for Python
# ------------------
set (Python_FIND_VIRTUALENV ONLY)
find_package(Python 3
    REQUIRED COMPONENTS Interpreter Development.Module
    OPTIONAL_COMPONENTS Development.SABIModule
)


# ----------------------------------
# Add subdirectories with C++ code
# ----------------------------------
add_subdirectory(src/core_lib)

if(${WITH_SAMPLES})
    add_subdirectory(samples/cpp/hello_widget_sample)
endif()

# ----------
# Shiboken
# ----------
include(cmake/shiboken.cmake)

add_subdirectory(src/bindings_lib)
