import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pardakht',
    version='1.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',  # example license
    description='Django app for connecting to Iranian payment gateways.',
    long_description=README,
    url='https://www.github.com/ARKhoshghalb/django-pardakht',
    author='Alireza Khoshghalb',
    author_email='alirezakhoshghalb@ymail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

dependencies = [
	'django-extensions==1.9.8',
	'zeep==2.5.0'
]
