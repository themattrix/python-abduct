import sys
from collections import namedtuple
from functools import wraps
from nose.tools import eq_
from abduct.compat import StringIO
from abduct import captured, out, err, captured_stdout, captured_stderr


#
# Test Decorators
#

def capture_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        stdout, stderr = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = StringIO(), StringIO()
            return func(sys.stdout, sys.stderr, *args, **kwargs)
        finally:
            sys.stdout, sys.stderr = stdout, stderr
    return wrapper


#
# Tests
#

@capture_wrapper
def test_captured_stdout(stdout, stderr):
    with captured(out()) as stdout_cap:
        write()

    eq_(stdout_cap.getvalue(), 'stdout')
    eq_(stdout.getvalue(), '')
    eq_(stderr.getvalue(), 'stderr')


@capture_wrapper
def test_captured_stderr(stdout, stderr):
    with captured(err()) as stderr_cap:
        write()

    eq_(stderr_cap.getvalue(), 'stderr')
    eq_(stdout.getvalue(), 'stdout')
    eq_(stderr.getvalue(), '')


@capture_wrapper
def test_captured_stdout_and_stderr(stdout, stderr):
    with captured(out(), err()) as (stdout_cap, stderr_cap):
        write()

    eq_(stdout_cap.getvalue(), 'stdout')
    eq_(stderr_cap.getvalue(), 'stderr')
    eq_(stdout.getvalue(), '')
    eq_(stderr.getvalue(), '')


@capture_wrapper
def test_captured_nothing(stdout, stderr):
    with captured():
        write()

    eq_(stdout.getvalue(), 'stdout')
    eq_(stderr.getvalue(), 'stderr')


def test_captured_stdout_and_stderr_scenarios():
    test_scenario = namedtuple(
        'test_scenario', (
            'release',
            'tee',
            'real_output_in_context',
            'real_output_in_except'))

    scenarios = (
        #             release
        #             |  tee
        #             |  |  output in context
        #             |  |  |  output in except
        #             |  |  |  |
        #             v  v  v  v
        test_scenario(0, 0, 0, 0),
        test_scenario(0, 1, 1, 1),
        test_scenario(1, 0, 0, 1),
        test_scenario(1, 1, 1, 1))

    @capture_wrapper
    def assert_scenario(stdout, stderr, scenario):
        context_out = 'stdout' if scenario.real_output_in_context else ''
        context_err = 'stderr' if scenario.real_output_in_context else ''
        except_out = 'stdout' if scenario.real_output_in_except else ''
        except_err = 'stderr' if scenario.real_output_in_except else ''

        o = out(release_on_exception=scenario.release, tee=scenario.tee)
        e = err(release_on_exception=scenario.release, tee=scenario.tee)

        try:
            with captured(o, e) as (stdout_cap, stderr_cap):
                write()

                eq_(stdout_cap.getvalue(), 'stdout')
                eq_(stderr_cap.getvalue(), 'stderr')
                eq_(stdout.getvalue(), context_out)
                eq_(stderr.getvalue(), context_err)

                raise MyCustomException()

        except MyCustomException:
            eq_(stdout.getvalue(), except_out)
            eq_(stderr.getvalue(), except_err)

    for s in scenarios:
        yield assert_scenario, s


@capture_wrapper
def test_capture_stdout(stdout, stderr):
    @captured_stdout()
    def run():
        write()

    run()
    eq_(stdout.getvalue(), '')
    eq_(stderr.getvalue(), 'stderr')


@capture_wrapper
def test_capture_stderr(stdout, stderr):
    @captured_stderr()
    def run():
        write()

    run()
    eq_(stdout.getvalue(), 'stdout')
    eq_(stderr.getvalue(), '')


@capture_wrapper
def test_capture_stdout_and_stderr(stdout, stderr):
    @captured(out(), err())
    def run():
        write()

    run()
    eq_(stdout.getvalue(), '')
    eq_(stderr.getvalue(), '')


#
# Test Helpers
#

def write():
    sys.stdout.writelines(('stdout',))
    sys.stderr.writelines(('stderr',))
    sys.stdout.flush()
    sys.stderr.flush()


class MyCustomException(Exception):
    """An exception unlikely to be raised by prodution code."""
