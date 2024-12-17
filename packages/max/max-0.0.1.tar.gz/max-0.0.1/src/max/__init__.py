ABOUT = """
Modular MAX (Placeholder Package)
-------------------

This package is a temporary placeholder for future releases of the 
Modular MAX SDK on PyPI which is currently only available as a 
conda package.

Learn more about MAX at: https://www.modular.com/max
"""

__app_name__ = "max"
__version__ = "0.0.1"


if __name__ == "__main__":
    print(ABOUT)
else:
    raise ImportError(ABOUT)