# -*- coding: utf-8 -*-
# Intro: 图片偏移量计算模块
# Author: Ztj
# Email: ztj1993@gmail.com

import os.path
import re

from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8')
readme = f.read()
f.close()

f = open(os.path.join(os.path.dirname(__file__), 'ZtjShifting.py'), encoding='utf8')
version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)
f.close()

setup(
    name='picture-shifting',
    version='0.0.1',
    description='picture shifting',
    long_description=readme,
    long_description_content_type='text/markdown',
    py_modules=['ZtjShifting'],
    url='https://github.com/ztj1993/py-picture-shifting',
    author='ZhangTianJie',
    author_email='ztj1993@gmail.com',
    keywords='picture shifting',
    license='MIT License',
    install_requires=[
        'numpy',
        'opencv-python',
    ],
)
