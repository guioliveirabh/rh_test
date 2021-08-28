"""Package with RH test.

Boilerplate from: https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='rh_test',
    version='1.0.0',
    description='Assignment for RH',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/guioliveirabh/rh_test',
    author='Guilherme',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    zip_safe=False,
    install_requires=['flask==2.0.1', 'flask_restful==0.3.9'],
    package_data={
        'rh_test': ['resources/colors.json'],
    },
    entry_points={
        'console_scripts': [
            'rh_test=rh_test.main:main',
        ],
    }
)
