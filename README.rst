The problem with ``ctypes.util.find_library()`` is that there is no guarantee
that it returns a library with ABI compatible with Python code. With
**dctypes** you can make ``find_library()`` return at runtime the same it
returned at build time, hopefully during a comprehensive test suite.

Howto
=====

1) Patch the source: ``s/ctypes/dctypes/g``

2) Run the test suite with ``PYTHON_DCTYPES_BOOT`` environment variable set to
   non-empty string. **dctypes** will collect information about the found
   libraries and save it to a ``.dctypes`` file.

3) ???

4) Profit! At runtime, **dctypes**' ``find_library()`` will return only
   information from the ``.dctypes`` files.

Automatic dependency calculation
================================

**dctypes2elf** creates an ELF library linked to all the libraries from
``.dctypes`` files from the specified directory. The ELF library can be used
to automatically calculate library dependencies, e.g. by ``dpkg-shlibdeps``.


.. _find_library: http://docs.python.org/2/library/ctypes.html#finding-shared-libraries

.. vim:tw=78 ts=3 sts=3 sw=3 et
