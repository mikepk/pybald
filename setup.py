#!/usr/bin/env python
# Copyright (c) 2011 Michael Kowalchik, TenZeroLab
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


"""Setup script for pybald."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages  
    # 
    # from distutils.core import setup

setup(name='pybald',
      version='0.1',
      description='A lightweight MVC framework',
      license='MIT',
      author='Michael Kowalchik',
      author_email='mikepk@tenzerolab.com',
      url='http://www.github.com/mikepk/pybald',
      packages=find_packages(),
      install_requires=[
          "Routes>=1.12", "FormAlchemy>=1.3.5", "SqlAlchemy>=0.6.0", 
          "WebOb>=1.0", "Eventlet>=0.9.13.dev1", "Spawning>=0.9.4"
      ]
)

