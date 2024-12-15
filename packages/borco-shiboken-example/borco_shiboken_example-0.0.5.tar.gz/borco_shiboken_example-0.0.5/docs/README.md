# shiboken example

Example creating a Python binding for Qt6 & C++ with
[shiboken](https://doc.qt.io/qtforpython-6/shiboken6/index.html). Based on the
[shiboken examples](https://doc.qt.io/qtforpython-6/shiboken6/examples/index.html).

## Usage

Add the bindings to another project using `uv`:

```terminal
$|success|uv add borco-shiboken-example
$|success|uv sync
...
info|+ borco-shiboken-example==0.0.4
info|+ shiboken6==6.8.1
...
```

Test the bindings were added and are usable (after activating the virtual environment created by `uv sync`):

```terminal
$|success|python
>>>|import borco_shiboken_example as x
>>>|dog = x.Dog()
>>>|dog.name = "Max"
>>>|dog.bark()
info|Max: woof!
>>>|
```
