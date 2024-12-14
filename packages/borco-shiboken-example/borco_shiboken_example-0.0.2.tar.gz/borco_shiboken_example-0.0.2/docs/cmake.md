# CMake

This project requires:

* C++
* cmake
* ninja
* Python (can be installed with `uv`)
* Qt6

## Presets

### venv

This preset uses the *Python* version installed in `.venv` with:

```bash
uv sync
```

#### Workflow

```bash
cmake --workflow --preset venv
```

#### Configure

```bash
cmake --preset venv
```

#### Build

```bash
cmake --preset venv --build
```

#### Testings

Run **C++ tests**:

```bash
ctest --preset venv
```

#### Build artifacts

##### location

The build artifacts are stored under `build/venv`.

##### remove

```bash
rm -rf build/venv
```
