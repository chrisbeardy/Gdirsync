# Contributing to Gdirsync

Please follow these guidelines for contributing. Pull requests are welcome.

## Basic requirements

- Create a new [github issue](https://github.com/chrisbeardy/Gdirsync/issues) for bugs
  or features. Search the ticket system first, to avoid filing a duplicate.
- Ensure code follows the [syntax and conventions](#Syntax-and-conventions).
- Code must pass tests. See [Testing](#Testing) for information on how to run and
 write unit tests.
- Commit messages should be informative.

## Pull request process:

- Fork us on [github](https://github.com/chrisbeardy/Gdirsync).
- Clone your repository.
- Create a feature branch for your issue.
- Apply your changes:
  - Add them, and then commit them to your branch.
  - Run the tests until they pass.
  - When you feel you are finished, rebase your commits to ensure a simple
    and informative commit log.
- Create a pull request on github from your forked repository.

## Syntax and conventions

### Code formatting tools

Use [Black](https://github.com/psf/black) for formatting Python code.
Simply run `black <filename>` from the command line.

### Docstrings

Please use the [Python domain info field lists](https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html?highlight=%3Areturn%3A#info-field-lists)
for all docstrings. This way documentation can be auto-generated from docstrings.

example:

    def func(foo, bar):
       """Function purpose.

        :param int foo: description and type of the foo argument
        :param bar: description of the bar argument 
        :type bar: int

        :return: return description
        :rtype: int
       """
       return foo * bar
    
## Testing

The tests are located `tests` folder. Tests should be included for any new contributions.

### Tox

All the tests for pyads can be run using [tox](https://pypi.python.org/pypi/tox).
Simply use `pip install tox` and run `tox` from the root directory. See `tox.ini`
for available environments.

### unittest

Tests are written using [unittest](https://docs.python.org/3/library/unittest.html)
and can be individually run for each environment with the python built in library.

### Travis-CI

When creating a pull request (PR) on [Github], [Travis] will automatically run
the unit tests with the code in the PR and report back.

[Github]: https://github.com/chrisbeardy/Gdirsync/pulls
[Travis]: https://travis-ci.org/chrisbeardy/Gdirsync

## Documentation contributions

Sphinx is used to create the documentation from source files and docstrings in code.
You can build your documentation changes for testing using:

    pip install -r requirements.txt
    cd docs
    make html

The resulting html files are in `doc/build/html`.

Documentation is found on [read the docs](https://Gdirsync.readthedocs.io/en/latest/)
and will automatically update when PRs are merged.
