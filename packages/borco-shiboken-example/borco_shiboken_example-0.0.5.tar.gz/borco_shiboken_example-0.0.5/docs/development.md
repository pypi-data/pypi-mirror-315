# Development overview

## Code organization

Folder | Purpose
---|---
`src/core_lib` | C++ code for the `core_lib` static lib with main functionality
`src/bindings_lib` | C++ code for the `shiboken` bindings
`samples/c++` | C++ samples
`samples/python` | Python samples
`tests/cpp/catch` | C++ tests using [catch2](https://github.com/catchorg/Catch2)
`tests/cpp/google` | C++  tests using [google test & google mock](https://github.com/google/googletest)
`tests/python` | Python tests

## Requirements

To build the `shiboken` bindings manually, we use:

* C++ compiler (that supports C20 or newer C++ standard)
* Qt 6.8+ headers and libs
* `libclang` (precompiled versions can be downloaded from [here](https://download.qt.io/development_releases/prebuilt/libclang/))
* `cmake` 3.29+
* `ninja`
* Python with development headers
* `uv` to configure and manage a local `.venv` virtual environment

## Environment

* the compiler, `cmake` and `ninja` should be on the path
* `cmake` should be able to find the Qt headers and libs
* the `libclang` location should be exported as `CLANG_INSTALL_DIR`
