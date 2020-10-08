#!/usr/bin/env python3
import os
import re

from setuptools import setup, find_packages


version = None


def find(haystack, *needles):
    regexes = [(index, re.compile(r'^{}\s*=\s*[\'"]([^\'"]*)[\'"]$'.format(needle))) for index, needle in enumerate(needles)]
    values = ['' for needle in needles]

    for line in haystack:
        if len(regexes) == 0:
            break

        for rindex, (vindex, regex) in enumerate(regexes):
            match = regex.match(line)
            if match:
                values[vindex] = match.groups()[0]
                del regexes[rindex]
                break

    if len(needles) == 1:
        return values[0]
    else:
        return values


with open(os.path.join(os.path.dirname(__file__), 'fooster', 'curse', '__init__.py'), 'r') as pkg:
    version = find(pkg, '__version__')


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as rfile:
    readme = rfile.read()


setup(
    name='fooster-curse',
    version=version,
    description='rewrite identifiers in Python source code with Unicode characters that still have the same canonical normalization',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/lilyinstarlight/python-fooster-curse',
    author='Lily Foster',
    author_email='lily@lily.flowers',
    install_requires=['redbaron'],
    packages=find_packages(),
    namespace_packages=['fooster'],
    entry_points={'console_scripts': ['curse = fooster.curse.__main__:main']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Artistic Software',
        'Topic :: Religion',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Utilities',
    ],
)
