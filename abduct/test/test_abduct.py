import sys
from functools import wraps
from nose.tools import eq_
from abduct.compat import StringIO
from abduct import captured, stdout, stderr


#
# Test Decorators
#

def captured_out(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        out, err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = StringIO(), StringIO()
            return func(*args, **kwargs)
        finally:
            sys.stdout, sys.stderr = out, err
    return wrapper


#
# Tests
#

@captured_out
def test_captured_stdout():
    with captured(stdout()) as stdout_cap:
        sys.stdout.write('stdout')
        sys.stderr.write('stderr')

    eq_(stdout_cap.getvalue(), 'stdout')

    eq_(sys.stdout.getvalue(), '')
    eq_(sys.stderr.getvalue(), 'stderr')


@captured_out
def test_captured_stderr():
    with captured(stderr()) as stderr_cap:
        sys.stdout.write('stdout')
        sys.stderr.write('stderr')

    eq_(stderr_cap.getvalue(), 'stderr')

    eq_(sys.stdout.getvalue(), 'stdout')
    eq_(sys.stderr.getvalue(), '')


@captured_out
def test_captured_stdout_and_stderr():
    with captured(stdout(), stderr()) as (stdout_cap, stderr_cap):
        sys.stdout.write('stdout')
        sys.stderr.write('stderr')

    eq_(stdout_cap.getvalue(), 'stdout')
    eq_(stderr_cap.getvalue(), 'stderr')

    eq_(sys.stdout.getvalue(), '')
    eq_(sys.stderr.getvalue(), '')


@captured_out
def test_captured_nothing():
    with captured():
        sys.stdout.write('stdout')
        sys.stderr.write('stderr')

    eq_(sys.stdout.getvalue(), 'stdout')
    eq_(sys.stderr.getvalue(), 'stderr')


@captured_out
def test_captured_stdout_and_stderr_with_release():
    out = stdout(release_on_exception=True)
    err = stderr(release_on_exception=True)

    try:
        with captured(out, err) as (stdout_cap, stderr_cap):
            sys.stdout.write('stdout')
            sys.stderr.write('stderr')

            eq_(stdout_cap.getvalue(), 'stdout')
            eq_(stderr_cap.getvalue(), 'stderr')

            raise MyCustomException()

    except MyCustomException:
        eq_(sys.stdout.getvalue(), 'stdout')
        eq_(sys.stderr.getvalue(), 'stderr')


#
# Test Helpers
#

class MyCustomException(Exception):
    """An exception unlikely to be raised by prodution code."""
