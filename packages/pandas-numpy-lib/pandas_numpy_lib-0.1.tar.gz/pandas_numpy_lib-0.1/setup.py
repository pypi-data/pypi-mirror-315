# setup.py

from setuptools import setup, find_packages

setup(
    name="pandas_numpy_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    author="Mahesh Makwana",
    author_email="maheshmakwana527@gmail.com",
    description="A library to combine pandas and numpy functionalities.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/MaheshMakwana787/pandas_numpy_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
