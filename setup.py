#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Project: Image Alignment  
#             
#
#    File: "$Id$"
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Jerome Kieffer"
__copyright__ = "2012, ESRF"
__license__ = "LGPL"

import sys
from distutils.core import setup
import glob
from numpy.distutils.misc_util import get_numpy_include_dirs

if sys.version_info < (2, 6):
    src = sources = ["feature.cpp"]
    from distutils.core import Extension
    build_ext = None
else:
    src = sources = ["feature.pyx"]
    from Cython.Distutils.extension import Extension
    from Cython.Distutils import build_ext

feature_ext = Extension(
    name="feature",
    
    sources=src + \
        glob.glob("surf/*.cpp")  + \
        glob.glob("sift/*.cpp")  + \
        glob.glob("asift/*.cpp") + \
        glob.glob("orsa/*.cpp"),
    
    include_dirs=get_numpy_include_dirs(),
    language="c++",
    
    undef_macros=['_OPENMP'],
    
    #libraries=["stdc++"],
    #extra_compile_args=['-fopenmp'],
    #extra_link_args=['-fopenmp'],
)


setup(
    name='feature',
    version="0.0.1",
    author="Jerome Kieffer",
    author_email="jerome.kieffer@esrf.eu",
    description='test for feature extraction algorithm like sift, surf, ...',
    ext_modules=[feature_ext],
    cmdclass={'build_ext': build_ext},
)
