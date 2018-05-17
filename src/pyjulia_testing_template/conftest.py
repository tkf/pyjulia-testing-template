from __future__ import print_function

from contextlib import contextmanager
import os
import subprocess

import pytest


def need_rebuild_pycall():
    # TODO: compare it with ~/.julia/v0.6/PyCall/deps/PYTHON
    return 'PYTHON' in os.environ


@contextmanager
def maybe_rebuild():
    if need_rebuild_pycall():
        # Since pyjulia modifies `os.environ`, I need to save it here:
        env = os.environ.copy()

        build = ['julia', '--color=yes', '-e', 'Pkg.build("PyCall")']
        print('Building PyCall.jl for this Python interpreter...')
        print(*build, end='')
        print(' (PYTHON =', os.environ['PYTHON'], ')')
        subprocess.check_call(build)
        try:
            print('Setting up pyjulia...')
            yield
        finally:
            env.pop('PYTHON', None)
            print('Restoring previous PyCall.jl build...')
            print(*build)
            subprocess.check_call(build, env=env)
    else:
        yield


# Initialize Julia as early as possible.  I don't fully understand it,
# but initializing julia.Julia (loading libjulia) before some other
# Python packages (depending on C extension?) helps avoiding OSError
# complaining GLIBCXX version.
# https://github.com/JuliaDiffEq/diffeqpy/pull/14/commits/5479173b29da4034d6a13c02739e7ac4d35ef96a
#
# It would be cleaner to use `pytest_addoption` but I couldn't find a
# "pre-collection hook" where I can safely initialize Julia before
# loading modules.  Although it is a bit ugly, it is simple if it is
# executed at the top level.
TEST_PYJULIA = os.environ.get('TEST_PYJULIA', 'no') == 'yes'
if TEST_PYJULIA:
    with maybe_rebuild():
        from julia import Julia
        JL = Julia()


@pytest.fixture
def julia():
    """ pytest fixture for providing a `julia.Julia` instance. """
    if TEST_PYJULIA:
        return JL
    else:
        pytest.skip("TEST_PYJULIA=no")
