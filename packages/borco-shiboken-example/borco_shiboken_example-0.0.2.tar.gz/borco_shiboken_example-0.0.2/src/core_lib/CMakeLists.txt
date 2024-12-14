set(LIB_NAME core_lib)

qt_add_library(${LIB_NAME} STATIC
    # pure c++ classes
    macros.h
    icecream.h
    icecream.cpp
    truck.h
    truck.cpp
    dog.h
    dog.cpp
    # qt classes
    hellowidget.h
    hellowidget.cpp
)

target_include_directories(
    ${LIB_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(
    ${LIB_NAME} PUBLIC
    Qt6::Widgets
)

# FIXME: Is this needed?
set_property(TARGET ${LIB_NAME} PROPERTY PREFIX "")

# Needed mostly on Windows to export symbols, and create a .lib file, otherwise
# the binding library can't link to the sample library.
target_compile_definitions(${LIB_NAME} PRIVATE BINDINGS_BUILD)
