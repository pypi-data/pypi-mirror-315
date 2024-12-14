# ----------------------------------------------------------------------------
# Force release build
# ----------------------------------------------------------------------------
set(CMAKE_BUILD_TYPE "Release" CACHE STRING "" FORCE)


# ----------------------------------------------------------------------------
# Define some custom macros for working with shiboken
# ----------------------------------------------------------------------------
include(${CMAKE_CURRENT_LIST_DIR}/shiboken_macros.cmake)


# ----------------------------------------------------------------------------
# Shiboken detection
# ----------------------------------------------------------------------------

# Query for the shiboken generator path, Python path, include paths and linker flags.
pyside_config(--shiboken-module-path SHIBOKEN_MODULE_PATH)
pyside_config(--shiboken-generator-path SHIBOKEN_GENERATOR_PATH)
pyside_config(--python-include-path SHIBOKEN_PYTHON_INCLUDE_DIR)
pyside_config(--shiboken-generator-include-path SHIBOKEN_INCLUDE_DIR 1)
pyside_config(--shiboken-module-shared-libraries-cmake SHIBOKEN_SHARED_LIBRARIES 0)
pyside_config(--python-link-flags-cmake SHIBOKEN_PYTHON_LINKING_DATA 0)

set(SHIBOKEN_PATH "${SHIBOKEN_GENERATOR_PATH}/shiboken6${CMAKE_EXECUTABLE_SUFFIX}")

if(NOT EXISTS ${SHIBOKEN_PATH})
    message(FATAL_ERROR "Shiboken executable not found at path: ${SHIBOKEN_PATH}")
endif()

message(STATUS "SHIBOKEN_PATH: ${SHIBOKEN_PATH}")


# ----------------------------------------------------------------------------
# RPATH configuration
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# !!! (The section below is deployment related, so in a real world application
# you will want to take care of this properly with some custom script or tool).
# ----------------------------------------------------------------------------
# Enable rpaths so that the built shared libraries find their dependencies.
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH ${SHIBOKEN_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
# ----------------------------------------------------------------------------
# !!! End of dubious section.
# ----------------------------------------------------------------------------
