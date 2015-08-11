#!/usr/bin/env python
# Copyright (c) 2015 Michael Kowalchik, TenZeroLab
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""Setup script for the pybald web framework."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import io
import os

import pybald
version = pybald.__version__

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'README.rst'), encoding='utf8') as f:
    README = f.read()
# with io.open(os.path.join(here, 'CHANGELOG.rst'), encoding='utf8') as f:
#     CHANGES = f.read() or ''
CHANGES = ''

setup(name='pybald',
      version=version,
      description='A lightweight python web framework',
      long_description=README + '\n\n' + CHANGES,
      license='MIT',
      keywords='web framework',
      author='Michael Kowalchik',
      author_email='mikepk@tenzerolab.com',
      url='http://pybald.com/',
      packages=find_packages(),
      package_data={'pybald': ['core/default_templates/*.template', 'core/default_templates/forms/*.template']},
      install_requires=[
          "pybald-routes==2.11",
          "FormAlchemy==1.5.5", "SQLAlchemy==1.0.8",
          "WebOb==1.4.1", "Mako==1.0.1", "python-memcached==1.53", "webassets==0.8",
          "lxml==3.2.3", "rjsmin==1.0.10", "cssmin==0.2.0", "PyReact==0.5.2"
      ],
)

