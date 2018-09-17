import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as license_file:
    LICENSE = license_file.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-workflow-tasks',
    version='0.1',
    packages=find_packages(),
    license=LICENSE,
    description='',
    long_description=README,
    author='Ricardo Oyarzún',
    author_email='royarzun@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ],
)