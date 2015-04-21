"""
Language agnostic database migration tool

migrate
=======

A simple language agnostic database migration tool

install
-------
::

    $ pip install migrate

usage
-----
::

    usage: migrate [options] <command>

See Readme_

.. _Readme: https://github.com/kofrasa/migrate/blob/master/README.md
"""

import migrate
from setuptools import setup

setup(
    name='migrate',
    version=migrate.__version__,
    license='MIT',
    author='Francis Asante',
    author_email='kofrasa@gmail.com',
    url='https://github.com/kofrasa/migrate',
    description="A simple language agnostic database migration tool",
    long_description=__doc__,
    py_modules=['migrate'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Database',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': ['migrate=migrate:main']
    }
)