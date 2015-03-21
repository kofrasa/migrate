"""
A simple generic database migration tool
"""

import migrate
from setuptools import setup


def read_file(name):
    with open(name, 'r') as f:
        return f.read()


setup(
    name='migrate',
    version=migrate.__version__,
    license='MIT',
    author='Francis Asante',
    author_email='kofrasa@gmail.com',
    url='https://github.com/kofrasa/migrate',
    description=__doc__,
    long_description=read_file('README.rst'),
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