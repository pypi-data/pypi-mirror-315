"""Example package using `shiboken6` to create Python bindings for C++ classes.
"""

# by importing shiboken6 here, we remove the need to deploy the shiboken6
# runtime files within the package itself
import shiboken6

# import the C++ classes wrapped by the binding
from .borco_shiboken_example import (
    Dog,
    Truck,
    Icecream,
)

# make the C++ classes wrapped by binding available directly from the python
# package
__all__ = [
    "Dog",
    "Truck",
    "Icecream",
]
