# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="esapp_upload",
    version = "1.0.1",
    author="chenddcoder",
    author_email="chenddcoder@foxmail.com",
    description="A library to compress directories and upload them to ES application server",
    url="https://gitee.com/chenddcoder/esapp-upload.git",  # 替换为你的GitHub仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "requests-toolbelt"
    ],
    entry_points={
        'console_scripts': [
            'esapp-upload=esapp_upload.main:main',
        ],
    },
)