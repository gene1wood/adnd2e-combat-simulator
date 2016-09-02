"""AD&D Second Edition Combat Simulator"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='adnd2e-combat-simulator',
    version='1.0.2',

    description='A tool to simulate combat in AD&D 2nd Edition',
    long_description=long_description,
    url='https://github.com/gene1wood/adnd2e-combat-simulator',
    author='Gene Wood',
    author_email='gene_wood@cementhorizon.com',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ad&d d&d adnd dnd combat',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['PyYAML', 'dice', 'colorama'],
    package_data={
        'adnd2e_combat_simulator': ['combatants.example.yaml'],
    },
    entry_points={
        'console_scripts': [
            'battle=adnd2e_combat_simulator:main',
        ],
    },
)
