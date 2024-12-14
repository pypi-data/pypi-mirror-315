# Windows

## Visual Studio 2022

Install *Visual Studio 2022* with:

* C++ compiler (check **Workload &rarr; Desktop development with C++**)
* `cmake` and `ninja` (check **Installation Details &rarr; Desktop development with C++ &rarr; C++ CMake tools for Windows**)

You will have to load the `vcvarsall.bat` before being able to run the `cmake`
or `ninja` installed by *Visual Studio 2022*.

Example (for `powershell`):

```powershell
& "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
```

## Qt6

Install *Qt6* with:

* Qt6 for *MSVC 2022 64-bit* (for example: **Qt &rarr; Qt 6.X.Y &rarr; MSVC 2022 64-bit**)
* (optional) if you plan to debug the code, install *Qt Debug Information Files*
  (**Qt &rarr; Qt 6.X.Y &rarr; Qt Debug Information Files**)
* (optional) if you want to use *Qt Creator* for development:
  * **Qt Creator &rarr; Qt Creator X.Y.Z**
  * **CDB Debugger Support**
  * **Debugging Tools for Windows**

Example (for `powershell`):

```powershell
& "C:\Qt\6.8.1\msvc2022_64\bin\qtenv2.bat"
```

### CMake and Ninja from Qt

You only need to install `cmake` and `ninja` from *Qt* installer if you plan to build with
*MinGW*. Python bindings should be built with *MSVC*, so they are not required by this
project.

## Environment

### Manually

To manually configure the environment, run these commands in a `cmd` terminal:

```batch
rem setup VS2022
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64

rem save current path
pushd .

rem setup Qt
"C:\Qt\6.8.1\msvc2022_64\bin\qtenv2.bat"

rem restore path
popd

rem setup libclang
set CLANG_INSTALL_DIR="C:\libclang\libclang-release_19.1.0"
```

### VSCode

If you use *VSCode*, the workspace is configured to use the `Git Bash (Custom)`
custom terminal profile that automatically:

* loads `vcvarsall.bat` to configure *Visual Studio* C++ toolchain
* loads `qtenv2.bat` to configure *Qt6*
* launches *git bash*

The profile name, the locations of `vcvarsall.bat` and `qtenv2.bat`, along with
other variables are defined in `.vscode/settings.json`.

When creating the terminal, *VSCode* executes `.vscode/git_bash_custom.bat`,
passing it the `env` defined in `.vscode/settings.json`.
