import sys
from contextlib2 import contextmanager
from abduct.compat import StringIO


def stdout(release_on_exception=False, tee=False):
    return make_stream_context('stdout', release_on_exception, tee)


def stderr(release_on_exception=False, tee=False):
    return make_stream_context('stderr', release_on_exception, tee)


def make_stream_context(stream_name, release_on_exception, tee):
    real_stream = getattr(sys, stream_name)
    fake_stream = TeeStream((real_stream,)) if tee else StringIO()

    @contextmanager
    def context():
        try:
            setattr(sys, stream_name, fake_stream)
            yield fake_stream
        except Exception:
            if release_on_exception and not tee:
                real_stream.write(fake_stream.getvalue())
            raise
        finally:
            setattr(sys, stream_name, real_stream)

    return context()


class TeeStream(object):
    def __init__(self, target_streams):
        self.__impl = StringIO()
        self.__target_streams = tuple(target_streams) + (self.__impl,)

    def __getattr__(self, name):
        return getattr(self.__impl, name)

    def __for_each_target(self, method, *args, **kwargs):
        for t in self.__target_streams:
            getattr(t, method)(*args, **kwargs)

    def flush(self):
        self.__for_each_target('flush')

    def write(self, s):  # pylint: disable=invalid-name
        self.__for_each_target('write', s)

    def writelines(self, iterable):
        for i in iterable:
            self.write(i)
