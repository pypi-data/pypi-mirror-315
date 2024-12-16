
from setuptools import setup, find_packages
import eci


NL = '\n'


with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()


setup(
    name=f'covvi-{eci.__name__}',
    version=eci.__version__,
    description='This project provides the ethernet interface to the COVVI Hand.',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    author='Jordan Birdsall',
    author_email='jordan.birdsall@covvi.com',
    maintainer='Jordan Birdsall',
    maintainer_email='jordan.birdsall@covvi.com',
    url='https://covvi-robotics.github.io/',
    classifiers=[line.strip() for line in '''
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Programming Language :: Python :: 3.13
Operating System :: OS Independent
'''.strip().split(NL)],
    packages=find_packages(),
    python_requires='>=3.8',
    package_data={
        'eci': ['py.typed'],
        'grips': ['*.gbc'],
    }
)
