# filepath: /spectoconvo/setup.py
from setuptools import setup, find_packages

setup(
    name='spectoconvo',
    version='0.1.0',
    description='A package to embed messages into spectrograms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mitchell Gerrard',
    url='https://github.com/Mitchell-Gerrard/spectoconvo',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'Pillow',
        'scikit-image'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)