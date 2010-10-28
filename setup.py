#!/usr/bin/env python
"""Distutils based setup script for ignition."""


from distutils.core import Command, setup
import sys
import subprocess

try:
    import sympy
except:
    print "Exception occurred whem importing sympy.  You must install sympy "\
        "to use ignition"

import ignition

class test_ignition (Command):
    """Runs all tests under iginition/ folder"""

    description = "run all tests"
    user_options = []

    def __init__ (self, *args):
        self.args = args[0]
        Command.__init__(self, *args)

    def initialize_options(self):  # distutils wants this
        pass

    def finalize_options(self):    # this too
        pass

    def run(self):
        subprocess.Popen("nosetests", shell=True).communicate()

setup(
      name='ignition',
      version=ignition.__version__,
      description='a numerical code generator',
      author='Andy R Terrel',
      author_email='',
      license='FreeBSD',
      url='',
      packages=['ignition'],
      scripts=[],
      ext_modules=[],
      package_data={ },
      data_files=[],
      cmdclass={'test': test_ignition,
                     },
      )
