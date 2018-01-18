# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path



here = path.abspath(path.dirname(__file__))

setup(
    name='slff',
    version='0.1.0',
    description='A library for interacting with SLFF format single-line fonts.',
    # The project's main homepage.
    url='https://github.com/phooky/SLFF',

    # Author details
    author='Adam Mayer',
    author_email='phooky@gmail.com', 

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Printing',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],

    keywords='cnc plotter retrocomputing',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['slff'],
    #package_data={'apple410' : ['data/*.pickle']},
    install_requires=[],

    python_requires='>=3',
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
            'console_scripts': [],
            },
    )
