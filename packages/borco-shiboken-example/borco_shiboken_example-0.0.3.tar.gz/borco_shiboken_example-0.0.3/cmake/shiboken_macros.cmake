# ----------------------------------------------------------------------------
# Macro to get various pyside / python include / link flags and paths.
# Uses the not entirely supported pyside_config.py file.
# ----------------------------------------------------------------------------
macro(pyside_config _PYSIDE_CONFIG_OPTION _OUTPUT_VAR)
    if(${ARGC} GREATER 2)
        set(is_list ${ARGV2})
    else()
        set(is_list "")
    endif()

    # use python from the virtual environment
    execute_process(
        COMMAND python ${CMAKE_CURRENT_LIST_DIR}/pyside_config.py ${_PYSIDE_CONFIG_OPTION}
        OUTPUT_VARIABLE ${_OUTPUT_VAR}
        OUTPUT_STRIP_TRAILING_WHITESPACE)

    if("${${_OUTPUT_VAR}}" STREQUAL "")
        message(FATAL_ERROR "Error: Calling \"python ${CMAKE_CURRENT_LIST_DIR}/pyside_config.py ${_PYSIDE_CONFIG_OPTION}\" returned no output.")
    endif()

    if(is_list)
        string(REPLACE " " ";" ${_OUTPUT_VAR} "${${_OUTPUT_VAR}}")
    endif()
endmacro()

