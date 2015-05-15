Abduct |Version| |Build| |Coverage| |Health|
============================================

|Compatibility| |Implementations| |Format| |Downloads|

Capture stdout/stderr and optionally release when an exception occurs.

.. code:: python

    from abduct import captured, out, err

    with captured(out()) as stdout:
        ...

    with captured(out(), err()) as (stdout, stderr):
        ...


Installation:

.. code:: console

    $ pip install abduct


When stdout or stderr is captured, the related ``sys.stdout`` or
``sys.stderr`` object is replaced with a ``StringIO`` object for the
life of the context.


Examples
--------

It's often useful to capture the output of a block of code. Abduct
makes this easy:

.. code:: python

    with captured(out()) as stdout:
        print('hello!')

    assert stdout.getvalue() == 'hello!'


Sometimes you may want to hide the output of some code *unless*
something goes wrong. In this case, simply specify
``release_on_exception=True``:

.. code:: python

    with captured(out(release_on_exception=True)):
        print('Really important message!')
        if blow_up:
            raise RuntimeError()


In this case, ``Really important message!`` will be printed on
``stdout`` if the exception is raised.

If you'd like to capture the output, but still write through to
``stdout`` or ``stderr``, use the ``tee=True`` parameter:

.. code:: python

    with captured(err(tee=True)) as stderr:
        sys.stderr.write('Error!')

    assert stderr.getvalue() == 'Error!'


In this case, ``Error!`` is captured *and* written to ``stderr``
at the same time.


Changelog
---------

**2.0.0**

- Feature: "Create a write-through option for output."
- Backwards-incompatible change: ``stdout`` and ``stderr`` methods are now ``out`` and ``err`` respectively.


**1.0.4**

- Fixed Travis release criteria.


**1.0.3**

- Refactored test runner.


**1.0.2**

- Fixed README and description.


**1.0.1**

- Travis config now defers to tox.
- Added examples to README.


**1.0.0**

- Actual working code. Yay!


**0.0.1**

- Initial release.


.. |Build| image:: https://travis-ci.org/themattrix/python-abduct.svg?branch=master
   :target: https://travis-ci.org/themattrix/python-abduct
.. |Coverage| image:: https://img.shields.io/coveralls/themattrix/python-abduct.svg
   :target: https://coveralls.io/r/themattrix/python-abduct
.. |Health| image:: https://landscape.io/github/themattrix/python-abduct/master/landscape.svg
   :target: https://landscape.io/github/themattrix/python-abduct/master
.. |Version| image:: https://pypip.in/version/abduct/badge.svg?text=version
   :target: https://pypi.python.org/pypi/abduct
.. |Downloads| image:: https://pypip.in/download/abduct/badge.svg
   :target: https://pypi.python.org/pypi/abduct
.. |Compatibility| image:: https://pypip.in/py_versions/abduct/badge.svg
   :target: https://pypi.python.org/pypi/abduct
.. |Implementations| image:: https://pypip.in/implementation/abduct/badge.svg
   :target: https://pypi.python.org/pypi/abduct
.. |Format| image:: https://pypip.in/format/abduct/badge.svg
   :target: https://pypi.python.org/pypi/abduct
