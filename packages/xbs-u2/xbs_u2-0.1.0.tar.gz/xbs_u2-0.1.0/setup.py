# coding: utf-8
# Project：uiautomator_sdk
# File：setup.py.py
# Author：张炼武
# Date ：2024/12/13 17:55
# IDE：PyCharm
# my_sdk/setup.py

from setuptools import setup, find_packages

setup(
    name='xbs_u2',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的依赖项，例如：
        'uiautomator2==2.16.25',
    ],
    author='65',
    author_email='18974710587@163.com',
    description='rewrite uiautomator2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ll6566/xbs_uiautomatro',  # 你的项目主页
    python_requires='>=3.0.0',
)
