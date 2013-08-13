#!/usr/bin/env python
# Copyright (c) 2013 Michael Kowalchik, TenZeroLab
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
    #
    # from distutils.core import setup

setup(name='pybald',
      version='0.2.0',
      description='A lightweight MVC framework',
      license='MIT',
      author='Michael Kowalchik',
      author_email='mikepk@tenzerolab.com',
      url='http://docs.pybald.com/',
      packages=find_packages(),
      package_data={'pybald': ['*.template', 'core/default_templates/forms/*.template']},
      install_requires=[
          "Routes==1.12.5dev",
          "FormAlchemy==1.4.3", "SqlAlchemy==0.8.2",
          "WebOb==1.2.3", "Mako==0.8.1", "python-memcached==1.53", "webassets==0.8",
          "lxml==3.2.3"
      ],
    dependency_links = [
        'http://github.com/mikepk/pybald-routes/tarball/master#egg=Routes-1.12.5dev'
    ]

)