# ----------------------------------------------------------------------------
# configure bindings cmake target
# ----------------------------------------------------------------------------
macro(shiboken_add_library _BINDINGS_LIB_NAME _WRAPPED_LIB_NAME _GENERATED_SOURCES)
    message(STATUS "┌─── shiboken_add_library")
    message(STATUS "│ _WRAPPED_LIB_NAME: ${_WRAPPED_LIB_NAME}")
    message(STATUS "│ _BINDINGS_LIB_NAME: ${_BINDINGS_LIB_NAME}")
    message(STATUS "│ _GENERATED_SOURCES: ${_GENERATED_SOURCES}")

    # Set the cpp files which will be used for the bindings library.
    set(${_BINDINGS_LIB_NAME}_sources ${_GENERATED_SOURCES})

    # Define and build the bindings library.
    add_library(${_BINDINGS_LIB_NAME} MODULE ${${_BINDINGS_LIB_NAME}_sources})

    # Apply relevant include and link flags.
    target_include_directories(${_BINDINGS_LIB_NAME} PRIVATE ${SHIBOKEN_PYTHON_INCLUDE_DIR})
    target_include_directories(${_BINDINGS_LIB_NAME} PRIVATE ${SHIBOKEN_INCLUDE_DIR})
    target_include_directories(${_BINDINGS_LIB_NAME} PRIVATE ${CMAKE_SOURCE_DIR})

    target_link_libraries(${_BINDINGS_LIB_NAME} PRIVATE ${SHIBOKEN_SHARED_LIBRARIES})
    target_link_libraries(${_BINDINGS_LIB_NAME} PRIVATE ${_WRAPPED_LIB_NAME})

    # Adjust the name of generated module.
    set_property(TARGET ${_BINDINGS_LIB_NAME} PROPERTY PREFIX "")
    set_property(TARGET ${_BINDINGS_LIB_NAME} PROPERTY OUTPUT_NAME
        "${BINDINGS_LIB_NAME}${PYTHON_EXTENSION_SUFFIX}")

    if(WIN32)
        if("${CMAKE_BUILD_TYPE}" STREQUAL "Debug")
            set_property(TARGET ${_BINDINGS_LIB_NAME} PROPERTY SUFFIX "_d.pyd")
        else()
            set_property(TARGET ${_BINDINGS_LIB_NAME} PROPERTY SUFFIX ".pyd")
        endif()
    endif()

    # Make sure the linker doesn't complain about not finding Python symbols on macOS.
    if(APPLE)
        set_target_properties(${_BINDINGS_LIB_NAME} PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
    endif(APPLE)

    # Find and link to the python import library only on Windows.
    # On Linux and macOS, the undefined symbols will get resolved by the dynamic linker
    # (the symbols will be picked up in the Python executable).
    if(WIN32)
        list(GET SHIBOKEN_PYTHON_LINKING_DATA 0 __SHIBOKEN_PYTHON_LIBDIR)
        list(GET SHIBOKEN_PYTHON_LINKING_DATA 1 __SHIBOKEN_PYTHON_LIB)
        find_library(SHIBOKEN_PYTHON_LINK_FLAGS
            ${__SHIBOKEN_PYTHON_LIB}
            PATHS ${__SHIBOKEN_PYTHON_LIBDIR}
            HINTS ${__SHIBOKEN_PYTHON_LIBDIR})
        message(STATUS "│ SHIBOKEN_PYTHON_LINK_FLAGS: ${SHIBOKEN_PYTHON_LINK_FLAGS}")
        target_link_libraries(${_BINDINGS_LIB_NAME} PRIVATE ${SHIBOKEN_PYTHON_LINK_FLAGS})
    endif()

    message(STATUS "└─── shiboken_add_library")
endmacro()

# ----------------------------------------------------------------------------
# Dubious deployment macro
# ----------------------------------------------------------------------------
macro(shiboken_deploy_library _BINDINGS_LIB_NAME _WRAPPED_LIB_NAME)
    message(STATUS "┌─── shiboken_deploy_library")
    set(__WINDOWS_SHIBOKEN_SHARED_LIBRARIES)

    if(WIN32)
        # --------------------------------------------------------------------
        # !!! (The section below is deployment related, so in a real world
        # application you will want to take care of this properly (this is
        # simply to eliminate errors that users usually encounter)).
        # --------------------------------------------------------------------
        # Circumvent some "#pragma comment(lib)"s in "include/pyconfig.h"
        # which might force to link against a wrong python shared library.
        set(__PYTHON_VERSIONS_LIST 3 36 37 38 39 310 311 312 313)
        set(__PYTHON_ADDITIONAL_LINK_FLAGS "")

        foreach(__VER ${__PYTHON_VERSIONS_LIST})
            set(__PYTHON_ADDITIONAL_LINK_FLAGS
                "${__PYTHON_ADDITIONAL_LINK_FLAGS} /NODEFAULTLIB:\"python${__VER}_d.lib\"")
            set(__PYTHON_ADDITIONAL_LINK_FLAGS
                "${__PYTHON_ADDITIONAL_LINK_FLAGS} /NODEFAULTLIB:\"python${__VER}.lib\"")
        endforeach()

        message(STATUS "│ __PYTHON_ADDITIONAL_LINK_FLAGS: ${__PYTHON_ADDITIONAL_LINK_FLAGS}")

        set_target_properties(${_BINDINGS_LIB_NAME}
            PROPERTIES LINK_FLAGS "${__PYTHON_ADDITIONAL_LINK_FLAGS}")

        # Compile a list of shiboken shared libraries to be installed, so that
        # the user doesn't have to set the PATH manually to point to the
        # PySide6 package.
        foreach(__LIBRARY_PATH ${SHIBOKEN_SHARED_LIBRARIES})
            string(REGEX REPLACE ".lib$" ".dll" __LIBRARY_PATH ${__LIBRARY_PATH})
            file(TO_CMAKE_PATH ${__LIBRARY_PATH} __LIBRARY_PATH)
            list(APPEND __WINDOWS_SHIBOKEN_SHARED_LIBRARIES "${__LIBRARY_PATH}")
        endforeach()

        message(STATUS "│ __WINDOWS_SHIBOKEN_SHARED_LIBRARIES: ${__WINDOWS_SHIBOKEN_SHARED_LIBRARIES}")

        # --------------------------------------------------------------------
        # !!! End of dubious section.
        # --------------------------------------------------------------------
    endif()

    # ------------------------------------------------------------------------
    # !!! (The section below is deployment related, so in a real world
    # application you will want to take care of this properly with some custom
    # script or tool).
    # ------------------------------------------------------------------------
    # Install the library and the bindings module into the
    # "${CMAKE_INSTALL_PREFIX}/bindings/${_BINDINGS_LIB_NAME}" folder.

    set(__SHIBOKEN_SHARED_LIBS_DESTINATION ${BINDINGS_INSTALL_DIR}/${_BINDINGS_LIB_NAME})
    message(STATUS "│ __SHIBOKEN_SHARED_LIBS_DESTINATION: ${__SHIBOKEN_SHARED_LIBS_DESTINATION}")

    install(TARGETS ${_BINDINGS_LIB_NAME} ${WRAPPED_LIB_NAME}
        DESTINATION "${__SHIBOKEN_SHARED_LIBS_DESTINATION}")

    install(FILES ${__WINDOWS_SHIBOKEN_SHARED_LIBRARIES}
        DESTINATION "${__SHIBOKEN_SHARED_LIBS_DESTINATION}")

    # ----------------------------------------------------------------------------
    # !!! End of dubious section.
    # ----------------------------------------------------------------------------
    message(STATUS "└─── shiboken_deploy_library")
endmacro()
