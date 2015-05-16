from contextlib2 import contextmanager, ExitStack
from abduct.stream import stdout as out
from abduct.stream import stderr as err

captured_stdout = out  # pylint: disable=invalid-name
captured_stderr = err  # pylint: disable=invalid-name


@contextmanager
def captured(*stream_context_managers):
    """
    Temporarily capture output from the specified streams and optionally
    release it when an exception occurs.
    """
    with __nested(stream_context_managers) as v:
        yield v[0] if len(v) == 1 else v


@contextmanager
def __nested(context_managers):
    with ExitStack() as stack:
        yield tuple(stack.enter_context(c) for c in context_managers)
