# -*- coding: UTF-8 -*-
"""
Flask-Celery
-------------

Flask supports for Celery 3.0+ (Python3 version).

"""
from setuptools import setup

import codecs

version = '0.2.3'

setup(
    name='Flask-Celery-py3',
    version=version,
    url='https://github.com/taogeT/flask-celery',
    license='MIT',
    author='Zheng Wentao',
    author_email='zwtzjd@gmail.com',
    description='Celery 3.0+ integration for Flask (Python 3 version)',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    py_modules=['flask_celery'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.11',
        'Celery>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
