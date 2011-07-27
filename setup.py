#!/usr/bin/env python

from setuptools import setup, find_packages

version_tuple = __import__('fbkit').VERSION
version = '.'.join([str(v) for v in version_tuple])

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

PACKAGE_DATA = {
    '': [
        'templates/*.*',
        'templates/**/*.*',
    ],
}

REQUIREMENTS = [
    'Django >= 1.3',
]

setup(name='fbkit',
      author='Mirumee Software',
      author_email='hello@mirumee.com',
      description='A Python interface to Facebook APIs',
      version=version,
      url='https://github.com/mirumee/fbkit',
      packages=find_packages(exclude=['tests*']),
      package_data=PACKAGE_DATA,
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      test_suite='tests',
      tests_require=['MiniMock'])
