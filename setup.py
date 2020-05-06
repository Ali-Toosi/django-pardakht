import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pardakht',
    version='1.4.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License', 
    description='Django app for connecting to Iranian payment gateways.',
    long_description=README,
    url='https://www.github.com/Ali-Toosi/django-pardakht',
    author='Ali Toosi',
    author_email='alirezakhoshghalb@ymail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
		'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
	install_requires = [
		'django-extensions==1.9.8',
		'zeep==2.5.0'
	]
)

