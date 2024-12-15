#!/usr/bin/env python

from io import open
from setuptools import setup

"""
:authors: echochel
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 echochel
"""
nm = 'ecr'
version = '0.0.0'
'''
with open('README.md', encoding='utf-8') as f: long_description=f.read()
'''
long_description = 'Python module for graphics integration vulkan'

setup(
    name=nm,
    version=version,
    author='echochel',
    author_email='echochel@bk.ru',
    description=(
        u'Python module for graphics integration vulkan'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=f'https://github.com/echochel/{nm}',
    license='Apache License, Version 2.0, see LICENSE file',
    packages=[nm],
    install_requires=['asyncio'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ]
)