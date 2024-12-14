# shiboken

Building Python bindings with shiboken.

## Requirements

* Python: 3.7+
* Qt: 6.0+
* libclang: version 10 for 6.0+ (see bellow for more)
* CMake: 3.1+

### libclang

Prebuilt `libclang` versions can be found
[here](https://download.qt.io/development_releases/prebuilt/libclang/).

You will need version **10 or newer** to use `shiboken` with Qt 6.0+.

For example, to use `libclang` version 19 on *Windows*:

* create a folder for `libclang` in `C:\libclang`
* download the archived `libclang` in it
* extract the archive
* rename it to `libclang-release_19.1.0`

The `libclang` path is exported to the environment through the
`CLANG_INSTALL_DIR` variable.

This allows us to easily switch between `libclang` versions, if needed.

When using `Git + Bash (Custom)` terminal profile in *VSCode* the location of
the `libclang` is configured in `.vscode\settings.json`:

```javascript
{
    "terminal.integrated.defaultProfile.windows": "Git Bash (Custom)",
    "terminal.integrated.profiles.windows": {
        "Git Bash (Custom)": {
            ...
            "env": {
                ...
                "CLANG_INSTALL_DIR": "C:\\libclang\\libclang-release_19.1.0",
                ...
            }
        }
    },
```

Alternatively, set it on the command line:

```powershell
$env:CLANG_INSTALL_DIR = "C:\libclang\libclang-release_19.1.0";
```

```bash
export CLANG_INSTALL_DIR="C:\libclang\libclang-release_19.1.0";
```

## Add dependencies

```bash
uv add --dev pyside6 shiboken shiboken6_generator
```
