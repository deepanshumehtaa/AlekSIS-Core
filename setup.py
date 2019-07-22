#!/usr/bin/env python3

from setuptools import setup

setup(
    name='BiscuIT-ng',
    version='1.0dev0',
    url='https://edugit.org/Teckids/BiscuIT/BiscuIT-ng',
    author="Teckids e.V.",
    author_email="verein@teckids.org",
    packages=[
        'biscuit.core',
        'biscuit.core.templatetags',
        'biscuit.core.util'
    ],
    namespace_packages=[
        'biscuit',
    ],
    include_package_data=True,
    install_requires=[
        'Django >= 2.0',
        'django-any-js',
        'django-bootstrap4',
        'django-fa',
        'django-easy-audit',
        'django-local-settings',
        'django-phonenumber-field[phonenumbers]',
        'django-simple-menu',
        'django-tables2',
        'Pillow'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
)
