# -*- coding: UTF-8 -*-
"""
Flask-Celery
-------------

Flask supports for Module Celery.

"""
from setuptools import setup

version = '0.0.1'

setup(
    name='Flask-Celery',
    version=version,
    url='https://github.com/taogeT/flask-celery',
    license='MIT',
    author='Zheng Wentao',
    author_email='zwtzjd@gmail.com',
    description='Celery 3.0+ integration for Flask',
    long_description=__doc__,
    py_modules=['flask_celery'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'Flask-Script>=2.0.0',
        'Celery>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)