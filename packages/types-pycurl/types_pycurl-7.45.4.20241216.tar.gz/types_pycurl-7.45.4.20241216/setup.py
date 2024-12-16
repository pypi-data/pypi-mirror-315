from setuptools import setup

name = "types-pycurl"
description = "Typing stubs for pycurl"
long_description = '''
## Typing stubs for pycurl

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pycurl`](https://github.com/pycurl/pycurl) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `pycurl`. This version of
`types-pycurl` aims to provide accurate annotations for
`pycurl==7.45.4`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/pycurl`](https://github.com/python/typeshed/tree/main/stubs/pycurl)
directory.

This package was tested with
mypy 1.13.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`7cae61f61a042a772010274dd1d8f1ee4454e5a4`](https://github.com/python/typeshed/commit/7cae61f61a042a772010274dd1d8f1ee4454e5a4).
'''.lstrip()

setup(name=name,
      version="7.45.4.20241216",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pycurl.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pycurl-stubs'],
      package_data={'pycurl-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
