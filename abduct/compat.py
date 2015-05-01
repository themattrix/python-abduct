try:
    from cStringIO import StringIO
except ImportError:          # pragma: no cover
    from io import StringIO  # pragma: no cover

assert StringIO              # silence PyFlakes
