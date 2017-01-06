# -*- coding: utf-8 -*-
"""cyipopt: Python wrapper for the Ipopt optimization package, written in Cython.

Modified by Eric Chang to work with the IPOPT distribution in anaconda channel pkerichang.

Copyright (C) 2012 Amit Aides, 2015 Matthias Kümmerer
Author: Matthias Kümmerer <matthias.kuemmerer@bethgelab.org>
(originally Author: Amit Aides <amitibo@tx.technion.ac.il>)
URL: <https://bitbucket.org/amitibo/cyipopt>
License: EPL 1.0
"""
from setuptools import setup
from setuptools.extension import Extension
import Cython.Distutils
import Cython.Compiler.Options
import numpy as np
import os
import sys

PACKAGE_NAME = 'ipopt'
VERSION = '0.1.6'


def main_win32():
    raise Exception('Windows is not supported yet.')


def main_unix():
    # if installing using Anaconda, PREFIX will be set properly.
    IPOPT_DIR = os.getenv('PREFIX')
    if IPOPT_DIR is None:
        raise Exception('Please set $PREFIX to be IPOPT installation directory.')

    IPOPT_LIB = os.path.join(IPOPT_DIR, 'lib')
    IPOPT_INC = os.path.join(IPOPT_DIR, 'include/coin/')
    extension = Extension('cyipopt',
                          ['src/cyipopt.pyx', ],
                          # assuming using IPOPT with MUMPS and Metis, compiled against MKL.
                          # this is the setup in my Anaconda channel.
                          libraries=['ipopt', 'coinmumps', 'coinmetis',
                                     'mkl_intel_ilp64', 'mkl_intel_thread', 'mkl_core', 'iomp5',
                                     'pthread', 'm', 'dl'],
                          library_dirs=[IPOPT_LIB],
                          include_dirs=[np.get_include(), IPOPT_INC, ],
                          )

    setup(name=PACKAGE_NAME,
          version=VERSION,
          packages=[PACKAGE_NAME],
          cmdclass={'build_ext': Cython.Distutils.build_ext},
          include_package_data=True,
          ext_modules=[extension],
          )


if __name__ == '__main__':
    if sys.platform == 'win32':
        main_win32()
    else:
        main_unix()
