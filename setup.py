from codecs import open
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vu-timetable',
    version='0.1.0',
    description='Tool to convert VU-Amsterdam timetables to ICS calendar files',
    long_description=long_description,
    author='Georgios Andreadis',
    author_email='info@gandreadis.com',
    license='MIT',
    keywords='sample setuptools development',
    install_requires=['beautifulsoup4>=4.6.0', 'bs4', 'ics', 'pytz', 'selenium'],
)
