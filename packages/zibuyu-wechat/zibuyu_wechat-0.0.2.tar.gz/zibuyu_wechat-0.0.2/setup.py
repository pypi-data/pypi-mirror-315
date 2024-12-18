# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: zibuyu_LLM
author: 子不语
date: 2024/5/11
contact: 【公众号】思维兵工厂
description: 
--------------------------------------------
"""

from setuptools import setup, find_packages

with open('./Readme.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

VERSION = '0.0.2'
DESCRIPTION = '个人工具-微信相关SDK'

setup(
    name='zibuyu_wechat',
    version=VERSION,
    description='子不语个人工具包-微信相关SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='子不语',
    author_email='zibuyu2015831@qq.com',
    packages=find_packages('./zibuyu_wechat'),
    license='MIT',
    url='https://gitee.com/zibuyu2015831/wechat-sdk',
    package_dir={'': './zibuyu_wechat'},
    keywords=['zibuyu', 'zibuyu_wechat', 'wechat'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=[
        'requests',
        'requests-toolbelt',
    ],
    python_requires='>=3.9'
)
