#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Flask>=0.11',
    'Flask-GraphQL>=1.3.0',
    'Flask-Webpack==0.1.0',
    'graphene>=0.10',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='relask',
    version='0.1.0',
    description="A Relay-based web development kit on Flask",
    long_description=readme + '\n\n' + history,
    author="Fantix King",
    author_email='fantix.king@gmail.com',
    url='https://github.com/decentfox/relask',
    packages=[
        'relask',
    ],
    package_dir={'relask': 'relask'},
    entry_points='''
        [flask.commands]
        init-relask=relask.cli:init
    ''',
    include_package_data=True,
    install_requires=requirements,
    license="BSD license",
    zip_safe=False,
    keywords='relask',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
