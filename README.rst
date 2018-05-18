Tested testing template for pyjulia-based projects
==================================================

This template tries to solve the following problem:

* Setting up test suite/CI for pyjulia_-based project is hard.
* Initializing pyjulia is slow.
* Using pyjulia with different Python interpreter requires manual
  rebuild.
* There are some common errors related to shared library loading.

This template includes setup for the following continuous integration
services:

* |travis-status| Travis CI (Linux and macOS)
* |appveyor-status| AppVeyor
* |gitlab-status| GitLab CI


Writing tests
-------------

This template uses pytest fixture for setting up pyjulia's
`julia.Julia` instance.  For the tests requiring pyjulia setup, use
`julia` fixture (defined in `conftest.py`_).  Example:

.. code:: python

  def test_julia(julia):
      assert julia.eval('1 + 1') == 2

Note that `julia` fixture has to be specified when your code calls
`julia.Julia` directly since the configuration in this template
recognizes the dependency on pyjulia by the use of the `julia`
fixture.

The tests using `julia` fixtures would be skipped unless
`TEST_PYJULIA` environment variable is set to `yes` (see below).  This
way, you can mix tests depending or not depending on pyjulia in your
test suite but can quickly run the tests without pyjulia dependency.


Running tests
-------------

This template provides three modes for running tests::

  make test-tox                     # tests without Julia and multiple Python interpreters/environments
  make test-tox TEST_PYJULIA=yes    # tests with Julia with and multiple Python interpreters/environments
  make test-notox TEST_PYJULIA=yes  # tests with Julia and default Python


Pure Python unit tests
^^^^^^^^^^^^^^^^^^^^^^

To run tests *without* pyjulia (running pure-Python unit tests) use::

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

Note that ``make test-tox`` sets up `SSL_CERT_FILE` in addition to the
`tox` version.  This may be useful when you have "error initializing
LibGit2 module" (see also: `JuliaLang/julia#18693`_,
`JuliaDiffEq/diffeqpy#13`_)

Behind the scene (in `conftest.py`_), it **builds** `PyCall.jl`_
(i.e., runs ``Pkg.build("PyCall")``) against Python interpreter in tox
environment and then **re-builds** `PyCall.jl`_ to *try* to re-create
whatever the original configuration was.

This is rather insane.  One way to solve it is to setup a Julia
environment per tox environment as in what diffeqpy is doing (see
`diffeqpy/tox.ini`_).  However, this consumes rather large amount of
disk space (~ 1 GB).

.. _`JuliaLang/julia#18693`: https://github.com/JuliaLang/julia/issues/18693
.. _`JuliaDiffEq/diffeqpy#13`: https://github.com/JuliaDiffEq/diffeqpy/pull/13/commits/850441ee63962a2417de2bce6f6223052ee9cceb
.. _`diffeqpy/tox.ini`: https://github.com/JuliaDiffEq/diffeqpy/blob/v0.3.0/tox.ini#L12


Faster way to test Python-Julia integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run tests with pyjulia without ``Pkg.build("PyCall")`` overhead,
use::

  make test-notox TEST_PYJULIA=yes

Note that this invokes pytest using the Python interpreter you setup
for `PyCall.jl`_.  It thus requires all Python dependencies including
pyjulia and pytest to be installed for this Python
interpreter/environment.

.. --- Links ---

.. _`conftest.py`: src/pyjulia_testing_template/conftest.py
.. _pyjulia: https://github.com/JuliaPy/pyjulia
.. _`PyCall.jl`: https://github.com/JuliaPy/PyCall.jl

.. |travis-status|
   image:: https://secure.travis-ci.org/tkf/pyjulia-testing-template.png?branch=master
   :target: http://travis-ci.org/tkf/pyjulia-testing-template
   :alt: Travis Build Status

.. |appveyor-status|
   image:: https://ci.appveyor.com/api/projects/status/x8ajrbq47llt595j?svg=true
   :target: https://ci.appveyor.com/project/tkf/pyjulia-testing-template
   :alt: AppVeyor Build Status

.. |gitlab-status|
   image:: https://gitlab.com/tkfpub/pyjulia-testing-template/badges/master/build.svg
   :target: https://gitlab.com/tkfpub/pyjulia-testing-template/pipelines
   :alt: GitLab Build Status
