# encoding=UTF-8

# Copyright © 2014 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

from ctypes.util import *

import ConfigParser as _cp
import fcntl as _fcntl
import inspect as _inspect
import os as _os

_orig_find_library = find_library

if __file__.endswith('.pyc'):
    __file__ = __file__[:-1]

class DctypesError(RuntimeError):
    pass

def find_library(name):
    path = _inspect.stack()[1][1]
    if path.endswith('>'):
        raise DctypesError('non-file modules are not supported')
    path = _os.path.splitext(path)[0] + '.dctypes'
    boot = _os.getenv('PYTHON_DCTYPES_BOOT')
    if path.startswith('/usr/'):
        boot = False
    if boot:
        mode = 'a+'
        lock_mode = _fcntl.LOCK_EX
    else:
        mode = 'r'
        lock_mode = _fcntl.LOCK_SH
    with open(path, mode) as file:
        _fcntl.flock(file, lock_mode)
        cp = _cp.RawConfigParser()
        cp.readfp(file)
        dirty = False
        try:
            cp.add_section('find_library')
        except _cp.DuplicateSectionError:
            pass
        try:
            result = cp.get('find_library', name) or None
        except _cp.NoOptionError:
            if boot:
                result = _orig_find_library(name)
                cp.set('find_library', name, result or '')
                dirty = True
            else:
                raise DctypesError('library not found: {0!r}'.format(name))
        if dirty:
            file.seek(0)
            file.truncate()
            cp.write(file)
        return result

# vim:ts=4 sts=4 sw=4 et
