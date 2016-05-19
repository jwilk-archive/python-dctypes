# encoding=UTF-8

# Copyright © 2014 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ctypes.util import *

import ConfigParser as _cp
import fcntl as _fcntl
import inspect as _inspect
import os as _os

_orig_find_libary = find_library

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
                result = _orig_find_libary(name)
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
