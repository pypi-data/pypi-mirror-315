# This file is part of dhlibs (https://github.com/DinhHuy2010/dhlibs)
#
# MIT License
#
# Copyright (c) 2024 DinhHuy2010 (https://github.com/DinhHuy2010)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""dhlibs - random libraries that you shouldn't care"""

def _get_version():
    import importlib.metadata
    return importlib.metadata.version(__name__)

__author__ = "DinhHuy2010"
__copyright__ = "Copyright (c) 2024 DinhHuy2010 (https://github.com/DinhHuy2010)"
__license__ = "MIT"
__version__ = _get_version()

del _get_version
