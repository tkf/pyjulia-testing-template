Tested testing template for pyjulia-based projects
==================================================

This template tries to solve the following problem:

* Setting up test suite/CI for pyjulia-based project is hard.
* Initializing pyjulia is slow.
* Using pyjulia with different Python interpreter requires manual
  rebuild.
* There are some common errors related to shared library loading.


Writing tests
-------------

This template uses pytest fixture for setting up pyjulia's
`julia.Julia` instance.  For the tests requiring pyjulia setup, use
`julia` fixture (defined in `./conftest.py`).  Example:

.. code:: python

  def test_julia(julia):
      assert julia.eval('1 + 1') == 2

Note that `julia` fixture has to be specified when your code
(internally) calls `julia.Julia` directly since the configuration in
this template recognizes the dependency on pyjulia by the use of the
`julia` fixture.

The tests using `julia` fixtures would be skipped unless
`TEST_PYJULIA` environment variable is set to `yes` (see below).  This
way, you can mix tests depending or not depending on pyjulia in your
test suite but can quickly run the tests without pyjulia dependency.


Running tests
-------------

This template provides a few modes for running tests::

  make test-{tox,notox} [TEST_PYJULIA=yes] [PYTEST_OPTS=...]

Pure Python unit tests
^^^^^^^^^^^^^^^^^^^^^^

To run tests without pyjulia (running pure-Python unit tests) run::

  tox
  make test-tox  # equivalent

This is a usual `tox`-based test execution but skips the tests
requiring pyjuila.

Testing Python-Julia integration in `tox`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run tests with pyjuila, set environment variable `TEST_PYJUILA` to
`yes` before running them.  Use::

  TEST_PYJULIA=yes tox
  make test-tox TEST_PYJULIA=yes  # (more-or-less) equivalent

Faster way to test Python-Julia integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run tests with pyjulia without `Pkg.build("PyCall")` overhead,
use::

  make test-notox TEST_PYJULIA=yes