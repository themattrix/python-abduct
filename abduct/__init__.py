import sys
from abduct.compat import StringIO
from collections import namedtuple
from contextlib import contextmanager


StreamSpec = namedtuple(
    'StreamSpec', (
        'sys_name',
        'release_on_exception'))


def stdout(release_on_exception=True):
    return StreamSpec('stdout', release_on_exception)


def stderr(release_on_exception=True):
    return StreamSpec('stderr', release_on_exception)


@contextmanager
def captured(*stream_specs):
    """
    Temporarily capture output from the specified streams and optionally
    release it when an exception occurs.
    """
    def set_streams(streams):
        for spec, stream in zip(stream_specs, streams):
            setattr(sys, spec.sys_name, stream)

    def put_streams():
        for spec, real, fake in zip(stream_specs, real_streams, fake_streams):
            if spec.release_on_exception:
                real.write(fake.getvalue())

    real_streams = tuple(getattr(sys, s.sys_name) for s in stream_specs)
    fake_streams = tuple(StringIO() for _ in stream_specs)

    try:
        set_streams(fake_streams)
        yield fake_streams if len(fake_streams) != 1 else fake_streams[0]
    except Exception:
        put_streams()
        raise
    finally:
        set_streams(real_streams)
