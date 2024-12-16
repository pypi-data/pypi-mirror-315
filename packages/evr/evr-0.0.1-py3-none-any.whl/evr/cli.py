"""Command line interface for :mod:`evr`.

Why does this file exist, and why not put this in ``__main__``?
You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m evr`` python will
  execute``__main__.py`` as a script. That means there won't be any
  ``evr.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``evr.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

from evr.api import main

__all__ = [
    "main",
]

if __name__ == "__main__":
    main()
